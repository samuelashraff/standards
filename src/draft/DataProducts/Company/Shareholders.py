from typing import List

from pydantic import BaseModel, Field

from src.converter import DataProductStandard


class ShareSeries(BaseModel):
    seriesName: str = Field(
        ..., title="Series Name", description="Classification of the share", example="A"
    )
    votesPerShare: int = Field(
        ...,
        title="Votes per share",
        description="Number of votes per share in the share series",
        example=1,
    )
    totalShares: int = Field(
        ...,
        title="Total Shares",
        description="Total number of shares in the share series",
        example=1000,
    )


class Ownerships(BaseModel):
    seriesName: str = Field(
        ..., title="Series Name", description="Name of the share series", example="A"
    )
    quantity: int = Field(
        ...,
        title="Number of Shares",
        description="Number of shares held by the owner",
        example=100,
    )


class Owners(BaseModel):
    name: str = Field(
        ...,
        title="Name of the Shareholder",
        description="Name of the shareholder",
        example="Matti Meikäläinen | Oy Company Ltd",
    )
    ownerships: List[Ownerships] = Field(
        ..., title="Ownerships", description="List of Ownerships"
    )


class ShareholdersInfoRequest(BaseModel):
    companyId: str = Field(
        ...,
        title="Company ID",
        description="The ID of the company, only supports Finnish business ID's",
        example="2464491-9",
    )


class ShareholdersInfoResponse(BaseModel):
    shareSeries: List[ShareSeries] = Field(
        ..., title="Share series", description="List of share series"
    )
    owners: List[Owners] = Field(..., title="Owners", description="List of owners")


STANDARD = DataProductStandard(
    description="Data Product for Shareholders info",
    request=ShareholdersInfoRequest,
    response=ShareholdersInfoResponse,
    route_description="Information about the shareholders of the company",
    summary="Shareholders Info",
)
