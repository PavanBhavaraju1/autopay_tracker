from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", auth_views.LoginView.as_view(template_name="payments/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(
        template_name="payments/logout.html",
        next_page="login"
    ), {'http_method_names': ['get', 'post']}, name="logout"),

    path("", include("payments.urls")),
]
