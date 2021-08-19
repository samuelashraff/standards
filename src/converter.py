import importlib.util
import json
from pathlib import Path
from typing import Optional, Type

from deepdiff import DeepDiff
from fastapi import FastAPI, Header
from pydantic import BaseModel
from stringcase import camelcase


class CamelCasedModel(BaseModel):
    class Config:
        alias_generator = camelcase


class DataProductStandard(BaseModel):
    description: Optional[str]
    generic_description: Optional[str]
    name: Optional[str]
    request: Type[BaseModel]
    response: Type[BaseModel]
    route_description: Optional[str]
    route_summary: Optional[str]
    summary: Optional[str]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if generic_description := kwargs.get("generic_description"):
            if not self.route_description:
                self.route_description = generic_description
            if not self.summary:
                self.summary = generic_description
            if not self.description:
                self.description = f"Data Product for {generic_description}"

        if not self.route_description:
            self.route_description = f"{self.name} Data Product"

        if not generic_description and (not self.description or not self.summary):
            raise ValueError(f"Please define required fields for {self.name}")


def export_openapi_spec(standard: DataProductStandard) -> dict:
    """
    Given a data product standard, create a FastAPI application and a corresponding
    POST route. Then export its OpenAPI spec
    :param standard: Data product standard
    :return: OpenAPI spec
    """
    app = FastAPI(
        title=standard.summary,
        description=standard.description,
        version="1.0.0",
    )

    @app.post(
        f"/{standard.name}",
        summary=standard.route_summary,
        description=standard.route_description,
        response_model=standard.response,
    )
    def request(
        params: standard.request,
        x_consent_token: Optional[str] = Header(
            None,
            description="Optional consent token",
        ),
        x_signature: Optional[str] = Header(
            None,
            description="HMAC-RSA256 signature for the request "
            "using Product Gateway's public key",
        ),
        authorization: Optional[str] = Header(
            None, description='The login token. Value should be "Bearer [token]"'
        ),
        x_authorization_provider: Optional[str] = Header(
            None, description="The bare domain of the system that provided the token."
        ),
    ):
        pass

    openapi = app.openapi()

    for path, data in openapi["paths"].items():
        operation_id = data["post"]["operationId"].removesuffix("_post")
        openapi["paths"][path]["post"]["operationId"] = operation_id

    return openapi


def convert_data_product_standards():
    """
    Browse src/draft/DataProducts folder for standards defined as python files
    and export them to corresponding OpenAPI specs in draft/DataProducts folder
    """
    root_dir = Path(__file__).parent.parent
    src_dir = root_dir / "src"
    in_dir = src_dir / "draft" / "DataProducts"

    for p in in_dir.glob("**/*.py"):
        spec = importlib.util.spec_from_file_location(name=str(p), location=str(p))
        if not spec.loader:
            raise RuntimeError(f"Failed to import {p} module")
        module = spec.loader.load_module(str(p))
        standard: DataProductStandard = getattr(module, "STANDARD")
        if not standard:
            raise ValueError(f"Error finding STANDARD variable in {p}")

        # Get standard name based on file path
        standard.name = p.relative_to(in_dir).with_suffix("").as_posix()
        if not standard.route_summary:
            standard.route_summary = standard.name

        openapi = export_openapi_spec(standard)

        out_file = (root_dir / p.relative_to(src_dir)).with_suffix(".json")

        current_spec = {}
        if out_file.exists():
            current_spec = json.loads(out_file.read_text(encoding="utf-8"))

        # Write resulted JSON only if it's changed to satisfy pre-commit hook
        if DeepDiff(current_spec, openapi, ignore_order=True) != {}:
            print(f"Exporting {out_file}")
            out_file.write_text(
                json.dumps(openapi, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
        else:
            print(f"Skipping {out_file}")
