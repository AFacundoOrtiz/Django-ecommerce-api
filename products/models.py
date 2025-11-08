from django.db import models


class Brand(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Nombre")

    class Meta:
        verbose_name = "Marca"
        verbose_name_plural = "Marcas"

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Nombre")
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Nombre")
    slug = models.SlugField(max_length=255, unique=True)
    description = models.TextField(
        blank=True, null=True, verbose_name="Descripción")

    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.SET_NULL, null=True, blank=True)
    brand = models.ForeignKey(
        Brand, related_name='products', on_delete=models.SET_NULL, null=True, blank=True)

    is_active = models.BooleanField(default=True, verbose_name="Está activo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def __str__(self):
        return self.name


class ProductVariant(models.Model):
    product = models.ForeignKey(
        Product, related_name='variants', on_delete=models.CASCADE)
    size = models.CharField(max_length=50, verbose_name="Talle")
    color = models.CharField(max_length=50, verbose_name="Color")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Precio")
    stock = models.PositiveIntegerField(default=0, verbose_name="Stock")
    sku = models.CharField(max_length=100, unique=True,
                           blank=True, null=True, verbose_name="SKU")

    class Meta:
        verbose_name = "Variante de Producto"
        verbose_name_plural = "Variantes de Producto"
        unique_together = ('product', 'size', 'color')

    def __str__(self):
        return f"{self.product.name} - {self.size} - {self.color}"
