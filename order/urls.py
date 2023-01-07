from django.urls import path
from order.views import OrderViewSet

urlpatterns = [
    path("order/", OrderViewSet.as_view({"post": "create"})),
]
