from rest_framework import viewsets, permissions
from .models import Product, Category, Brand
from .serializers import ProductSerializer, CategorySerializer, BrandSerializer
from config.permissions import IsAdminOrReadOnly


class ProductViewSet(viewsets.ModelViewSet):
    """
    - list(): GET /api/products/ (Lista de productos)
    - retrieve(): GET /api/products/<slug>/ (Un producto)
    - create(): POST /api/products/ (Crear un producto)
    - update(): PUT /api/products/<slug>/ (Actualizar un producto)
    - partial_update(): PATCH /api/products/<slug>/ (Actualizar parcial)
    - destroy(): DELETE /api/products/<slug>/ (Eliminar un producto)
    """
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer
    lookup_field = 'slug'

    permission_classes = [IsAdminOrReadOnly]

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class CategoryViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para Categorías.
    Rutas: /api/categories/ y /api/categories/<slug>/
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'


class BrandViewSet(viewsets.ModelViewSet):
    """
    CRUD completo para Marcas.
    Rutas: /api/brands/ y /api/brands/<id>/
    """
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAdminOrReadOnly]
