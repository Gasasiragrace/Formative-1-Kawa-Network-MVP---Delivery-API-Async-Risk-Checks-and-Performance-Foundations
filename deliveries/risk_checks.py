import logging
import time
from datetime import timedelta

from django.utils import timezone

from .models import Plot, RiskCheckAttempt
from .risk_registry import RegistryUnavailable, query_registry

logger = logging.getLogger(__name__)

MAX_ATTEMPTS = 5
BASE_BACKOFF_SECONDS = 30


def is_due(plot: Plot) -> bool:
    """A plot is due if it was never tried, or its exponential backoff has elapsed."""
    last = plot.risk_attempts.order_by('-attempted_at').first()
    if last is None:
        return True
    attempts = plot.risk_attempts.count()
    wait = BASE_BACKOFF_SECONDS * 2 ** (attempts - 1)
    return timezone.now() >= last.attempted_at + timedelta(seconds=wait)


def run_check(plot: Plot) -> None:
    started = time.monotonic()
    try:
        outcome, detail = query_registry(plot), ''
    except RegistryUnavailable as exc:
        outcome, detail = 'error', str(exc)
    duration_ms = int((time.monotonic() - started) * 1000)

    RiskCheckAttempt.objects.create(
        plot=plot, outcome=outcome, detail=detail, duration_ms=duration_ms
    )

    if outcome in ('clear', 'flagged'):
        plot.risk_status = outcome
    elif plot.risk_attempts.count() >= MAX_ATTEMPTS:
        plot.risk_status = 'check_failed'
    plot.save(update_fields=['risk_status'])
    logger.info(
        'Risk check plot=%s outcome=%s status=%s duration_ms=%s',
        plot.pk, outcome, plot.risk_status, duration_ms,
    )


def process_pending() -> int:
    processed = 0
    for plot in Plot.objects.filter(risk_status='pending').order_by('id'):
        if is_due(plot):
            run_check(plot)
            processed += 1
    return processed
