from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from products import views as product_views

router = DefaultRouter()

#    /api/products/
#    /api/products/<slug>/
router.register(r'products', product_views.ProductViewSet, basename='product')

#    /api/categories/
#    /api/categories/<slug>/
router.register(r'categories', product_views.CategoryViewSet,
                basename='category')

#    /api/brands/
#    /api/brands/<id>/
router.register(r'brands', product_views.BrandViewSet, basename='brand')


# 3. Definimos las URLs del proyecto
urlpatterns = [
    path('admin/', admin.site.urls),

    # 4. Incluimos todas las rutas del router bajo el prefijo 'api/'
    path('api/', include(router.urls)),
]
