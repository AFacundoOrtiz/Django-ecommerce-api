from django.shortcuts import render
from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer


class ProductListView(generics.ListAPIView):
    # Vista GET lista de todos los productos.
    queryset = Product.objects.filter(is_active=True)

    serializer_class = ProductSerializer
