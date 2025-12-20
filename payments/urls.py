from django.urls import path
from . import views, api_views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("signup/", views.signup, name="signup"),

    path("subscriptions/add/", views.add_subscription, name="add-subscription"),
    path("subscriptions/<int:pk>/edit/", views.edit_subscription, name="edit-subscription"),
    path("subscriptions/<int:pk>/delete/", views.delete_subscription, name="delete-subscription"),

    path("cards/", views.card_list, name="card-list"),
    path("cards/add/", views.add_card, name="add-card"),
    
    path("api/popup-subscription/", api_views.create_from_popup, name="popup-subscription"),
]
