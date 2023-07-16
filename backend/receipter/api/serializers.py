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
    LineItem, LocationAlias,
)


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = "__all__"


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = "__all__"


class StoreAliasSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreAlias
        fields = "__all__"


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = "__all__"


class LocationAliasSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationAlias
        fields = "__all__"


class ProductSerializer(serializers.ModelSerializer):
    pretty_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"

    @staticmethod
    def get_pretty_name(obj):
        return str(obj)


class ProductAliasSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductAlias
        fields = "__all__"


class ProductCodeSerializer(serializers.ModelSerializer):
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
    product = ProductSerializer()

    class Meta:
        model = LineItem
        exclude = ("receipt",)
        depth = 1


class ReceiptSerializer(serializers.ModelSerializer):
    line_items = LineItemSerializer(many=True, read_only=True)

    class Meta:
        model = Receipt
        fields = "__all__"
        depth = 2
