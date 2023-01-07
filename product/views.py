from rest_framework.viewsets import ViewSet
from .serializers import ProductCategorySerializer, ProductSerializer
from .models import Product, ProductCategory
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView
from .permissions import ReadOnly
from base.pagination import PageNumberPaginationMod

# Create your views here.
class ProductViewSet(ListAPIView, ViewSet):
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticated | ReadOnly,)
    pagination_class = PageNumberPaginationMod

    def create(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=200, data=serializer.data)
        return Response(status=400, data=serializer.errors)

    def list(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        data = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(data)

    def get_product(self, request, product_uuid):
        product = Product.objects.get(uuid=product_uuid)
        serializer = ProductSerializer(product)
        return Response(status=200, data=serializer.data)

    def update(self, request, product_uuid):
        product = Product.objects.get(uuid=product_uuid)
        serializer = ProductSerializer(
            data=request.data, instance=product, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(status=200, data=serializer.data)
        return Response(status=400, data=serializer.errors)

    def product_detail(self, request, slug):
        product = Product.objects.filter(slug=slug).last()
        serializer = ProductSerializer(product)
        return Response(status=200, data=serializer.data)

    def search_products(self, request):
        query = request.query_params.get("q")
        if not query:
            return Response(status=400, data={"error": "Search Keyword is required"})
        queryset = Product.objects.filter(name__icontains=query)
        serializer = ProductSerializer(queryset, many=True)
        data = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(data)


class ProductCategoryViewSet(ViewSet, ListAPIView):
    permission_classes = (IsAuthenticated | ReadOnly,)
    serializer_class = ProductCategorySerializer

    def get_queryset(self):
        queryset = ProductCategory.objects.all()
        return queryset

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=400, data=serializer.errors)
        serializer.save()
        return Response(status=200, data=serializer.data)

    def update(self, request, category_uuid):
        instance = ProductCategory.objects.filter(uuid=category_uuid).last()
        if not instance:
            return Response(
                status=400, data={"error": "Product Category Does not exist"}
            )
        serializer = self.get_serializer(data=request.data, instance=instance)
        if not serializer.is_valid():
            return Response(status=400, data=serializer.errors)
        serializer.save()
        return Response(status=200, data=serializer.data)
