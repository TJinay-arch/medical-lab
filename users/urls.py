from django.urls import path

from .views import CustomLoginView, CustomLogoutView, RegisterView, ActivateUserView, dashboard_router

app_name = "users"

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path(
        "activate/<uidb64>/<token>/",
        ActivateUserView.as_view(),
        name="activate"
    ),
    path("dashboard/", dashboard_router, name="dashboard_router"),
]
