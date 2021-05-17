from pydantic import Field

from src.converter import CamelCasedModel, DataProductStandard


class DimensionsAndWeightsResponse(CamelCasedModel):
    gross_weight: str = Field(..., title="Gross weight")
    height: float = Field(..., title="Height")
    length: float = Field(..., title="Length")
    net_weight: float = Field(..., title="Net weight")
    product_description: str = Field(..., title="Product description")
    product_name: str = Field(..., title="Product name")
    volume: float = Field(..., title="Volume")
    width: float = Field(..., title="Width")


class DimensionsAndWeightsRequest(CamelCasedModel):
    product_code: str = Field(..., title="Product code")


STANDARD = DataProductStandard(
    generic_description="Dimensions And Weights",
    request=DimensionsAndWeightsRequest,
    response=DimensionsAndWeightsResponse,
)
