"""Pydantic модели для ответов API Яндекс.Спеллера."""

from enum import IntEnum
from pydantic import BaseModel, Field
from typing import List


class SpellerOptions(IntEnum):
    """
    Опции Яндекс.Спеллера для управления проверкой.

    Можно комбинировать через побитовое ИЛИ (`|`).
    Например: `SpellerOptions.IGNORE_URLS | SpellerOptions.IGNORE_DIGITS`.

    Attributes:
        IGNORE_DIGITS: Пропускать слова с цифрами (например, "R2D2").
        IGNORE_URLS: Пропускать интернет-адреса, email.
        FIND_REPEAT_WORDS: Находить повторяющиеся подряд слова.
        IGNORE_CAPITALIZATION: Игнорировать неверное использование заглавных букв.
    """

    IGNORE_DIGITS = 2
    IGNORE_URLS = 4
    FIND_REPEAT_WORDS = 8
    IGNORE_CAPITALIZATION = 512


class SpellResult(BaseModel):
    """
    Информация об одной найденной орфографической ошибке.

    Attributes:
        code: Код ошибки (1 – нет в словаре, 2 – повтор, 3 – заглавные и т.д.).
        pos: Позиция слова в тексте (в символах, начиная с 0).
        row: Номер строки (начиная с 0).
        col: Номер символа в строке (начиная с 0).
        length: Длина ошибочного слова.
        word: Само ошибочное слово.
        suggestions: Список вариантов исправления (может быть пустым).
    """

    code: int = Field(..., description="Код ошибки")
    pos: int = Field(..., description="Позиция слова в тексте (в символах)")
    row: int = Field(..., description="Номер строки")
    col: int = Field(..., description="Номер колонки (символа в строке)")
    length: int = Field(..., alias="len", description="Длина ошибочного слова")
    word: str = Field(..., description="Само слово")
    suggestions: List[str] = Field(
        default_factory=list, alias="s", description="Варианты исправления"
    )

    class Config:
        populate_by_name = True


class CheckTextResponse(BaseModel):
    """
    Ответ API для проверки одного фрагмента текста.

    Attributes:
        errors: Список найденных ошибок.
        original_text: Исходный проверенный текст (только для внутреннего использования).
    """

    errors: List[SpellResult] = Field(
        default_factory=list, description="Список найденных ошибок"
    )
    original_text: str = Field(default="", exclude=True)


class CheckTextsResponse(BaseModel):
    """
    Ответ API для проверки нескольких фрагментов текста (checkTexts).

    Attributes:
        results: Список результатов проверки для каждого отправленного текста.
    """

    results: List[CheckTextResponse] = Field(
        default_factory=list, description="Результаты проверки для каждого текста"
    )