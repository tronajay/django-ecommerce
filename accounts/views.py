from rest_framework.viewsets import ViewSet
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from accounts.serializers import UserSerializer, UserAddressSerializer
from accounts.models import Address
from base.throttling import CustomUserLoginThrottle
from rest_framework.exceptions import Throttled


class UserLoginAPIView(TokenObtainPairView):
    throttle_classes = [CustomUserLoginThrottle]

    def throttled(self, request, wait):
        raise Throttled(
            detail={
                "message": f"Login Request Limit Exceeded. Please Wait {wait} seconds and Try again."
            }
        )


class UserAPIViewSet(ViewSet):
    serializer_class = UserSerializer

    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=HTTP_400_BAD_REQUEST, data=serializer.errors)
        serializer.save()
        return Response(status=HTTP_201_CREATED, data=serializer.data)


class UserAddressViewSet(ViewSet, ListAPIView):
    serializer_class = UserAddressSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def create(self, request):
        data = request.data
        data["user"] = request.user.id
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response(status=HTTP_400_BAD_REQUEST, data=serializer.errors)
        serializer.save()
        return Response(status=HTTP_200_OK, data=serializer.data)

    def update(self, request, pk):
        instance = Address.objects.filter(pk=pk).first()
        if not instance:
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={"message": "User Address Does not Exist"},
            )
        serializer = self.get_serializer(
            data=request.data, instance=instance, partial=True
        )
        if not serializer.is_valid():
            return Response(status=HTTP_400_BAD_REQUEST, data=serializer.data)
        serializer.save()
        return Response(status=HTTP_202_ACCEPTED, data=serializer.data)
