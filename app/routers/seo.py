"""Роутер для SEO-агента."""

from fastapi import APIRouter, Body
from pydantic import BaseModel

from agent import generate_seo_titles

router = APIRouter(prefix="/seo", tags=["SEO Agent"])


class SeoRequest(BaseModel):
    url: str


@router.post("/generate-titles")
async def generate_titles(request: SeoRequest = Body(...)) -> dict:
    """
    Генерирует 5 SEO-заголовков на основе статьи по URL.
    
    Args:
        url: URL статьи для анализа.
    
    Returns:
        Список заголовков.
    """
    try:
        titles = generate_seo_titles(request.url)
        return {
            "success": True,
            "titles": titles,
            "count": len(titles),
            "error": None,
        }
    except ValueError as e:
        return {
            "success": False,
            "titles": [],
            "count": 0,
            "error": str(e),
        }
    except Exception as e:
        return {
            "success": False,
            "titles": [],
            "count": 0,
            "error": f"Ошибка: {e}",
        }
