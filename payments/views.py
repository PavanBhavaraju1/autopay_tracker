from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import Subscription, Card
from .forms import SubscriptionForm, CardForm

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

    context = {
        "auto_list": auto,
        "due_list": due,
        "paid_list": paid,
        "upcoming_list": upcoming,
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
