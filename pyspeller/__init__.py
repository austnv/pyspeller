"""
# pyspeller

---

Библиотека для работы с API Яндекс.Спеллера.

Предоставляет синхронные и асинхронные клиенты, а также функции-помощники.

## Quick start:

    from pyspeller import check_text, SpellerOptions
    result = check_text("Превед, медвед!")
    print(result.errors[0].suggestions)  # ['Привет']
"""

from .client import YandexSpeller, AsyncYandexSpeller
from .exceptions import SpellerError, SpellerAPIError, SpellerNetworkError
from .types import SpellResult, CheckTextResponse, CheckTextsResponse, SpellerOptions


IGNORE_DIGITS = 2
IGNORE_URLS = 4
FIND_REPEAT_WORDS = 8
IGNORE_CAPITALIZATION = 512


def check_text(
    text: str,
    lang: str = "ru,en",
    options: int | SpellerOptions = 0,
    format: str = "plain",
) -> CheckTextResponse:
    """
    Быстрая синхронная проверка одного текста.

    Создаёт экземпляр YandexSpeller, выполняет запрос и сразу возвращает результат.
    Сессия автоматически закрывается.

    Args:
        text: Текст для проверки.
        lang: Коды языков через запятую (`"ru"`, `"en"`, `"uk"`). По умолчанию `"ru,en"`.
        options: Опции проверки. Можно передать int или комбинацию SpellerOptions.
            Например: `SpellerOptions.IGNORE_URLS | SpellerOptions.FIND_REPEAT_WORDS`.
            По умолчанию 0 (все опции выключены).
        format: Формат текста: `"plain"` (по умолчанию) или `"html"`.

    Returns:
        CheckTextResponse со списком найденных ошибок.

    Raises:
        SpellerAPIError: При ошибке API.
        SpellerNetworkError: При сетевой ошибке.

    Example:
        >>> from pyspeller import check_text
        >>> result = check_text("очепятка")
        >>> result.errors[0].suggestions
        ['опечатка']
    """
    speller = YandexSpeller(lang=lang, options=options, format=format)
    return speller.check_text(text)


async def async_check_text(
    text: str,
    lang: str = "ru,en",
    options: int | SpellerOptions = 0,
    format: str = "plain",
) -> CheckTextResponse:
    """
    Быстрая асинхронная проверка одного текста.

    Создаёт экземпляр AsyncYandexSpeller, выполняет асинхронный запрос и возвращает результат.
    Сессия автоматически закрывается.

    Args:
        text: Текст для проверки.
        lang: Коды языков (см. check_text).
        options: Опции проверки (см. check_text).
        format: Формат текста (см. check_text).

    Returns:
        CheckTextResponse.

    Raises:
        SpellerAPIError: При ошибке API.
        SpellerNetworkError: При сетевой ошибке.

    Example:
        >>> import asyncio
        >>> from pyspeller import async_check_text
        >>> asyncio.run(async_check_text("ашипка"))
    """
    speller = AsyncYandexSpeller(lang=lang, options=options, format=format)
    return await speller.check_text(text)


def check_texts(
    texts: list[str],
    lang: str = "ru,en",
    options: int | SpellerOptions = 0,
    format: str = "plain",
) -> CheckTextsResponse:
    """
    Быстрая синхронная проверка нескольких текстов (метод checkTexts API).

    Args:
        texts: Список строк для проверки.
        lang: Коды языков (см. check_text).
        options: Опции проверки (см. check_text).
        format: Формат текстов (см. check_text).

    Returns:
        CheckTextsResponse, содержащий для каждого текста свой CheckTextResponse.

    Raises:
        SpellerAPIError: При ошибке API.
        SpellerNetworkError: При сетевой ошибке.

    Example:
        >>> from pyspeller import check_texts
        >>> result = check_texts(["синхрафазатрон", "дубне"])
        >>> for res in result.results:
        ...     for err in res.errors:
        ...         print(err.suggestions)
    """
    speller = YandexSpeller(lang=lang, options=options, format=format)
    return speller.check_texts(texts)


async def async_check_texts(
    texts: list[str],
    lang: str = "ru,en",
    options: int | SpellerOptions = 0,
    format: str = "plain",
) -> CheckTextsResponse:
    """
    Быстрая асинхронная проверка нескольких текстов.

    Args:
        texts: Список строк для проверки.
        lang: Коды языков (см. check_text).
        options: Опции проверки (см. check_text).
        format: Формат текстов (см. check_text).

    Returns:
        CheckTextsResponse.

    Raises:
        SpellerAPIError: При ошибке API.
        SpellerNetworkError: При сетевой ошибке.

    Example:
        >>> import asyncio
        >>> from pyspeller import async_check_texts
        >>> asyncio.run(async_check_texts(["текст1", "текст2"]))
    """
    speller = AsyncYandexSpeller(lang=lang, options=options, format=format)
    return await speller.check_texts(texts)


__all__ = [
    "YandexSpeller",
    "AsyncYandexSpeller",
    "SpellResult",
    "CheckTextResponse",
    "CheckTextsResponse",
    "SpellerOptions",
    "SpellerError",
    "SpellerAPIError",
    "SpellerNetworkError",
    "check_text",
    "async_check_text",
    "check_texts",
    "async_check_texts",
]