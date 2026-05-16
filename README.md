# 🐝 PySpeller

<p align="center">
  <a href="https://pypi.org/project/pyspeller/"><img src="https://img.shields.io/pypi/v/pyspeller?color=blue&label=PyPI&logo=pypi" alt="PyPI version"></a>
  <a href="https://pypi.org/project/pyspeller/"><img src="https://img.shields.io/pypi/pyversions/pyspeller?color=red&label=Python&logo=python" alt="Python versions"></a>
  <a href="https://github.com/austnv/pyspeller/blob/main/LICENSE"><img src="https://img.shields.io/github/license/austnv/pyspeller?color=green" alt="License"></a>
  <a href="https://pypi.org/project/pyspeller/"><img src="https://img.shields.io/pypi/dm/pyspeller?color=purple" alt="Downloads"></a>
  <a href="https://github.com/austnv/pyspeller/stargazers"><img src="https://img.shields.io/github/stars/austnv/pyspeller?style=social" alt="Stars"></a>
</p>

Простая и легковесная библиотека-обёртка для [API Яндекс.Спеллера](https://yandex.ru/dev/speller/). Предоставляет синхронный и асинхронный клиенты, строгую типизацию через Pydantic, и удобные функции-помощники для быстрой проверки текста.

## ✨ Возможности

-   ✅ Проверка одного текста или списка текстов (метод `checkTexts`)
-   ⚡ Синхронный и асинхронный режимы (на базе `httpx`)
-   🎛️ Поддержка всех [опций Яндекс.Спеллера](https://yandex.ru/dev/speller/doc/ru/reference/speller-options) (игнорирование URL, цифр, повторов и т.д.)
-   🧠 Автоматическое управление HTTP-сессиями — создаются и закрываются при каждом вызове, не требуется использовать контекстный менеджер
-   📦 Типизированные модели ответов на основе Pydantic v2
-   🚨 Понятные исключения для ошибок API и сетевых проблем
-   🪶 Минимум зависимостей: только `httpx` и `pydantic`

## 📦 Установка

```bash
pip install pyspeller
```

или с помощью `uv`:

```bash
uv add pyspeller
```

Для работы требуется **Python 3.9** или новее.

## 🚀 Быстрый старт

### Синхронная проверка

```python
from pyspeller import check_text

result = check_text("Превед, медвед!")
if result.errors:
    print(result.errors[0].suggestions)  # ['Привет']
```

### Асинхронная проверка

```python
import asyncio
from pyspeller import async_check_text

async def main():
    res = await async_check_text("синхрафазатрон")
    print(res.errors[0].suggestions)  # ['синхрофазотрон']

asyncio.run(main())
```

### Проверка списка текстов

```python
from pyspeller import check_texts

results = check_texts(["очепятка", "дубне"])
for text_result in results.results:
    for error in text_result.errors:
        print(f"Слово '{error.word}' → {error.suggestions}")
```

## ⚙️ Опции проверки

Все [опции Яндекс.Спеллера](https://yandex.ru/dev/speller/doc/ru/reference/speller-options) доступны через перечисление `SpellerOptions`. Их можно комбинировать с помощью побитового ИЛИ (`|`).

```python
from pyspeller import check_text, SpellerOptions

result = check_text(
    "мой сайт http://example.com и номер R2D2",
    options=SpellerOptions.IGNORE_URLS | SpellerOptions.IGNORE_DIGITS
)

# Или импортировать опции напрямую

from pyspeller import check_text, IGNORE_URLS, IGNORE_DIGITS

result = check_text(
    "мой сайт http://example.com и номер R2D2",
    options=IGNORE_URLS | IGNORE_DIGITS
)
```

### Доступные опции

| Константа                 | Число | Описание                                |
|---------------------------|-------|-----------------------------------------|
| `IGNORE_DIGITS`           | 2     | Пропускать слова с цифрами              |
| `IGNORE_URLS`             | 4     | Пропускать интернет-адреса и e‑mail     |
| `FIND_REPEAT_WORDS`       | 8     | Находить повторяющиеся подряд слова     |
| `IGNORE_CAPITALIZATION`   | 512   | Игнорировать неверное использование заглавных букв |

При необходимости можно передать произвольное целое число.

## 📖 API

### Клиенты

#### `YandexSpeller(lang="ru,en", options=0, format="plain")`

Синхронный клиент.

**Методы:**

-   `check_text(text: str) -> CheckTextResponse`
-   `check_texts(texts: List[str]) -> CheckTextsResponse`

#### `AsyncYandexSpeller(lang="ru,en", options=0, format="plain")`

Асинхронный клиент. Методы аналогичны синхронному, но возвращают корутины.

### Удобные функции

```python
# Синхронные
check_text(text, lang="ru,en", options=0, format="plain") -> CheckTextResponse
check_texts(texts, ...) -> CheckTextsResponse

# Асинхронные
async_check_text(text, ...) -> CheckTextResponse
async_check_texts(texts, ...) -> CheckTextsResponse
```

Все функции автоматически создают и закрывают сессию, поэтому их можно вызывать без дополнительного управления.

### Модели данных

#### `SpellResult` — одна найденная ошибка

| Поле         | Тип        | Описание                                     |
|--------------|------------|----------------------------------------------|
| `code`       | `int`      | Код ошибки (1 – нет в словаре, 3 – регистр) |
| `pos`        | `int`      | Позиция слова в тексте (символы)            |
| `row`        | `int`      | Номер строки                                 |
| `col`        | `int`      | Номер символа в строке                       |
| `length`     | `int`      | Длина ошибочного слова                       |
| `word`       | `str`      | Само слово                                   |
| `suggestions`| `List[str]`| Варианты исправления                         |

#### `CheckTextResponse` — результат проверки одного текста

-   `errors: List[SpellResult]`

#### `CheckTextsResponse` — результат проверки нескольких текстов

-   `results: List[CheckTextResponse]`

### Исключения

Все исключения наследуются от `SpellerError`.

-   `SpellerAPIError(status_code: int, message: str)` – ошибка API (HTTP 4xx/5xx).
-   `SpellerNetworkError(original_exception: Exception)` – сетевая ошибка (таймаут, DNS и т.п.).

## 🛠️ Разработка

```bash
git clone https://github.com/austnv/pyspeller.git
cd pyspeller
uv sync --group dev
uv run pytest tests/ -v
```

## 📄 Лицензия

Проект распространяется под лицензией MIT. Подробнее см. в файле [LICENSE](LICENSE).

---

Сделано с ❤️ для проверки орфографии через Яндекс.Спеллер.