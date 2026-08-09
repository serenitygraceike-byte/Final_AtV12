import os
import json

from dotenv import load_dotenv
from openai import OpenAI

# Загружаем переменные окружения из .env файла
load_dotenv()


class LLMClient:
    """Клиент для общения с LLM через Proxy API."""

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        model: str = "gpt-4o-mini",
    ):
        """
        Инициализация клиента.

        Args:
            base_url: URL прокси API. Если не передан, берётся из BASE_URL env.
            api_key: API ключ. Если не передан, берётся из OPENAI_API_KEY env.
            model: Модель LLM по умолчанию — gpt-4o-mini.
        """
        self.base_url = base_url or os.getenv("BASE_URL")
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")

        if not self.base_url:
            raise ValueError(
                "base_url не указан: передайте в конструктор или задайте BASE_URL в env."
            )
        if not self.api_key:
            raise ValueError(
                "api_key не указан: передайте в конструктор или задайте OPENAI_API_KEY в env."
            )

        self.model = model
        self.system_prompt: str | None = None
        self.max_tokens: int = 1024

        self._client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
        )

    def chat(self, prompt: str) -> str:
        """
        Простой запрос к LLM.

        Args:
            prompt: Текст пользовательского сообщения.

        Returns:
            Ответ от LLM в виде строки.
        """
        return self.chat_with_system(
            system_prompt=self.system_prompt,
            user_prompt=prompt,
        )

    def chat_with_system(self, system_prompt: str | None, user_prompt: str) -> str:
        """
        Запрос с системным промптом.

        Args:
            system_prompt: Системное сообщение (если None, используется self.system_prompt).
            user_prompt: Текст пользовательского сообщения.

        Returns:
            Ответ от LLM в виде строки.
        """
        messages = []

        effective_system = system_prompt if system_prompt is not None else self.system_prompt
        if effective_system is not None:
            messages.append({"role": "system", "content": effective_system})

        messages.append({"role": "user", "content": user_prompt})

        response = self._client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=self.max_tokens,
        )

        return response.choices[0].message.content or ""

    def chat_json(self, system_prompt: str | None, user_prompt: str) -> dict:
        """
        Запрос со структурированным ответом (JSON).

        Args:
            system_prompt: Системное сообщение (если None, используется self.system_prompt).
            user_prompt: Текст пользовательского сообщения.

        Returns:
            Ответ от LLM, распаршенный как Python-словарь (dict).
        """
        messages = []

        effective_system = system_prompt if system_prompt is not None else self.system_prompt
        if effective_system is not None:
            messages.append({"role": "system", "content": effective_system})

        messages.append({"role": "user", "content": user_prompt})

        response = self._client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=self.max_tokens,
        )

        raw_text = response.choices[0].message.content or ""
        return json.loads(raw_text)


if __name__ == "__main__":
    import traceback

    client = LLMClient()

    # Тест 1: Простой чат
    print("=" * 60)
    print("Тест 1: chat() — простой запрос")
    print("=" * 60)
    try:
        result = client.chat("Сколько будет 2 + 2? Ответь одним числом.")
        print(f"Ответ: {result}")
    except Exception as e:
        print(f"Ошибка: {e}")
        traceback.print_exc()

    # Тест 2: Чат с системным промптом
    print("\n" + "=" * 60)
    print("Тест 2: chat_with_system() — запрос с системным промптом")
    print("=" * 60)
    try:
        result = client.chat_with_system(
            system_prompt="Ты краткий помощник. Отвечай только фактами.",
            user_prompt="Кто написал 'Преступление и наказание'?",
        )
        print(f"Ответ: {result}")
    except Exception as e:
        print(f"Ошибка: {e}")
        traceback.print_exc()

    # Тест 3: JSON-ответ
    print("\n" + "=" * 60)
    print("Тест 3: chat_json() — запрос со структурированным ответом")
    print("=" * 60)
    try:
        result = client.chat_json(
            system_prompt="Отвечай только в формате JSON без дополнительных полей.",
            user_prompt="Опиши город Москва: название, население, страна.",
        )
        print(f"Ответ: {json.dumps(result, ensure_ascii=False, indent=2)}")
    except Exception as e:
        print(f"Ошибка: {e}")
        traceback.print_exc()
