from django.contrib.auth import get_user_model
from django.db import models


class ProductCategory(models.Model):
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


class Packaging(models.Model):
    unit = models.ForeignKey("Unit", on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.FloatField(null=True, blank=True)
    packaging_type = models.TextField(null=True, blank=True, help_text="Bag, Box, etc.")


class Product(models.Model):
    category = models.ForeignKey(
        ProductCategory, on_delete=models.SET_NULL, null=True, blank=True
    )
    name = models.TextField(unique=True, db_index=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)
    packaging = models.ForeignKey(Packaging, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


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
    source = models.OneToOneField(ReceiptFile, on_delete=models.CASCADE, null=True, blank=True)
    location = models.ForeignKey(
        Location, on_delete=models.CASCADE, null=True, blank=True
    )
    date = models.DateField(null=True, blank=True, auto_created=True)
    total_paid = models.FloatField(null=True, blank=True)


class LineItem(models.Model):
    receipt = models.ForeignKey(
        Receipt, on_delete=models.CASCADE, related_name="line_items"
    )
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE
    )
    price = models.FloatField(null=True, blank=True)
    quantity = models.FloatField(null=True, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, blank=True)
    unit_price = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.product} - {self.quantity}x{self.unit} @ {self.unit_price}/{self.unit} = {self.price}"
