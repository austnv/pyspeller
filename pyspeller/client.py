"""Синхронный и асинхронный клиенты для Яндекс.Спеллера."""

from typing import List, Union
import httpx
from .types import CheckTextResponse, CheckTextsResponse, SpellerOptions, SpellResult
from .exceptions import SpellerAPIError, SpellerNetworkError


class BaseSpeller:
    """
    Базовая логика для построения запросов и парсинга ответов.

    Не предназначен для прямого использования.
    """

    BASE_URL = "https://speller.yandex.net/services/spellservice.json"
    CHECK_TEXT_URL = f"{BASE_URL}/checkText"
    CHECK_TEXTS_URL = f"{BASE_URL}/checkTexts"

    def __init__(
        self,
        lang: str = "ru,en",
        options: Union[int, SpellerOptions] = 0,
        format: str = "plain",
    ):
        """
        Инициализация базового клиента.

        Args:
            lang: Список языков проверки через запятую.
                Допустимые коды: `"ru"` (русский), `"en"` (английский), `"uk"` (украинский).
                По умолчанию `"ru,en"`.
            options: Комбинация опций проверки (см. `SpellerOptions`).
                Можно передавать целое число или использовать enum с побитовым ИЛИ.
                По умолчанию 0 (все опции выключены).
            format: Формат проверяемого текста.
                `"plain"` – без разметки (по умолчанию), `"html"` – HTML-разметка.
        """
        self.lang = lang
        self.options = int(options)
        self.format = format

    def _build_params(self, text: Union[str, List[str]]) -> dict:
        """Внутренний метод сборки параметров запроса."""
        if isinstance(text, list):
            params = {
                "text": text,
                "lang": self.lang,
                "options": self.options,
                "format": self.format,
            }
        else:
            params = {
                "text": text,
                "lang": self.lang,
                "options": self.options,
                "format": self.format,
            }
        return params

    def _parse_response(self, data: list, original_text: str) -> CheckTextResponse:
        """Парсинг ответа для checkText."""
        errors = [SpellResult.model_validate(item) for item in data]
        return CheckTextResponse(errors=errors, original_text=original_text)

    def _parse_checktexts_response(self, data: list, original_texts: List[str]) -> CheckTextsResponse:
        """Парсинг ответа для checkTexts."""
        results = []
        for i, item in enumerate(data):
            errors = [SpellResult.model_validate(error) for error in item]
            results.append(CheckTextResponse(errors=errors, original_text=original_texts[i]))
        return CheckTextsResponse(results=results)


class YandexSpeller(BaseSpeller):
    """
    Синхронный клиент для Яндекс.Спеллера.

    Каждый вызов метода создаёт и сразу закрывает HTTP-сессию.
    Не требует использования контекстного менеджера.

    Example:
        speller = YandexSpeller(lang="ru", options=SpellerOptions.FIND_REPEAT_WORDS)
        result = speller.check_text("мама мама мыла раму")
    """

    def check_text(self, text: str) -> CheckTextResponse:
        """
        Проверить один фрагмент текста на орфографические ошибки.

        Args:
            text: Текст для проверки (строка в формате plain или HTML).

        Returns:
            CheckTextResponse со списком найденных ошибок.

        Raises:
            SpellerAPIError: При ошибке API (HTTP 4xx/5xx).
            SpellerNetworkError: При сетевой ошибке.

        Example:
            ```
            speller = YandexSpeller()
            result = speller.check_text("Привет, мир!")
            for err in result.errors:
                print(err.word, err.suggestions)
            ```
        """
        params = self._build_params(text)
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(self.CHECK_TEXT_URL, params=params)
                response.raise_for_status()
                data = response.json()
            return self._parse_response(data, text)
        except httpx.HTTPStatusError as e:
            raise SpellerAPIError(
                status_code=e.response.status_code,
                message=e.response.text,
            ) from e
        except httpx.RequestError as e:
            raise SpellerNetworkError(e) from e

    def check_texts(self, texts: List[str]) -> CheckTextsResponse:
        """
        Проверить список текстов (метод checkTexts API).

        Args:
            texts: Список строк для проверки.

        Returns:
            CheckTextsResponse, содержащий для каждого текста свой CheckTextResponse.

        Raises:
            SpellerAPIError: При ошибке API.
            SpellerNetworkError: При сетевой ошибке.

        Example:
            ```
            speller = YandexSpeller()
            result = speller.check_texts(["синхрафазатрон", "дубне"])
            for res in result.results:
                for err in res.errors:
                    print(err.suggestions)
            ```
        """
        params = self._build_params(texts)
        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.get(self.CHECK_TEXTS_URL, params=params)
                response.raise_for_status()
                data = response.json()
            return self._parse_checktexts_response(data, texts)
        except httpx.HTTPStatusError as e:
            raise SpellerAPIError(
                status_code=e.response.status_code,
                message=e.response.text,
            ) from e
        except httpx.RequestError as e:
            raise SpellerNetworkError(e) from e


class AsyncYandexSpeller(BaseSpeller):
    """
    Асинхронный клиент для Яндекс.Спеллера.

    Каждый вызов метода создаёт и сразу закрывает асинхронную HTTP-сессию.
    Не требует использования контекстного менеджера.

    Example:
        ```
        speller = AsyncYandexSpeller()
        result = await speller.check_text("Привет!")
        ```
    """

    async def check_text(self, text: str) -> CheckTextResponse:
        """
        Асинхронно проверить один фрагмент текста.

        Args:
            text: Текст для проверки.

        Returns:
            CheckTextResponse со списком ошибок.

        Raises:
            SpellerAPIError: При ошибке API.
            SpellerNetworkError: При сетевой ошибке.

        Example:
            ```
            speller = AsyncYandexSpeller()
            result = await speller.check_text("Превед")
            print(result.errors[0].suggestions)
            ```
        """
        params = self._build_params(text)
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(self.CHECK_TEXT_URL, params=params)
                response.raise_for_status()
                data = response.json()
            return self._parse_response(data, text)
        except httpx.HTTPStatusError as e:
            raise SpellerAPIError(
                status_code=e.response.status_code,
                message=e.response.text,
            ) from e
        except httpx.RequestError as e:
            raise SpellerNetworkError(e) from e

    async def check_texts(self, texts: List[str]) -> CheckTextsResponse:
        """
        Асинхронно проверить список текстов.

        Args:
            texts: Список строк для проверки.

        Returns:
            CheckTextsResponse с результатами для каждого текста.

        Raises:
            SpellerAPIError: При ошибке API.
            SpellerNetworkError: При сетевой ошибке.

        Example:
            ```
            speller = AsyncYandexSpeller()
            result = await speller.check_texts(["текст1", "текст2"])
            for res in result.results:
                print(len(res.errors))
            ```
        """
        params = self._build_params(texts)
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(self.CHECK_TEXTS_URL, params=params)
                response.raise_for_status()
                data = response.json()
            return self._parse_checktexts_response(data, texts)
        except httpx.HTTPStatusError as e:
            raise SpellerAPIError(
                status_code=e.response.status_code,
                message=e.response.text,
            ) from e
        except httpx.RequestError as e:
            raise SpellerNetworkError(e) from e