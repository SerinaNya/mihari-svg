from pydantic import BaseModel, conint
from fastapi import Query


class ApiInfo(BaseModel):
    name: str = "jinzhijie/mihari-svg"
    description: str = "Convert SVG to Image"


class RequestQuery_Commons(BaseModel):
    dpi: conint(ge=96, le=600) | None = Query(
        default=96, description="The DPI of outputed image."
    )
