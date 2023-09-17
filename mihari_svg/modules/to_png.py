from io import BytesIO

import cairosvg
import ulid
from fastapi import APIRouter, Depends, File, UploadFile, status, Form
from fastapi.responses import StreamingResponse
from jinja2 import Template

from pydantic import Json
from ..models.common import RequestQuery_Commons

router = APIRouter()


def render(bytestring: bytes, dpi: int):
    output_file = cairosvg.svg2png(bytestring=bytestring, dpi=dpi)
    return StreamingResponse(
        BytesIO(output_file),
        headers={
            "Content-Disposition": f"inline; filename=mihari-svg-{ulid.new()}.png"
        },
        media_type="image/png",
    )

@router.post(
    "/png",
    summary="Convert SVG to PNG",
    responses={
        status.HTTP_200_OK: {
            "content": {"image/png": {}},
            "description": "Return a PNG image.",
        }
    },
    response_class=StreamingResponse,
)
async def render_png(
    commons: RequestQuery_Commons = Depends(RequestQuery_Commons),
    file: UploadFile = File(description="Source SVG file."),
):
    return render(await file.read(), commons.dpi)

@router.post(
    "/png/template",
    summary="Render with Template, then Convert to PNG",
    responses={
        status.HTTP_200_OK: {
            "content": {"image/png": {}},
            "description": "Return a PNG image.",
        }
    },
    response_class=StreamingResponse,
)
async def render_png_template(
    commons: RequestQuery_Commons = Depends(RequestQuery_Commons),
    file: UploadFile = File(description="Source SVG file, with Jinja2 template format."),
    params: Json = Form(description="Parameters to be rendered.")
):
    template = await file.read()
    renderer = Template(template.decode(), enable_async=True)
    rendered_string = await renderer.render_async(params)
    return render(rendered_string.encode(), commons.dpi)