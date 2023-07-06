from django.contrib import admin

from receipter.models import ProductCategory, Store, StoreAlias, Location, Product, ProductAlias, ProductCode, Unit, UnitAlias, ReceiptFile, Receipt, LineItem
# Register your models here.


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    class Meta:
        model = ProductCategory


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    class Meta:
        model = Store


@admin.register(StoreAlias)
class StoreAliasAdmin(admin.ModelAdmin):
    class Meta:
        model = StoreAlias


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    class Meta:
        model = Location


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    class Meta:
        model = Product


@admin.register(ProductAlias)
class ProductAliasAdmin(admin.ModelAdmin):
    class Meta:
        model = ProductAlias


@admin.register(ProductCode)
class ProductCodeAdmin(admin.ModelAdmin):
    class Meta:
        model = ProductCode


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    class Meta:
        model = Unit


@admin.register(UnitAlias)
class UnitAliasAdmin(admin.ModelAdmin):
    class Meta:
        model = UnitAlias


@admin.register(ReceiptFile)
class ReceiptFileAdmin(admin.ModelAdmin):
    class Meta:
        model = ReceiptFile


@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    class Meta:
        model = Receipt


@admin.register(LineItem)
class LineItemAdmin(admin.ModelAdmin):
    class Meta:
        model = LineItem
