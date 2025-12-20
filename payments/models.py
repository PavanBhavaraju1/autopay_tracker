from django.db import models

class Card(models.Model):
    name = models.CharField(max_length=100)  # e.g. HDFC Credit Card
    last4 = models.CharField(max_length=4)
    issuer = models.CharField(max_length=50, blank=True)  # e.g. Visa
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} •••• {self.last4}"


class Subscription(models.Model):
    STATUS_CHOICES = [
        ("auto", "Auto"),
        ("due", "Due"),
        ("paid", "Paid"),
        ("upcoming", "Upcoming"),
    ]

    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="subscriptions")
    service_name = models.CharField(max_length=100)   # e.g. Netflix
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    billing_cycle_days = models.PositiveIntegerField(default=30)
    next_billing_date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="upcoming")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.service_name} ({self.amount})"
