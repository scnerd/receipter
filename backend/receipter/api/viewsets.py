import json
import logging
import re
from datetime import date
from io import StringIO

import boto3
from dateutil import parser
from django.core.files import File
from django.db.transaction import atomic
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from receipter.api.serializers import ProductCategorySerializer, StoreSerializer, StoreAliasSerializer, \
    LocationSerializer, ProductAliasSerializer, ProductSerializer, ProductCodeSerializer, UnitSerializer, \
    ReceiptFileSerializer, ReceiptSerializer, LineItemSerializer, UnitAliasSerializer
from receipter.models import ProductCategory, Store, StoreAlias, Location, Product, ProductAlias, ProductCode, Unit, UnitAlias, ReceiptFile, Receipt, LineItem
from receipter.textract.models import AnalyzeExpenseResponse


class ProductCategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ProductCategory to be viewed or edited.
    """
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategorySerializer
    # permission_classes = (permissions.IsAuthenticated,)


class StoreViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Store to be viewed or edited.
    """
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    # permission_classes = (permissions.IsAuthenticated,)


class StoreAliasViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows StoreAlias to be viewed or edited.
    """
    queryset = StoreAlias.objects.all()
    serializer_class = StoreAliasSerializer
    # permission_classes = (permissions.IsAuthenticated,)


class LocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Location to be viewed or edited.
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Product to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductAliasViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ProductAlias to be viewed or edited.
    """
    queryset = ProductAlias.objects.all()
    serializer_class = ProductAliasSerializer


class ProductCodeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ProductCode to be viewed or edited.
    """
    queryset = ProductCode.objects.all()
    serializer_class = ProductCodeSerializer


class UnitViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Unit to be viewed or edited.
    """
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer


class UnitAliasViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows UnitAlias to be viewed or edited.
    """
    queryset = UnitAlias.objects.all()
    serializer_class = UnitAliasSerializer


class ReceiptFileViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows ReceiptFile to be viewed or edited.
    """
    queryset = ReceiptFile.objects.all()
    serializer_class = ReceiptFileSerializer

    @staticmethod
    def _sanitize_text(text: str) -> str:
        text = re.sub(r"\s+", " ", text)
        text = text.upper()
        return text

    @staticmethod
    def _parse_summary_field(response: AnalyzeExpenseResponse, field_name: str, finalizer):
        candidate_values = {
            prop.value_detection.text
            for document in response.expense_documents
            for prop in document.summary_fields
            if prop.type_.text == field_name
        }
        match len(candidate_values):
            case 0:
                return finalizer(None)
            case 1:
                return finalizer(candidate_values.pop())
            case _:
                raise ValueError(f"Multiple different values found for {field_name}")

    @action(detail=True, methods=['get', 'post'])
    def analyze(self, request, pk):
        receipt_file: ReceiptFile = self.get_object()
        try:
            receipt = Receipt.objects.get(source=receipt_file)
            return Response(data=dict(success=True, receipt_id=receipt.pk))
        except Receipt.DoesNotExist:
            pass

        if not receipt_file.analysis_file:
            textract = boto3.client("textract")
            response_raw = textract.analyze_expense(
                Document=dict(Bytes=receipt_file.image_file.open('rb').read()),
            )
            receipt_file.analysis_file = File(StringIO(json.dumps(response_raw)), receipt_file.image_file.name + '.json')
            receipt_file.save()
        else:
            response_raw = json.load(receipt_file.analysis_file.open('r'))

        response = AnalyzeExpenseResponse.model_validate(response_raw)

        with atomic():
            store_name = self._parse_summary_field(response, "NAME", self._sanitize_text)
            address = self._parse_summary_field(response, "ADDRESS_BLOCK", self._sanitize_text)
            invoice_date = self._parse_summary_field(
                response,
                "INVOICE_RECEIPT_DATE",
                lambda v: parser.parse(v) if v else date.today(),
            )

            try:
                store_alias = StoreAlias.objects.get(name=store_name)
                store = store_alias.store
            except StoreAlias.DoesNotExist:
                store = Store.objects.get_or_create(name=store_name)[0]
                StoreAlias.objects.create(name=store_name, store=store)

            location = Location.objects.get_or_create(
                store=store,
                name=address,
            )[0]

            receipt = Receipt.objects.create(
                location=location,
                date=invoice_date,
                source=receipt_file,
            )

            logging.info(f"Generating new receipt at {location} on {invoice_date}")

            for doc in response.expense_documents:
                for item_group in doc.line_item_groups:
                    for item_fields in item_group.line_items:
                        # Line item model:
                        # product_code = models.ForeignKey(ProductCode, on_delete=models.CASCADE, null=True, blank=True)
                        # item_name = models.ForeignKey(ProductAlias, on_delete=models.CASCADE, null=True, blank=True)
                        # price = models.FloatField(null=True, blank=True)
                        # quantity = models.FloatField(null=True, blank=True)
                        # unit = models.ForeignKey(UnitAlias, on_delete=models.CASCADE, null=True, blank=True)
                        # unit_price = models.FloatField(null=True, blank=True)
                        simplified_item = {
                            f.type_.text: f.value_detection.text
                            for f in item_fields.line_item_expense_fields
                        }

                        if "PRODUCT_CODE" in simplified_item:
                            try:
                                product_code = ProductCode.objects.get(
                                    code=simplified_item["PRODUCT_CODE"], store=store
                                )
                            except ProductCode.DoesNotExist:
                                _name = simplified_item.get(
                                    "ITEM", simplified_item.get("PRODUCT_CODE")
                                )
                                product = Product.objects.get_or_create(name=_name)[0]
                                product_code = ProductCode.objects.create(
                                    code=simplified_item["PRODUCT_CODE"],
                                    store=store,
                                    product=product,
                                )
                        else:
                            product_code = None

                        if "ITEM" in simplified_item:
                            try:
                                product_alias = ProductAlias.objects.get(
                                    name=simplified_item["ITEM"], store=store
                                )
                            except ProductAlias.DoesNotExist:
                                _name = simplified_item["ITEM"]
                                product = Product.objects.get_or_create(name=_name)[0]
                                product_alias = ProductAlias.objects.create(
                                    name=simplified_item["ITEM"],
                                    store=store,
                                    product=product,
                                )
                        else:
                            product_alias = None

                        match (product_code, product_alias):
                            case (None, None):
                                raise ValueError(f"Product unknown for entry {item_fields}")
                            case (None, x) | (x, None):
                                product = x.product
                            case (x, y) if x.product == y.product:
                                product = x.product
                            case _:
                                raise ValueError(
                                    f"Product code and name map to two different product: {product_code} vs {product_alias}"
                                )

                        price = simplified_item.get("PRICE").split()[0]
                        quantity, _, unit1 = simplified_item.get("QUANTITY", "").partition(" ")
                        unit_price, _, unit2 = simplified_item.get("UNIT_PRICE", "").partition(
                            "/"
                        )

                        price = float(price.strip()) if price else None
                        quantity = float(quantity.strip()) if quantity else None
                        unit_price = float(unit_price.strip()) if unit_price else None

                        match (unit1.strip(), unit2.strip()):
                            case ("", ""):
                                unit = None
                            case (u, "") | ("", u):
                                unit = u
                            case (u1, u2) if u1 == u2:
                                unit = u1
                            case _:
                                unit = unit1

                        if unit:
                            try:
                                unit_alias = UnitAlias.objects.get(text=unit)
                                unit_obj = unit_alias.unit
                            except UnitAlias.DoesNotExist:
                                unit_obj = Unit.objects.get_or_create(name=unit)[0]
                                UnitAlias.objects.create(text=unit, unit=unit_obj)
                        else:
                            unit_obj = None

                        logging.info(
                            dict(
                                product_code=product_code,
                                product_alias=product_alias,
                                product=product,
                                price=price,
                                quantity=quantity,
                                unit=unit_obj,
                                unit_price=unit_price,
                            )
                        )
                        receipt.line_items.create(
                            product=product,
                            price=price,
                            quantity=quantity,
                            unit=unit_obj,
                            unit_price=unit_price,
                        )

        return Response(data=dict(success=True, receipt_id=receipt.pk))


class ReceiptViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows Receipt to be viewed or edited.
    """
    queryset = Receipt.objects.all().order_by('-date')
    serializer_class = ReceiptSerializer


class LineItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows LineItem to be viewed or edited.
    """
    queryset = LineItem.objects.all()
    serializer_class = LineItemSerializer
