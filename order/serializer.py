from rest_framework import serializers
from product.models import Product
from order.models import Order, LineItem
from accounts.models import User


class LineItemSerializer(serializers.Serializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    quantity = serializers.IntegerField()


class OrderSerializer(serializers.Serializer):
    order_id = serializers.IntegerField(read_only=True)
    products = serializers.ListField(child=LineItemSerializer())
    user = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(), write_only=True
    )

    def create(self, validated_data):
        order_id = 1
        last_order = Order.objects.all().last()
        if last_order:
            order_id += last_order.order_id
        order = Order.objects.create(order_id=order_id, user=validated_data["user"])
        for lineitem in validated_data["products"]:
            LineItem.objects.create(order=order, **lineitem)
        return True

    def validate_products(self, products):
        if not products:
            raise serializers.ValidationError(
                detail="Atleast One Product is Required to Place Order"
            )
        return products


class LineItemViewSerializer(serializers.Serializer):
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    product = serializers.SlugRelatedField(
        queryset=Product.objects.all(), slug_field="name"
    )
    quantity = serializers.IntegerField()


class OrderViewSerializer(serializers.Serializer):
    created_at = serializers.DateTimeField()
    order_id = serializers.IntegerField()
    line_items = serializers.SerializerMethodField()

    def get_line_items(self, instance):
        line_items = LineItem.objects.filter(order=instance)
        return LineItemViewSerializer(line_items, many=True).data
