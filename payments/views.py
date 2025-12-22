from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse, JsonResponse, FileResponse, Http404
import json
import os
from django.conf import settings
from .models import Subscription, Card
from .forms import SubscriptionForm, CardForm
from django.views.decorators.csrf import csrf_exempt
from django.utils.dateparse import parse_date




def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "payments/signup.html", {"form": form})


@login_required
def dashboard(request):
    auto = Subscription.objects.filter(user=request.user, status="auto")
    due = Subscription.objects.filter(user=request.user, status="due")
    paid = Subscription.objects.filter(user=request.user, status="paid")
    upcoming = Subscription.objects.filter(user=request.user, status="upcoming")
    cards = Card.objects.filter(user=request.user)
    show_extension_prompt = not Card.objects.filter(user=request.user).exists()

    context = {
        "auto_list": auto,
        "due_list": due,
        "paid_list": paid,
        "upcoming_list": upcoming,
        "cards": cards,
        "show_extension_prompt": show_extension_prompt,
    }
    return render(request, "payments/dashboard.html", context)


@login_required
def add_subscription(request):
    if request.method == "POST":
        form = SubscriptionForm(request.POST, user=request.user)
        if form.is_valid():
            subscription = form.save(commit=False)
            subscription.user = request.user
            subscription.save()
            return redirect("dashboard")
    else:
        form = SubscriptionForm(user=request.user)

    has_cards = Card.objects.filter(user=request.user).exists()
    return render(
        request,
        "payments/subscription_form.html",
        {"form": form, "title": "Add Subscription", "has_cards": has_cards},
    )


@login_required
def edit_subscription(request, pk):
    subscription = get_object_or_404(Subscription, pk=pk, user=request.user)
    if request.method == "POST":
        form = SubscriptionForm(request.POST, instance=subscription, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
    else:
        form = SubscriptionForm(instance=subscription, user=request.user)
    return render(
        request,
        "payments/subscription_form.html",
        {"form": form, "title": "Edit Subscription"},
    )


@login_required
def delete_subscription(request, pk):
    subscription = get_object_or_404(Subscription, pk=pk, user=request.user)
    if request.method == "POST":
        subscription.delete()
        return redirect("dashboard")
    return render(
        request,
        "payments/subscription_confirm_delete.html",
        {"subscription": subscription},
    )


@login_required
def card_list(request):
    cards = Card.objects.filter(user=request.user)
    return render(request, "payments/card_list.html", {"cards": cards})


@login_required
def add_card(request):
    if request.method == "POST":
        form = CardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.user = request.user
            card.save()
            return redirect("card-list")
    else:
        form = CardForm()
    return render(
        request,
        "payments/card_form.html",
        {"form": form, "title": "Add Card"},
    )


@login_required
def delete_card(request, pk):
    card = get_object_or_404(Card, pk=pk, user=request.user)
    if request.method == "POST":
        card.delete()
        return redirect("card-list")
    return render(request, "payments/card_confirm_delete.html", {"card": card})


@login_required
def bulk_delete_cards(request):
    if request.method == "POST":
        card_ids = request.POST.getlist('card_ids')
        Card.objects.filter(id__in=card_ids, user=request.user).delete()
        return redirect("card-list")
    return redirect("card-list")

@csrf_exempt
@login_required
def api_add_card(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return HttpResponse("Invalid JSON", status=400)

    name = data.get("name", "")
    last4 = data.get("last4", "")
    issuer = data.get("issuer", "")
    is_active = data.get("is_active", True)

    if not last4 or len(last4) != 4:
        return HttpResponse("last4 required", status=400)

    card = Card.objects.create(
        user=request.user,
        name=name or f"Card •••• {last4}",
        last4=last4,
        issuer=issuer,
        is_active=is_active,
    )

    return JsonResponse({"id": card.id, "name": card.name}, status=201)


@csrf_exempt
@login_required
def api_add_subscription(request):
    if request.method != "POST":
        return HttpResponse(status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return HttpResponse("Invalid JSON", status=400)

    service_name = data.get("service_name", "")
    amount = data.get("amount")
    billing_cycle_days = data.get("billing_cycle_days")
    next_billing_date = data.get("next_billing_date")
    status = data.get("status", "upcoming")
    card_id = data.get("card_id")

    if not service_name or amount is None or not billing_cycle_days:
        return HttpResponse("Missing required fields", status=400)

    card = None
    if card_id:
        card = get_object_or_404(Card, id=card_id, user=request.user)

    sub = Subscription.objects.create(
        user=request.user,
        card=card,
        service_name=service_name,
        amount=amount,
        billing_cycle_days=billing_cycle_days,
        next_billing_date=parse_date(next_billing_date) if next_billing_date else None,
        status=status,
    )

    return JsonResponse({"id": sub.id, "service_name": sub.service_name}, status=201)

def extension_install(request):
    """Show instructions for manually installing the Chrome extension in dev mode."""
    return render(request, "payments/extension_install.html")

def extension_download(request):
    """Serve the autopay_extension.zip file for download."""
    zip_path = os.path.join(settings.BASE_DIR, "autopay_extension.zip")
    if not os.path.exists(zip_path):
        raise Http404("Extension ZIP not found. Ask the developer to build autopay_extension.zip.")
    return FileResponse(open(zip_path, "rb"), as_attachment=True, filename="autopay_extension.zip")