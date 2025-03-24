from typing import Dict

from fastapi import APIRouter

from app.core.enums import get_mas_framework_names
from app.models.llm import get_models, get_model_ids

router = APIRouter(prefix="/system", tags=["system"])


@router.get("/maf-llm-models", response_model=Dict)
def get_maf_models():
    return get_model_ids()

@router.get("/maf-frameworks", response_model=Dict)
def get_maf_frameworks():
    return get_mas_framework_names()

# @router.get("/chat-llm-models", response_model=Dict)
# def get_maf_models():
#     return get_models()
