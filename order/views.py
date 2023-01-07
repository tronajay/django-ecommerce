from django.shortcuts import render
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_400_BAD_REQUEST
from order.serializer import OrderSerializer, OrderViewSerializer
from order.models import Order

# Create your views here.
class OrderViewSet(ViewSet):
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        request.data["user"] = request.user.id
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                status=HTTP_201_CREATED,
                data={"status": "success", "message": "Order Placed Successfully"},
            )
        return Response(status=HTTP_400_BAD_REQUEST, data=serializer.errors)

    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderViewSerializer(orders, many=True)
        return Response(status=HTTP_200_OK, data=serializer.data)
