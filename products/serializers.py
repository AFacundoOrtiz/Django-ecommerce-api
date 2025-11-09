from rest_framework import serializers
from .models import Product, ProductVariant, Category, Brand
from django.db import IntegrityError, transaction


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'slug']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ['name']


class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        # 'product' será manejado por el serializer padre
        exclude = ('product',)
        extra_kwargs = {
            'sku': {'validators': []},
        }


class ProductSerializer(serializers.ModelSerializer):
    # (GET): objeto anidado completo
    category = CategorySerializer(read_only=True)
    brand = BrandSerializer(read_only=True)

    # (POST/PUT): Aceptamos solo el ID
    # 'source' le dice a qué campo del modelo ('category') va este id
    # 'write_only' significa que este campo no aparecerá en el GET
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    brand_id = serializers.PrimaryKeyRelatedField(
        queryset=Brand.objects.all(), source='brand', write_only=True, required=False, allow_null=True
    )

    # Para LECTURA y ESCRITURA:
    # 'required=False' permite crear un producto sin variantes.
    variants = ProductVariantSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = (
            'id',
            'name',
            'slug',
            'description',
            'category',
            'brand',
            'category_id',
            'brand_id',
            'variants'
        )
        pass

    @transaction.atomic
    def create(self, validated_data):
        # 1. Extraemos los datos de las variantes (lista vacía si no vienen)
        variants_data = validated_data.pop('variants', [])

        # 2. Creamos el Producto principal con los datos restantes
        product = Product.objects.create(**validated_data)

        # 3. Iteramos sobre las variantes y las creamos,
        #    asociándolas al producto que acabamos de crear.
        try:
            for variant_data in variants_data:
                ProductVariant.objects.create(product=product, **variant_data)
        except IntegrityError as e:
            raise serializers.ValidationError({
                'variants': f'Error de integridad al crear variantes: {e}'
            })

        return product

    @transaction.atomic
    def update(self, instance, validated_data):
        # Extraemos los datos de las variantes.
        # 'None' significa que si la key 'variants' no viene, no hacemos cambios.
        variants_data = validated_data.pop('variants', None)

        # Actualizamos los campos simples del Producto (name, slug, etc.)
        # Este loop actualiza el 'instance' (el producto) con
        #  los 'validated_data' (los datos nuevos).
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if variants_data is not None:
            # Borrar todas las variantes antiguas y crear las nuevas
            instance.variants.all().delete()
            try:
                for variant_data in variants_data:
                    ProductVariant.objects.create(
                        product=instance, **variant_data)
            except IntegrityError as e:
                raise serializers.ValidationError({
                    'variants': f'Error de integridad al actualizar variantes: {e}'
                })

        return instance
