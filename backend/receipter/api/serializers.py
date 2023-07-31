from rest_framework import serializers

from receipter.models import (
    ProductCategory,
    Store,
    StoreAlias,
    Location,
    Product,
    ProductAlias,
    ProductCode,
    Unit,
    UnitAlias,
    ReceiptFile,
    Receipt,
    LineItem,
    LocationAlias,
    Brand,
)


class StringifiedModelSerializer(serializers.ModelSerializer):
    pretty_name = serializers.SerializerMethodField(read_only=True)

    def get_pretty_name(self, obj):
        return str(obj)


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = "__all__"


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = "__all__"


class StoreAliasSerializer(StringifiedModelSerializer):
    value = StoreSerializer()

    class Meta:
        model = StoreAlias
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class LocationAliasSerializer(StringifiedModelSerializer):
    value = LocationSerializer()

    class Meta:
        model = LocationAlias
        fields = "__all__"


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = "__all__"


class ProductSerializer(StringifiedModelSerializer):
    package_unit_detail = UnitSerializer(source="package_unit", read_only=True)
    brand_detail = BrandSerializer(source="brand", read_only=True)
    category_detail = ProductCategorySerializer(source="category", read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
        # depth = 1


class ProductAliasSerializer(StringifiedModelSerializer):
    value = ProductSerializer()

    class Meta:
        model = ProductAlias
        fields = "__all__"


class ProductCodeSerializer(StringifiedModelSerializer):
    value = ProductSerializer()

    class Meta:
        model = ProductCode
        fields = "__all__"


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = "__all__"


class UnitAliasSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnitAlias
        fields = "__all__"


class ReceiptFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiptFile
        fields = "__all__"


class LineItemSerializer(serializers.ModelSerializer):
    product_detail = ProductSerializer(source="product", read_only=True)
    unit_detail = UnitSerializer(source="unit", read_only=True)

    class Meta:
        model = LineItem
        exclude = ("receipt",)


class ReceiptSerializer(serializers.ModelSerializer):
    line_items = LineItemSerializer(many=True, read_only=True)
    location_detail = LocationSerializer(source="location", read_only=True)
    store_detail = StoreSerializer(source="store", read_only=True)
    source = ReceiptFileSerializer()

    class Meta:
        model = Receipt
        fields = "__all__"
