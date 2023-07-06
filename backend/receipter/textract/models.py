import enum

from pydantic import BaseModel, Field


class Geometry(BaseModel):
    class BoundingBox(BaseModel):
        width: float = Field(alias="Width")
        height: float = Field(alias="Height")
        left: float = Field(alias="Left")
        top: float = Field(alias="Top")

    class PolygonPoint(BaseModel):
        x: float = Field(alias="X")
        y: float = Field(alias="Y")

    bounding_box: BoundingBox | None = Field(alias="BoundingBox", default=None)
    polygon: list[PolygonPoint] | None = Field(alias="Polygon", default=None)


class Text(BaseModel):
    text: str = Field(alias="Text")
    confidence: float = Field(alias="Confidence")

    def __str__(self):
        return self.text


class TextWithGeometry(Text):
    geometry: Geometry = Field(alias="Geometry")


class Currency(BaseModel):
    class CurrencyCode(str, enum.Enum):
        USD = "USD"
        EUR = "EUR"
        GBP = "GBP"
        CAD = "CAD"
        INR = "INR"
        JPY = "JPY"
        CHF = "CHF"
        AUD = "AUD"
        CNY = "CNY"
        BZR = "BZR"
        SEK = "SEK"
        HKD = "HKD"

    code: CurrencyCode = Field(alias="Code")
    confidence: float = Field(alias="Confidence")


class GroupProperty(BaseModel):
    types: list[str] = Field(alias="Types")
    id: str = Field(alias="Id")


class Block(BaseModel):
    class BlockType(str, enum.Enum):
        PAGE = "PAGE"
        WORD = "WORD"
        LINE = "LINE"
        TABLE = "TABLE"
        TABLE_TITLE = "TABLE_TITLE"
        TABLE_FOOTER = "TABLE_FOOTER"
        CELL = "CELL"
        MERGED_CELL = "MERGED_CELL"
        SELECTION_ELEMENT = "SELECTION_ELEMENT"
        SIGNATURE = "SIGNATURE"
        QUERY = "QUERY"
        QUERY_RESULT = "QUERY_RESULT"

    class Relationship(BaseModel):
        class RelationshipType(str, enum.Enum):
            VALUE = "VALUE"
            CHILD = "CHILD"
            MERGED_CELL = "MERGED_CELL"
            ANSWER = "ANSWER"
            TABLE = "TABLE"
            TABLE_TITLE = "TABLE_TITLE"
            TABLE_FOOTER = "TABLE_FOOTER"

        type_: RelationshipType = Field(alias="Type")
        ids: list[str] = Field(alias="Ids")

    block_type: BlockType = Field(alias="BlockType")
    confidence: float = Field(alias="Confidence")
    text: str = Field(alias="Text")
    text_type: str = Field(alias="TextType")
    row_index: int = Field(alias="RowIndex")
    column_index: int = Field(alias="ColumnIndex")
    row_span: int = Field(alias="RowSpan")
    column_span: int = Field(alias="ColumnSpan")
    geometry: Geometry = Field(alias="Geometry")
    id: str = Field(alias="Id")
    relationships: list[Relationship] = Field(alias="Relationships")
    entity_types: list[str] = Field(alias="EntityTypes")
    selection_status: str = Field(alias="SelectionStatus")
    page: int = Field(alias="Page")
    query: dict = Field(alias="Query")


class AnalyzeExpenseResponse(BaseModel):
    class DocumentMetadata(BaseModel):
        pages: int = Field(alias="Pages")

    class ExpenseDocument(BaseModel):
        class SummaryField(BaseModel):
            type_: Text = Field(alias="Type")
            label_detection: TextWithGeometry | None = Field(
                alias="LabelDetection", default=None
            )
            value_detection: TextWithGeometry | None = Field(
                alias="ValueDetection", default=None
            )
            page_number: int = Field(alias="PageNumber")
            currency: Currency | None = Field(alias="Currency", default=None)
            group_properties: list[GroupProperty] = Field(
                alias="GroupProperties", default_factory=list
            )

        class LineItemGroup(BaseModel):
            class LineItem(BaseModel):
                class LineItemExpenseField(BaseModel):
                    type_: Text = Field(alias="Type")
                    label_detection: TextWithGeometry | None = Field(
                        alias="LabelDetection", default=None
                    )
                    value_detection: TextWithGeometry | None = Field(
                        alias="ValueDetection", default=None
                    )
                    page_number: int = Field(alias="PageNumber")
                    currency: Currency | None = Field(alias="Currency", default=None)

                line_item_expense_fields: list[LineItemExpenseField] = Field(
                    alias="LineItemExpenseFields"
                )

            line_item_group_index: int = Field(alias="LineItemGroupIndex")
            line_items: list[LineItem] = Field(alias="LineItems")
            group_properties: list[GroupProperty] = Field(
                alias="GroupProperties", default_factory=list
            )

        expense_index: int = Field(alias="ExpenseIndex")
        summary_fields: list[SummaryField] = Field(alias="SummaryFields")
        line_item_groups: list[LineItemGroup] = Field(alias="LineItemGroups")

    document_metadata: DocumentMetadata = Field(alias="DocumentMetadata")
    expense_documents: list[ExpenseDocument] = Field(alias="ExpenseDocuments")
    blocks: list[Block] = Field(alias="Blocks", default_factory=list)
