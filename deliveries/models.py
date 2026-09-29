from django.db import models
from django.core.validators import MinValueValidator


class Farmer(models.Model):
    name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    national_id = models.CharField(max_length=30, unique=True)

    def __str__(self):
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

    def __str__(self):
        return f"Plot ({self.sector}, {self.station})"


class Delivery(models.Model):
    plot = models.ForeignKey(Plot, on_delete=models.CASCADE, related_name='deliveries')
    weight_kg = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    delivered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Delivery of {self.weight_kg}kg from {self.plot}"