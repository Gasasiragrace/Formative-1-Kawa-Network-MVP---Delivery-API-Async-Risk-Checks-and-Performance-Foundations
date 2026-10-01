from django.core.validators import MinValueValidator
from django.db import models


class Farmer(models.Model):
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    national_id = models.CharField(max_length=30, unique=True)

    def __str__(self) -> str:
        return self.name


class Plot(models.Model):
    farmer = models.ForeignKey(Farmer, on_delete=models.CASCADE, related_name='plots')
    sector = models.CharField(max_length=100)
    station = models.CharField(max_length=100)

    RISK_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('clear', 'Clear'),
        ('flagged', 'Flagged'),
        ('check_failed', 'Check Failed'),
    ]
    risk_status = models.CharField(max_length=20, choices=RISK_STATUS_CHOICES, default='pending')

    def __str__(self) -> str:
        return f"Plot ({self.sector}, {self.station})"


class Delivery(models.Model):
    plot = models.ForeignKey(Plot, on_delete=models.CASCADE, related_name='deliveries')
    weight_kg = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
    )
    delivered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Delivery of {self.weight_kg}kg from {self.plot}"


class PriceSchedule(models.Model):
    season = models.CharField(max_length=20)
    grade = models.CharField(max_length=20)
    price_per_kg = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self) -> str:
        return f"{self.season} {self.grade}: {self.price_per_kg}/kg"


class RiskCheckAttempt(models.Model):
    OUTCOME_CHOICES = [
        ('clear', 'Clear'),
        ('flagged', 'Flagged'),
        ('error', 'Error'),
    ]

    plot = models.ForeignKey(Plot, on_delete=models.CASCADE, related_name='risk_attempts')
    attempted_at = models.DateTimeField(auto_now_add=True)
    outcome = models.CharField(max_length=10, choices=OUTCOME_CHOICES)
    detail = models.CharField(max_length=255, blank=True)
    duration_ms = models.PositiveIntegerField(default=0)

    def __str__(self) -> str:
        return f"Plot {self.plot_id} attempt: {self.outcome}"
