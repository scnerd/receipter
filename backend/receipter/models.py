import textwrap
from typing import Callable

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import ManyToOneRel
from django.db.transaction import atomic


def CurrencyField(*args, **kwargs):
    kwargs.setdefault("max_digits", 10)
    kwargs.setdefault("decimal_places", 2)
    return models.DecimalField(*args, **kwargs)


def QuantityField(*args, **kwargs):
    kwargs.setdefault("max_digits", 10)
    kwargs.setdefault("decimal_places", 3)
    return models.DecimalField(*args, **kwargs)


class TextualModelManager(models.Manager):
    __text_field_name__: str = ""

    def get_or_create_by_text(self, text: str, get_kwargs: Callable[[], dict] = dict):
        try:
            return self.get(**{self.__text_field_name__: text}), False
        except self.model.DoesNotExist:
            return self.create(**{self.__text_field_name__: text, **get_kwargs()}), True


class OCRManager(TextualModelManager):
    __text_field_name__: str = "ocr_text"


class OCRModel(models.Model):
    ocr_text = models.TextField(unique=True, db_index=True, editable=False)
    value = None

    objects = OCRManager()

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.value} [{textwrap.shorten(self.ocr_text, width=40, placeholder='...')}]"


class TextManager(TextualModelManager):
    __text_field_name__: str = "name"


class TextModel(models.Model):
    name = models.TextField(unique=True, db_index=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class ProductCategory(TextModel):
    parent_category = models.ForeignKey(
        "ProductCategory", on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.name


class Store(TextModel):
    pass


class StoreAlias(OCRModel):
    value = models.ForeignKey(Store, on_delete=models.CASCADE)


class Location(TextModel):
    store = models.ForeignKey(Store, on_delete=models.CASCADE)


class LocationAlias(OCRModel):
    value = models.ForeignKey(Location, on_delete=models.CASCADE)


class Brand(TextModel):
    pass


class Packaging(models.Model):
    unit = models.ForeignKey("Unit", on_delete=models.SET_NULL, null=True, blank=True)
    quantity = QuantityField(null=True, blank=True)
    packaging_type = models.TextField(null=True, blank=True, help_text="Bag, Box, etc.")

    def __str__(self):
        match (self.unit, self.quantity, self.packaging_type):
            case (None, None, None):
                return ""
            case (u, None, None):
                return f"1 {u.name}"
            case (None, q, None):
                return f"{q}"
            case (None, None, pt):
                return pt
            case (u, q, None):
                return f"{q} {u.name}"
            case (u, None, pt):
                return f"1 {u.name} ({pt})"
            case (None, q, pt):
                return f"{q} ({pt})"
            case (u, q, pt):
                return f"{q} {u.name} ({pt})"
            case _:
                raise RuntimeError(
                    f"Unhandled combination: {self.unit}, {self.quantity}, {self.packaging_type}"
                )


class Product(TextModel):
    category = models.ForeignKey(
        ProductCategory, on_delete=models.SET_NULL, null=True, blank=True
    )
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    packaging = models.ForeignKey(
        Packaging, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        match (self.brand, self.packaging):
            case (None, None):
                return self.name
            case (None, p) if not str(p):
                return self.name
            case (b, None):
                return f"{self.name} [{b}]"
            case (None, p):
                return f"{self.name} ({p})"
            case (b, p):
                return f"{self.name} [{b}] ({p})"
            case _:
                raise RuntimeError(
                    f"Unhandled combination: {self.brand}, {self.packaging}"
                )


class ProductAlias(OCRModel):
    store_alias = models.ForeignKey(StoreAlias, on_delete=models.CASCADE)
    value = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["ocr_text", "store_alias"], name="unique_name_per_store"
            )
        ]

    def __str__(self):
        return f"{self.product.name}[{self.store.name}.{self.name}]"


class ProductCode(OCRModel):
    store_alias = models.ForeignKey(StoreAlias, on_delete=models.CASCADE)
    value = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["ocr_text", "store_alias"], name="unique_code_per_store"
            )
        ]

    def __str__(self):
        return f"{self.product.name}[{self.store.name}.{self.code}]"


class Unit(TextModel):
    pass


class UnitAlias(OCRModel):
    value = models.ForeignKey(Unit, on_delete=models.CASCADE)


class ReceiptFile(models.Model):
    # user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    image_file = models.ImageField(upload_to="receipt_images")
    analysis_file = models.FileField(
        upload_to="receipt_analyses", null=True, blank=True
    )


class Receipt(models.Model):
    # user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    source = models.OneToOneField(
        ReceiptFile, on_delete=models.CASCADE, null=True, blank=True
    )
    location_alias = models.ForeignKey(
        Location, on_delete=models.CASCADE, null=True, blank=True
    )
    date = models.DateField(null=True, blank=True, auto_created=True)
    total_paid = CurrencyField(null=True, blank=True)


class LineItem(models.Model):
    receipt = models.ForeignKey(
        Receipt, on_delete=models.CASCADE, related_name="line_items"
    )
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = CurrencyField(null=True, blank=True)
    quantity = QuantityField(null=True, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, blank=True)
    unit_price = CurrencyField(null=True, blank=True)

    def __str__(self):
        return f"{self.product} - {self.quantity}x{self.unit} @ {self.unit_price}/{self.unit} = {self.price}"
