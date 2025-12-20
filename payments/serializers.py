from rest_framework import serializers
from .models import Card, Subscription

class PopupSubscriptionSerializer(serializers.Serializer):
    service_name = serializers.CharField(max_length=100)
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    card_name = serializers.CharField(max_length=100)
    card_last4 = serializers.CharField(max_length=4)
    next_billing_date = serializers.DateField()
    status = serializers.ChoiceField(choices=[
        ("auto", "Auto"), ("due", "Due"), ("paid", "Paid"), ("upcoming", "Upcoming")
    ])
