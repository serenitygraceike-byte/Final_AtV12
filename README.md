# SEO Agent — Генератор заголовков из статьи

Агент, который на основе статьи по URL генерирует 5 цепляющих SEO-заголовков с помощью LLM.

## 📋 Требования

- Python ≥ 3.10
- Ключ OpenAI в файле `.env`

## 📦 Установка

```bash
pip install -r requirements.txt
```

## ⚙️ Настройка

Создайте файл `.env` в корне проекта:

```env
OPENAI_API_KEY=your_api_key_here
BASE_URL=https://api.proxyapi.ru/openai/v1
```

## 🚀 Использование

### Как скрипт

```bash
python agent.py https://example.com/article
```

### Как модуль

```python
from agent import generate_seo_titles

titles = generate_seo_titles("https://example.com/article")
for title in titles:
    print(title)
```

### Через API (FastAPI)

```bash
uvicorn app.main:app --reload
```

Документация: http://localhost:8000/docs

## 🏗 Логика работы

1. Загружает HTML по ссылке, извлекает текст с помощью BeautifulSoup.
2. Создаёт системный промпт: «Ты SEO-редактор. Придумай 5 заголовков…»
3. Отправляет текст статьи в LLM с этим промптом.
4. Возвращает массив из 5 заголовков.
5. При сбоях — до 3 повторных попыток (tenacity).

## 📁 Структура проекта

```
project/
├── agent.py            # Основной агент
├── openai_module.py    # Модуль для работы с OpenAI
├── requirements.txt    # Зависимости
├── .env                # API ключи
├── app/                # FastAPI бэкенд
│   ├── main.py
│   ├── routers/
│   └── services/
└── README.md
```

## 🛡 Требования

- **PEP8** + типизация (mypy)
- **Зависимости**: openai, requests, beautifulsoup4, dotenv, tenacity
- **Python ≥ 3.10**
- **Ключ OpenAI** хранится в `.env`

## 🧪 Приёмка

- `python agent.py <url>` возвращает список заголовков
- Ошибки обрабатываются корректно
- Результат логично соотносится с содержанием статьи
