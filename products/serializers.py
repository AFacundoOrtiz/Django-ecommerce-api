from rest_framework import serializers
from .models import Product, ProductVariant, Brand, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug')


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ('name',)


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ('size', 'color', 'price', 'stock', 'sku')


class ProductSerializer(serializers.ModelSerializer):
    variants = ProductVariantSerializer(many=True, read_only=True)

    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'slug',
            'description',
            'category',
            'brand',
            'variants'
        )
