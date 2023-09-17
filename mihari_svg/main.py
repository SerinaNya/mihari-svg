from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from . import modules
from .models.common import ApiInfo

app = FastAPI(
    title="mihari-svg", description="Convert SVG file to other image formats."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(modules.router)


@app.get(
    "/",
    response_model=ApiInfo,
    summary="API Information",
    response_description="The information of this project.",
)
async def root():
    return ApiInfo()
