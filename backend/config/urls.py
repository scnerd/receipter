"""
URL configuration for receipter project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from receipter.api.viewsets import ProductCategoryViewSet, StoreViewSet, StoreAliasViewSet, LocationViewSet, \
    ProductViewSet, ProductAliasViewSet, ProductCodeViewSet, UnitViewSet, UnitAliasViewSet, ReceiptFileViewSet, \
    ReceiptViewSet, LineItemViewSet

router = routers.DefaultRouter()
router.register(r'categories', ProductCategoryViewSet)
router.register(r'stores', StoreViewSet)
router.register(r'stores-aliases', StoreAliasViewSet)
router.register(r'locations', LocationViewSet)
router.register(r'products', ProductViewSet)
router.register(r'product-aliases', ProductAliasViewSet)
router.register(r'product-codes', ProductCodeViewSet)
router.register(r'units', UnitViewSet)
router.register(r'unit-aliases', UnitAliasViewSet)
router.register(r'receipt-files', ReceiptFileViewSet)
router.register(r'receipts', ReceiptViewSet)
router.register(r'line-items', LineItemViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path("admin/", admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
