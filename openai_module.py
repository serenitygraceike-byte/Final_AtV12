"""Модуль для работы с OpenAI LLM."""

import os
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

load_dotenv()


class OpenAIModule:
    """Клиент для общения с OpenAI-совместимым API с повторами при сбоях."""

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        model: str = "gpt-4o",
    ) -> None:
        """
        Инициализация клиента.

        Args:
            base_url: URL прокси API. Если не передан, берётся из BASE_URL env.
            api_key: API ключ. Если не передан, берётся из OPENAI_API_KEY env.
            model: Модель LLM по умолчанию — gpt-4o.
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
        self._client = OpenAI(
            base_url=self.base_url,
            api_key=self.api_key,
        )

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((Exception,)),
    )
    def chat(
        self, system_prompt: str, user_prompt: str
    ) -> str:
        """
        Отправить запрос к LLM с повторами при сбоях (до 3 раз).

        Args:
            system_prompt: Системное сообщение.
            user_prompt: Сообщение пользователя.

        Returns:
            Ответ от LLM в виде строки.
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        response = self._client.chat.completions.create(
            model=self.model,
            messages=messages,
            max_tokens=1024,
        )

        return response.choices[0].message.content or ""
