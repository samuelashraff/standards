from typing import List

from pydantic import BaseModel, Field

from src.converter import DataProductStandard


class HealthDiagnosesRequest(BaseModel):
    pass


class HealthDiagnosesResponse(BaseModel):
    diagnoses: List[str] = Field(
        ..., description="List of users diagnoses in ICD10 code", example=["icd10:J45"]
    )


STANDARD = DataProductStandard(
    description="Data Product for user's diagnoses with ICD10 codes",
    request=HealthDiagnosesRequest,
    response=HealthDiagnosesResponse,
    route_description="Health diagnoses in ICD codes",
    summary="Persons Diagnoses",
)
