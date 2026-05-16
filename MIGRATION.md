# 🔄 Миграция с PySpeller v1.x на v2.0.0

PySpeller v2.0.0 — это полная переработка библиотеки, направленная на современный Python, строгую типизацию и поддержку асинхронности. К сожалению, эти улучшения **требуют изменений в вашем коде**. Данное руководство поможет быстро и безболезненно адаптировать ваш проект к новой версии.

## 📋 Содержание

- [Зачем обновляться?](#-зачем-обновляться)
- [Ключевые различия](#-ключевые-различия)
- [Пошаговая миграция](#-пошаговая-миграция)
  - [1. Зависимости и установка](#1-зависимости-и-установка)
  - [2. Импорты](#2-импорты)
  - [3. Передача опций](#3-передача-опций)
  - [4. Обработка ответов](#4-обработка-ответов)
  - [5. Асинхронный код](#5-асинхронный-код)
  - [6. Обработка ошибок](#6-обработка-ошибок)
  - [7. Передача аргументов](#7-передача-аргументов)
- [Полный пример «до и после»](#-полный-пример-до-и-после)
- [Часто задаваемые вопросы](#-часто-задаваемые-вопросы)

---

## ✨ Зачем обновляться?

| Преимущество | v1.x | v2.0.0 |
|-------------|------|--------|
| Типизация | `dict` / `list` без подсказок | Строгие Pydantic-модели |
| Асинхронность | ❌ Нет | ✅ `asyncio` из коробки |
| HTTP-клиент | Устаревшая stdlib | Современный `httpx` |
| IDE-поддержка | Никакой | Автодополнение, проверка типов |
| Исключения | Разные `Exception` | Понятные `SpellerAPIError`, `SpellerNetworkError` |
| Поддержка Python | Только 3.12 | 3.9+ |

---

## 🔍 Ключевые различия

### Зависимости
- **v1.x:** Только стандартная библиотека Python
- **v2.x:** `httpx >= 0.24.0`, `pydantic >= 2.0.0`

### Структура пакета
- **v1.x:** Один файл `pyspeller.py`
- **v2.x:** Полноценный пакет (`client.py`, `types.py`, `exceptions.py`)

### Опции проверки
- **v1.x:** Список строк: `['IGNORE_URLS', 'IGNORE_DIGITS']`
- **v2.x:** Enum или целое число: `SpellerOptions.IGNORE_URLS | SpellerOptions.IGNORE_DIGITS`

### Ответы API
- **v1.x:** Словари и списки словарей
- **v2.x:** Объекты `CheckTextResponse`, `CheckTextsResponse`, `SpellResult`

---

## 🚶 Пошаговая миграция

### 1. Зависимости и установка

Установите новую версию и обновите файл зависимостей вашего проекта:

```bash
pip install "pyspeller>=2.0.0"
```

**`requirements.txt`:**
```diff
- pyspeller==1.0.0
+ pyspeller>=2.0.0
```

**`pyproject.toml`:**
```diff
- "pyspeller==1.0.0"
+ "pyspeller>=2.0.0"
```

---

### 2. Импорты

Замените неявный импорт на явный:

```diff
- from pyspeller import *
+ from pyspeller import check_text, check_texts, SpellerOptions, SpellerAPIError
```

**Основные импорты, которые могут понадобиться:**

```python
from pyspeller import (
    check_text,          # синхронная проверка одного текста
    check_texts,         # синхронная проверка списка текстов
    async_check_text,    # асинхронная проверка одного текста
    async_check_texts,   # асинхронная проверка списка текстов
    YandexSpeller,       # синхронный клиент (для тонкой настройки)
    AsyncYandexSpeller,  # асинхронный клиент
    SpellerOptions,      # enum опций проверки
    SpellerAPIError,     # исключение ошибки API
    SpellerNetworkError, # исключение сетевой ошибки
)
```

---

### 3. Передача опций

Опции больше не передаются как список строк. Используйте `SpellerOptions` или целое число.

```diff
- result = check_text('масква', 'ru', 'plain', ['IGNORE_URLS', 'IGNORE_DIGITS'])
+ result = check_text('масква', lang='ru', options=SpellerOptions.IGNORE_URLS | SpellerOptions.IGNORE_DIGITS)
```

**Все доступные опции:**

```python
from pyspeller import SpellerOptions

SpellerOptions.IGNORE_DIGITS         # = 2
SpellerOptions.IGNORE_URLS           # = 4
SpellerOptions.FIND_REPEAT_WORDS     # = 8
SpellerOptions.IGNORE_CAPITALIZATION # = 512
```

**Комбинирование нескольких опций:**

```python
# Enum (рекомендуется)
options = SpellerOptions.IGNORE_URLS | SpellerOptions.IGNORE_DIGITS

# Целое число (тоже работает)
options = 6  # 2 (IGNORE_DIGITS) + 4 (IGNORE_URLS)

# Без опций
options = 0  # или просто не передавайте параметр
```

**Таблица перехода:**

| v1.x строка | v2.x enum | Числовое значение |
|------------|-----------|------------------|
| `'IGNORE_DIGITS'` | `SpellerOptions.IGNORE_DIGITS` | `2` |
| `'IGNORE_URLS'` | `SpellerOptions.IGNORE_URLS` | `4` |
| `'FIND_REPEAT_WORDS'` | `SpellerOptions.FIND_REPEAT_WORDS` | `8` |
| `'IGNORE_CAPITALIZATION'` | `SpellerOptions.IGNORE_CAPITALIZATION` | `512` |

---

### 4. Обработка ответов

Ответы теперь являются **объектами**, а не словарями. Доступ к данным — через атрибуты с точкой.

```diff
- result = check_text('масква')
- if result:  # проверка на пустоту
-     for error in result:
-         print(error['word'], error['s'])
+ result = check_text('масква')
+ for error in result.errors:
+     print(error.word, error.suggestions)
```

**Структура объекта `SpellResult` (одна ошибка):**

```python
error.code        # int:   код ошибки (1, 2, 3, ...)
error.pos         # int:   позиция в тексте
error.row         # int:   номер строки
error.col         # int:   номер колонки
error.length      # int:   длина слова
error.word        # str:   ошибочное слово
error.suggestions # List[str]: варианты исправления
```

**Структура `CheckTextResponse`:**

```python
result.errors     # List[SpellResult]: список ошибок
```

**Структура `CheckTextsResponse` (для `check_texts`):**

```python
result.results    # List[CheckTextResponse]: по одному на каждый текст
```

**Пример итерации по всем результатам:**

```python
# v1.x: работа со словарями
results = check_texts(['текст1', 'текст2'])
for i, error_list in enumerate(results):
    for err in error_list:
        print(f"Текст {i}: {err['word']} → {err['s']}")

# v2.x: работа с объектами
results = check_texts(['текст1', 'текст2'])
for i, text_result in enumerate(results.results):
    for err in text_result.errors:
        print(f"Текст {i}: {err.word} → {err.suggestions}")
```

---

### 5. Асинхронный код

Если ваш проект использует `asyncio`, вы можете заменить синхронные вызовы на асинхронные:

```python
# v1.x: только синхронно
import requests

async def my_handler():
    # Приходилось использовать run_in_executor или синхронный код
    result = check_text('масква')
    print(result)
```

```python
# v2.x: нативная асинхронность
import asyncio
from pyspeller import async_check_text, async_check_texts

async def my_handler():
    # Прямой асинхронный вызов
    result = await async_check_text('масква')
    for err in result.errors:
        print(err.word, err.suggestions)

    # Асинхронная проверка списка
    results = await async_check_texts(['текст1', 'текст2'])

asyncio.run(my_handler())
```

**Клиенты (для тонкой настройки):**

```python
# Синхронный
from pyspeller import YandexSpeller

speller = YandexSpeller(lang='ru', options=SpellerOptions.IGNORE_URLS)
result = speller.check_text('текст')
results = speller.check_texts(['текст1', 'текст2'])
```

```python
# Асинхронный
from pyspeller import AsyncYandexSpeller

async def main():
    speller = AsyncYandexSpeller(lang='ru')
    result = await speller.check_text('текст')
    results = await speller.check_texts(['текст1', 'текст2'])

asyncio.run(main())
```

---

### 6. Обработка ошибок

v2.0.0 предоставляет специализированные исключения вместо стандартных.

```diff
- try:
-     result = check_text('текст')
- except Exception as e:
-     print(f"Ошибка: {e}")
+ from pyspeller import SpellerAPIError, SpellerNetworkError
+
+ try:
+     result = check_text('текст')
+ except SpellerAPIError as e:
+     print(f"Ошибка API {e.status_code}: {e.message}")
+ except SpellerNetworkError as e:
+     print(f"Сетевая ошибка: {e.original_exception}")
```

**Иерархия исключений:**

```
SpellerError (базовое)
├── SpellerAPIError (HTTP 4xx/5xx)
│   ├── .status_code: int
│   └── .message: str
└── SpellerNetworkError (таймаут, DNS и т.п.)
    └── .original_exception: Exception
```

---

### 7. Передача аргументов

Все параметры, кроме `text`/`texts`, стали **именованными**:

```diff
# v1.x: позиционные аргументы
- check_text('масква', 'ru', 'plain', ['IGNORE_URLS'])
- check_texts(['текст1', 'текст2'], 'ru', 'plain', [])

# v2.x: именованные аргументы
+ check_text('масква', lang='ru', format='plain', options=SpellerOptions.IGNORE_URLS)
+ check_texts(['текст1', 'текст2'], lang='ru')
```

**Значения по умолчанию (можно не указывать):**

| Параметр | По умолчанию |
|----------|-------------|
| `lang` | `"ru,en"` |
| `format` | `"plain"` |
| `options` | `0` |

---

## 📝 Полный пример «до и после»

### v1.0.0

```python
from pyspeller import check_text, check_texts

# Проверка одного текста
result = check_text('масква', 'ru', 'plain', ['IGNORE_URLS'])
if result:
    for error in result:
        print(f"Ошибка в слове '{error['word']}': {error['s']}")

# Проверка списка текстов
texts = ['синхрафазатрон', 'олексей']
results = check_texts(texts, 'ru', 'plain', ['FIND_REPEAT_WORDS'])

for i, text_errors in enumerate(results):
    print(f"\nТекст #{i+1}:")
    for err in text_errors:
        suggestions = ', '.join(err['s']) if err['s'] else 'нет предложений'
        print(f"  Слово: {err['word']} → {suggestions}")
```

### v2.0.0

```python
from pyspeller import (
    check_text,
    check_texts,
    SpellerOptions,
    SpellerAPIError,
    SpellerNetworkError,
)

# Проверка одного текста
try:
    result = check_text(
        'масква',
        lang='ru',
        options=SpellerOptions.IGNORE_URLS
    )
    for error in result.errors:
        suggestions = error.suggestions if error.suggestions else ['нет предложений']
        print(f"Ошибка в слове '{error.word}': {', '.join(suggestions)}")
except SpellerAPIError as e:
    print(f"Ошибка API: {e}")
except SpellerNetworkError as e:
    print(f"Сетевая ошибка: {e}")

# Проверка списка текстов
texts = ['синхрафазатрон', 'олексей']
results = check_texts(
    texts,
    lang='ru',
    options=SpellerOptions.FIND_REPEAT_WORDS
)

for i, text_result in enumerate(results.results):
    print(f"\nТекст #{i+1}:")
    for err in text_result.errors:
        suggestions = ', '.join(err.suggestions) if err.suggestions else 'нет предложений'
        print(f"  Слово: {err.word} → {suggestions}")
```

---

## ❓ Часто задаваемые вопросы

**Q: Могу ли я использовать v1.x и v2.x одновременно?**

A: Нет, это разные мажорные версии. Установите нужную: `pip install "pyspeller<2.0.0"` (v1.x) или `pip install "pyspeller>=2.0.0"` (v2.x).

**Q: Почему убрали контекстный менеджер для клиента?**

A: Для простоты использования. Каждый вызов метода создаёт и закрывает сессию автоматически. Вам не нужно управлять жизненным циклом клиента.

**Q: Поддерживает ли v2.0.0 Python 3.13+?**

A: Да, библиотека проверена на Python 3.9–3.12 и должна работать на всех более новых версиях.

**Q: Изменилось ли поведение API Яндекс.Спеллера?**

A: Нет, изменилась только обёртка. Само API Спеллера осталось прежним.

**Q: Где сообщить о проблемах?**

A: Создайте issue в [репозитории на GitHub](https://github.com/austnv/pyspeller/issues).

---

**Удачной миграции!** Если у вас возникли трудности, не стесняйтесь открыть [issue](https://github.com/austnv/pyspeller/issues) — мы поможем.