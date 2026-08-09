"""SEO-агент: генерирует 5 цепляющих заголовков на основе статьи по URL."""

import re
from typing import List

import requests
from bs4 import BeautifulSoup
from openai_module import OpenAIModule


SYSTEM_PROMPT = (
    "Ты SEO-редактор. Придумай 5 цепляющих SEO-заголовков для статьи ниже. "
    "Каждый заголовок должен быть не более 70 символов. "
    "Отвечай только списком из 5 заголовков, каждый с новой строки, без нумерации и кавычек."
)


def extract_text_from_url(url: str) -> str:
    """
    Загружает HTML по ссылке и извлекает текст с помощью BeautifulSoup.

    Args:
        url: URL статьи.

    Returns:
        Извлечённый текст статьи.

    Raises:
        requests.exceptions.RequestException: При ошибке загрузки.
    """
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Удаляем скрипты и стили
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()

    # Извлекаем текст из <p> и <h> тегов
    text_parts: List[str] = []
    for tag in soup.find_all(["p", "h1", "h2", "h3", "h4", "h5", "h6"]):
        text = tag.get_text(strip=True)
        if text:
            text_parts.append(text)

    return "\n\n".join(text_parts)


def generate_seo_titles(url: str, model: str = "gpt-4o") -> List[str]:
    """
    Генерирует 5 SEO-заголовков на основе статьи по URL.

    Args:
        url: URL статьи.
        model: Модель OpenAI (gpt-4o или gpt-3.5-turbo).

    Returns:
        Список из 5 заголовков.
    """
    # 1. Загружаем и извлекаем текст
    text = extract_text_from_url(url)

    if not text.strip():
        raise ValueError(f"Не удалось извлечь текст из статьи: {url}")

    # Обрезаем текст, если он слишком длинный (лимит токенов)
    max_chars = 6000
    if len(text) > max_chars:
        text = text[:max_chars] + "\n... [текст обрезан]"

    # 2. Создаём клиент и отправляем запрос
    client = OpenAIModule(model=model)

    result = client.chat(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=f"Проанализируй статью ниже и придумай 5 SEO-заголовков:\n\n{text}",
    )

    # 3. Парсим результат — извлекаем 5 заголовков
    titles = [
        line.strip()
        for line in result.strip().splitlines()
        if line.strip() and re.match(r"^\d+[\.\)\-]?\s*", line.strip()) is None
    ]

    # Ограничиваем до 5 заголовков
    titles = titles[:5]

    # Если заголовков меньше 5 — возвращаем что есть
    return titles


if __name__ == "__main__":
    import sys

    # Пример использования: python agent.py <url>
    if len(sys.argv) < 2:
        url = "https://example.com"
        print(f"URL не указан. Используется демо-URL: {url}")
    else:
        url = sys.argv[1]

    print(f"Анализ статьи: {url}\n")
    print("Генерация заголовков...")

    try:
        titles = generate_seo_titles(url)
        print(f"\n✅ Сгенерировано {len(titles)} заголовков:\n")
        for i, title in enumerate(titles, 1):
            print(f"  {i}. {title}")
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        sys.exit(1)
