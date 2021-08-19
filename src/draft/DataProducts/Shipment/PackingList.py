from typing import List

from pydantic import Field

from src.converter import CamelCasedModel, DataProductStandard


class ProductItem(CamelCasedModel):
    product_code: str = Field(..., title="Product code")
    product_count: int = Field(..., title="Product count")


class PackingListResponse(CamelCasedModel):
    contract_reference: str = Field(..., title="Contract reference")
    description_of_goods: str = Field(..., title="Description of goods")
    final_destination: str = Field(..., title="Final destination")
    handling_units: int = Field(..., title="Handling units")
    incoterm: str = Field(..., title="Incoterm")
    incoterm_place: str = Field(..., title="Incoterm place")
    lc_number: str = Field(..., title="LC number")
    packing_description: str = Field(..., title="Packing description")
    packing_reference: str = Field(..., title="Packing reference")
    place_of_receipt: str = Field(..., title="Place of receipt")
    product_items: List[ProductItem] = Field(
        ..., title="Product items", description="List of product items"
    )
    total_gross_weight: float = Field(..., title="Total gross weight")
    total_net_weight: float = Field(..., title="Total net weight")
    total_volume: float = Field(..., title="Total volume")


class PackingListRequest(CamelCasedModel):
    shipment_id: str = Field(..., title="Shipment ID")


STANDARD = DataProductStandard(
    generic_description="Packing List",
    request=PackingListRequest,
    response=PackingListResponse,
)
