from django.urls import path
from .views import UserAPIViewSet, UserAddressViewSet, UserLoginAPIView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("login/", UserLoginAPIView.as_view(), name="login_token_obtain_pair"),
    path(
        "register/",
        UserAPIViewSet.as_view({"post": "create"}),
        name="user_register_api_view",
    ),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path(
        "address/",
        UserAddressViewSet.as_view({"post": "create"}),
        name="get_saved_address_for_users",
    ),
    path(
        "address/<int:pk>/",
        UserAddressViewSet.as_view({"patch": "update"}),
        name="update_user_address",
    ),
]
