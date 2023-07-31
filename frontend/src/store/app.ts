// Utilities
import { defineStore } from 'pinia'
import {DBObjBase, defineDRFStore} from "@/utils";

export const useAppStore = defineStore('app', {
  state: () => ({
    //
  }),
})

/* Django Models
import textwrap
from typing import Callable

from django.core.validators import RegexValidator
from django.db import models


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

    objects = TextManager()

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


class Product(TextModel):
    variant = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        ProductCategory, on_delete=models.SET_NULL, null=True, blank=True
    )
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, blank=True)

    package_unit = models.ForeignKey("Unit", on_delete=models.SET_NULL, null=True, blank=True)
    package_quantity = QuantityField(null=True, blank=True)
    package_type = models.TextField(null=True, blank=True, help_text="Bag, Box, etc.")

    @property
    def packaging_pretty_str(self):
        match self.package_quantity:
            case None:
                cleaned_quantity = None
            case i if i == int(i):
                cleaned_quantity = int(i)
            case i:
                cleaned_quantity = i

        match (self.package_unit, cleaned_quantity, self.package_type):
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
                return f"1 {u.name} {pt}"
            case (None, q, pt):
                return f"{q} {pt}s"
            case (u, q, pt):
                return f"{q} {u.name} {pt}"
            case _:
                raise RuntimeError(
                    f"Unhandled combination: {self.package_unit}, {self.package_quantity}, {self.package_type}"
                )

    def __str__(self):
        entries = [self.name]
        if self.variant:
            entries.append(self.variant)
        if self.packaging_pretty_str:
            entries.append(self.packaging_pretty_str)

        return ' - '.join(entries)


class ProductAlias(OCRModel):
    store_alias = models.ForeignKey(StoreAlias, on_delete=models.CASCADE)
    value = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["ocr_text", "store_alias"], name="unique_name_per_store"
            )
        ]


class ProductCode(OCRModel):
    store_alias = models.ForeignKey(StoreAlias, on_delete=models.CASCADE)
    value = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["ocr_text", "store_alias"], name="unique_code_per_store"
            )
        ]


class Unit(TextModel):
    pass


class UnitAlias(OCRModel):
    value = models.ForeignKey(Unit, on_delete=models.CASCADE)


class ReceiptFile(models.Model):
    # user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    image_sha256 = models.CharField(max_length=64, unique=True, db_index=True, validators=[
        RegexValidator(r'[a-f0-9]{64}')
    ])
    image_file = models.ImageField(upload_to="receipts/images")
    analysis_file = models.FileField(upload_to="receipts/analyses")


class Receipt(models.Model):
    # user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    source = models.OneToOneField(
        ReceiptFile, on_delete=models.CASCADE, null=True, blank=True
    )
    location_alias = models.ForeignKey(
        LocationAlias, on_delete=models.CASCADE, null=True, blank=True
    )
    date = models.DateField(null=True, blank=True, auto_created=True)
    total_paid = CurrencyField(null=True, blank=True)

    @property
    def location(self):
        return self.location_alias.value if self.location_alias else None

    @property
    def store(self):
        return self.location.store if self.location else None


class LineItem(models.Model):
    receipt = models.ForeignKey(
        Receipt, on_delete=models.CASCADE, related_name="line_items"
    )
    product_code = models.ForeignKey(ProductCode, on_delete=models.SET_NULL, null=True, blank=True)
    product_alias = models.ForeignKey(ProductAlias, on_delete=models.SET_NULL, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    price = CurrencyField(null=True, blank=True)
    quantity = QuantityField(null=True, blank=True)
    unit_alias = models.ForeignKey(UnitAlias, on_delete=models.SET_NULL, null=True, blank=True)
    unit = models.ForeignKey(Unit, on_delete=models.SET_NULL, null=True, blank=True)
    unit_price = CurrencyField(null=True, blank=True)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return f"{self.product} - {self.quantity}x{self.unit} @ {self.unit_price}/{self.unit} = {self.price}"

 */


export interface ProductCategory extends DBObjBase {
  name: string
  parentCategory?: ProductCategory
}

export interface Store extends DBObjBase {
  name: string
}

export interface StoreAlias extends DBObjBase {
  ocr_text: string
  value: Store
}

export interface Location extends DBObjBase {
  name: string
  value: number
}

export interface LocationAlias extends DBObjBase {
  ocr_text: string
  value: Location
}

export interface Brand extends DBObjBase {
  name: string
}

export interface Product extends DBObjBase {
  name: string
  variant?: string
  category?: number
  brand?: number
  package_unit?: number
  package_quantity?: number
  package_type?: string
}

export interface ProductAlias extends DBObjBase {
  ocr_text: string
  value: Product
}

export interface ProductCode extends DBObjBase {
  ocr_text: string
  value: Product
}

export interface Unit extends DBObjBase {
  name: string
}

export interface UnitAlias extends DBObjBase {
  ocr_text: string
  value: Unit
}

// interface ReceiptFile extends DBObjBase {
//
// }

export interface Receipt extends DBObjBase {
  source?: number
  location_alias?: number
  date?: Date
  total_paid?: number
  location?: number
  store?: number
}

export interface LineItem extends DBObjBase {
  receipt?: number
  product_code?: number
  product_alias?: number
  product?: number
  price?: number
  quantity?: number
  unit_alias?: number
  unit?: number
  unit_price?: number
}

// And now, we create DRF Stores for each type

export const useProductCategoryStore = defineDRFStore<ProductCategory>('categories');
export const useStoreStore = defineDRFStore<Store>('stores');
export const useStoreAliaStore = defineDRFStore<StoreAlias>('store-aliases');
export const useLocationStore = defineDRFStore<Location>('locations');
export const useLocationAliasStore = defineDRFStore<LocationAlias>('location-aliases');
export const useBrandStore = defineDRFStore<Brand>('brands');
export const useProductStore = defineDRFStore<Product>('products');
export const useProductAliasStore = defineDRFStore<ProductAlias>('product-aliases');
export const useProductCodeStore = defineDRFStore<ProductCode>('product-codes');
export const useUnitStore = defineDRFStore<Unit>('units');
export const useUnitAliasStore = defineDRFStore<UnitAlias>('unit-aliases');
// export const useReceiptFileStore = defineDRFStore<ReceiptFile>('receipt-files');
export const useReceiptStore = defineDRFStore<Receipt>('receipts');
export const useLineItemStore = defineDRFStore<LineItem>('line-items');
