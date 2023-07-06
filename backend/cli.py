# Create typer CLI
import enum
import json
import re
from datetime import date
from pathlib import Path

import boto3
import typer
from dateutil import parser

import os

from django.core.files.images import ImageFile
from django.core.files import File

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from receipter.models import (
    StoreAlias,
    Location,
    Receipt,
    ProductCode,
    Store,
    Product,
    ProductAlias,
    UnitAlias,
    Unit,
    ReceiptFile,
)
from receipter.textract.models import AnalyzeExpenseResponse

cli = typer.Typer(pretty_exceptions_enable=False)


def analyze_receipt(receipt_file: Path) -> AnalyzeExpenseResponse:
    response_file = receipt_file.with_suffix(".json")
    if response_file.exists():
        response = json.loads(response_file.read_text())
    else:
        textract = boto3.client("textract")
        response = textract.analyze_expense(
            Document=dict(Bytes=receipt_file.read_bytes()),
        )
        response_file.write_text(json.dumps(response))

    return AnalyzeExpenseResponse.model_validate(response)


def _sanitize_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    text = text.upper()
    return text


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


# Create command for ingesting new receipt
@cli.command()
def add(scan_file: Path):
    """
    Ingest a new receipt
    """
    assert scan_file.exists()
    response = analyze_receipt(scan_file)
    receipt_file = ReceiptFile.objects.update_or_create(
        image_file=ImageFile(scan_file.open("rb")),
        defaults=dict(analysis_file=File(scan_file.with_suffix(".json").open("rb"))),
    )[0]

    store_name = _parse_summary_field(response, "NAME", _sanitize_text)
    address = _parse_summary_field(response, "ADDRESS_BLOCK", _sanitize_text)
    invoice_date = _parse_summary_field(
        response,
        "INVOICE_RECEIPT_DATE",
        lambda v: parser.parse(v) if v else date.today(),
    )

    try:
        store_alias = StoreAlias.objects.get(name=store_name)
        store = store_alias.store
    except StoreAlias.DoesNotExist:
        store = Store.objects.get_or_create(name=store_name)[0]
        store_alias = StoreAlias.objects.create(name=store_name, store=store)

    location = Location.objects.get_or_create(
        store=store,
        name=address,
    )[0]

    receipt = Receipt.objects.create(
        location=location,
        date=invoice_date,
        source=receipt_file,
    )

    typer.echo(f"Generating new receipt at {location} on {invoice_date}")

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
                        unit = typer.prompt(
                            f"Multiple units found: {unit1} and {unit2}, choose one",
                            type=enum.Enum("Unit", {unit1: unit1, unit2: unit2}),
                        ).value

                if unit:
                    try:
                        unit_alias = UnitAlias.objects.get(text=unit)
                        unit_obj = unit_alias.unit
                    except UnitAlias.DoesNotExist:
                        unit_obj = Unit.objects.get_or_create(name=unit)[0]
                        unit_alias = UnitAlias.objects.create(text=unit, unit=unit_obj)
                else:
                    unit_obj = None

                typer.echo(
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


if __name__ == "__main__":
    cli()
