from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from accounts.models import User, Address


class UserSerializer(serializers.Serializer):
    first_name = serializers.CharField(
        max_length=256, allow_blank=True, allow_null=True, required=False
    )
    last_name = serializers.CharField(
        max_length=256, allow_blank=True, allow_null=True, required=False
    )
    mobile_number = serializers.CharField(
        max_length=256, allow_blank=True, allow_null=True, required=False
    )
    email = serializers.EmailField(
        max_length=100, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(max_length=100, write_only=True)

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return validated_data


class UserAddressSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    address_1 = serializers.CharField(max_length=200)
    address_2 = serializers.CharField(max_length=200, required=False, allow_blank=True)
    city = serializers.CharField(max_length=100)
    state = serializers.CharField(max_length=50)
    postal_code = serializers.CharField(max_length=6)
    phone = serializers.CharField(max_length=13)
    company = serializers.CharField(required=False, max_length=50)

    def create(self, validated_data):
        return Address.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for key in validated_data.keys():
            setattr(instance, key, validated_data[key])
        instance.save()
        return instance
