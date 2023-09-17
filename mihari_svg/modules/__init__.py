from fastapi import APIRouter
from . import to_png

router = APIRouter()

for module in [to_png]:
    router.include_router(module.router)
