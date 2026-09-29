"""Simulated external risk registry: slow and often unavailable."""
import os
import random
import time

from .models import Plot


class RegistryUnavailable(Exception):
    """Raised when the external registry times out or is down."""


def query_registry(plot: Plot) -> str:
    max_delay = float(os.environ.get('KAWA_REGISTRY_MAX_DELAY', '3'))
    failure_rate = float(os.environ.get('KAWA_REGISTRY_FAILURE_RATE', '0.3'))
    time.sleep(random.uniform(0.5, max_delay))
    if random.random() < failure_rate:
        raise RegistryUnavailable('Registry timed out or is unavailable')
    return 'flagged' if random.random() < 0.1 else 'clear'
