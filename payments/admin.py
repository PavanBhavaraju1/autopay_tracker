from django.contrib import admin
from .models import Card, Subscription

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ("name", "last4", "issuer", "is_active")
    search_fields = ("name", "last4", "issuer")


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("service_name", "card", "amount", "status", "next_billing_date")
    list_filter = ("status", "card")
    search_fields = ("service_name",)
