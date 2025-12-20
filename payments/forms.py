from django import forms
from .models import Subscription, Card

class SubscriptionForm(forms.ModelForm):
    class Meta:
        model = Subscription
        fields = [
            "card",
            "service_name",
            "amount",
            "billing_cycle_days",
            "next_billing_date",
            "status",
        ]
        labels = {
            "card": "Card",
            "service_name": "Service name",
            "amount": "Amount",
            "billing_cycle_days": "Billing cycle days",
            "next_billing_date": "Next billing date",
            "status": "Status",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["card"].empty_label = "Select a card"
        self.fields["card"].help_text = (
            "Don’t see your card? Click “Add card” to create it, then come back."
        )


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ["name", "last4", "issuer", "is_active"]
        labels = {
            "name": "Card name (e.g. HDFC Credit Card)",
            "last4": "Last 4 digits",
            "issuer": "Issuer (e.g. Visa)",
            "is_active": "Active",
        }
