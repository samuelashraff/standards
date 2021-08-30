from pydantic import BaseModel, Field

from src.converter import DataProductStandard


class BasicCompanyInfoRequest(BaseModel):
    companyId: str = Field(
        ...,
        title="Company ID",
        description="The ID of the company",
        example="2464491-9",
    )


class BasicCompanyInfoResponse(BaseModel):
    name: str = Field(
        ..., title="Name of the company", example="Digital Living International Oy"
    )
    companyId: str = Field(..., title="ID of the company", example="2464491-9")
    companyForm: str = Field(
        ..., title="The company form of the company", example="LLC"
    )
    registrationDate: str = Field(
        ..., title="Date of registration for the company", example="2012-02-23"
    )


STANDARD = DataProductStandard(
    description="Data Product for basic company info",
    request=BasicCompanyInfoRequest,
    response=BasicCompanyInfoResponse,
    route_description="Information about the company",
    summary="Basic Company Info",
)
