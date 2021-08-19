from typing import List

from pydantic import BaseModel, Field

from src.converter import DataProductStandard


class RecommendationRequest(BaseModel):
    keywords: str = Field(
        ...,
        title="Keywords",
        description="Keyword data to base recommendations on",
        example="Looking for data product companies to invest on",
    )


class Recommendation(BaseModel):
    score: int = Field(
        ..., description="Recommendation score of the company", example=231
    )
    companyId: str = Field(
        ..., title="Company ID", description="Company ID", example="2464491-9"
    )
    companyName: str = Field(
        ...,
        title="Company name",
        description="Company name",
        example="Digital Living Oy",
    )


class RecommendationResponse(BaseModel):
    results: List[Recommendation] = Field(
        ..., title="Recommendation results", description="List of recommendations"
    )


STANDARD = DataProductStandard(
    request=RecommendationRequest,
    response=RecommendationResponse,
    route_description="Data Product for company recommendations score",
    description="Data Product for company recommendations score",
    summary="Company Recommendations Scores",
)
