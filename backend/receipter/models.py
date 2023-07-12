from django.contrib.auth import get_user_model
from django.db import models


def CurrencyField(*args, **kwargs):
    kwargs.setdefault("max_digits", 10)
    kwargs.setdefault("decimal_places", 2)
    return models.DecimalField(*args, **kwargs)


def QuantityField(*args, **kwargs):
    kwargs.setdefault("max_digits", 10)
    kwargs.setdefault("decimal_places", 3)
    return models.DecimalField(*args, **kwargs)


class ProductCategory(models.Model):
    parent_category = models.ForeignKey(
        "ProductCategory", on_delete=models.SET_NULL, null=True, blank=True
    )
    name = models.TextField(unique=True, db_index=True)

    def __str__(self):
        return self.name


class Store(models.Model):
    name = models.TextField(unique=True, db_index=True)

    def __str__(self):
        return self.name


class StoreAlias(models.Model):
    name = models.TextField(unique=True, db_index=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.store.name}[{self.name}]"


class Location(models.Model):
    name = models.TextField(unique=True, db_index=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.store.name}[{self.name}]"


class Brand(models.Model):
    name = models.TextField(unique=True, db_index=True)

    def __str__(self):
        return self.name


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


class Product(models.Model):
    category = models.ForeignKey(
        ProductCategory, on_delete=models.SET_NULL, null=True, blank=True
    )
    name = models.TextField()
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


class ProductAlias(models.Model):
    name = models.TextField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "store"], name="unique_name_per_store"
            )
        ]

    def __str__(self):
        return f"{self.product.name}[{self.store.name}.{self.name}]"


class ProductCode(models.Model):
    code = models.TextField()
    store = models.ForeignKey(Store, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["code", "store"], name="unique_code_per_store"
            )
        ]

    def __str__(self):
        return f"{self.product.name}[{self.store.name}.{self.code}]"


class Unit(models.Model):
    name = models.TextField(unique=True, db_index=True)

    def __str__(self):
        return self.name


class UnitAlias(models.Model):
    text = models.TextField(unique=True, db_index=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.unit.name}[{self.text}]"


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
    location = models.ForeignKey(
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
