"""
# pyspeller

Библиотека для проверки орфографии текста с помощью [API Яндекс.Спеллер](https://yandex.ru/dev/speller/). Содержит два метода: `check_text` и `check_texts`.

Методы проверяют орфографию в указанном отрывке текста. Демонстрация работы метода `check_text` находится [здесь](https://speller.yandex.net/services/spellservice?op=checkText). Документация API находится [здесь](https://yandex.ru/dev/speller/doc/ru/).

## Описание параметров метода `check_text`:

- `query` — Строка поискового запроса.
- `lang` — Язык проверки орфографии (по умолчанию `ru,en`). Доступны `en`, `uk`, `ru`.
- `format_text` — Формат текста (по умолчанию `plain`). Доступны `plain`, `html`.
- `options` — Дополнительные опции проверки орфографии (по умолчанию `None`). Доступны `IGNORE_DIGITS`, `IGNORE_URLS`, `FIND_REPEAT_WORDS`, `IGNORE_CAPITALIZATION`.

## Примеры использования:

```python
import pyspeller
print(pyspeller.check_text('Текст для проверки орфографии.'))
print(pyspeller.check_text('Текст для проверки орфографии.', format_text='html'))
print(pyspeller.check_text('Текст для проверки орфографии.', lang='en'))
print(pyspeller.check_text('Текст для проверки орфографии.', options=['IGNORE_DIGITS', 'IGNORE_URLS', 'FIND_REPEAT_WORDS', 'IGNORE_CAPITALIZATION']))
print(pyspeller.check_text('Текст для проверки орфографии.', format_text='html', options=['IGNORE_DIGITS', 'IGNORE_URLS', 'FIND_REPEAT_WORDS', 'IGNORE_CAPITALIZATION']))
```

## Описание параметров метода `check_texts`:

- `query` — Список строк поисковых запросов.
- `lang` — Язык проверки орфографии (по умолчанию `ru,en`). Доступны `en`, `uk`, `ru`.
- `format_text` — Формат текста (по умолчанию `plain`). Доступны `plain`, `html`.
- `options` — Дополнительные опции проверки орфографии (по умолчанию `None`). Доступны `IGNORE_DIGITS`, `IGNORE_URLS`, `FIND_REPEAT_WORDS`, `IGNORE_CAPITALIZATION`.

## Примеры использования:

```python
import pyspeller
print(pyspeller.check_texts(['Текст для проверки орфографии.', 'Текст для проверки орфографии.']))
print(pyspeller.check_texts(['Текст для проверки орфографии.', 'Текст для проверки орфографии.'], format_text='html'))
print(pyspeller.check_texts(['Текст для проверки орфографии.', 'Текст для проверки орфографии.'], lang='en'))
print(pyspeller.check_texts(['Текст для проверки орфографии.', 'Текст для проверки орфографии.'], options=['IGNORE_DIGITS', 'IGNORE_URLS', 'FIND_REPEAT_WORDS', 'IGNORE_CAPITALIZATION']))
print(pyspeller.check_texts(['Текст для проверки орфографии.', 'Текст для проверки орфографии.'], format_text='html', options=['IGNORE_DIGITS', 'IGNORE_URLS', 'FIND_REPEAT_WORDS', 'IGNORE_CAPITALIZATION']))
```

## Лицензия

[MIT License](https://ustinov.mit-license.org/)

## Авторы

Алексей Устинов: 

- [GitVerse](https://gitverse.ru/ustinov)
- [GitHub](https://github.com/austnv)
- [Instagram](https://www.instagram.com/a_ustnv/)
- [Telegram](https://t.me/austnv)

"""

from typing import Literal
import requests

type Params = Literal['title', 'url', 'pageid', 'revision_id', 'summary', 'section_names', 'sections', 'html', 'content', 'images', 'links', 'categories', 'references']
type Language = Literal['en', 'ru', 'uk', 'en,ru', 'en,uk', 'ru,uk', 'en,ru,uk']
type FormatText = Literal['plain', 'html']
type Options = Literal['IGNORE_DIGITS', 'IGNORE_URLS', 'FIND_REPEAT_WORDS', 'IGNORE_CAPITALIZATION']
API_URL = 'https://speller.yandex.net/services/spellservice.json'

class OptionError(Exception):
    def __init__(self):
        self.message = "Options must be one of the following: IGNORE_DIGITS, IGNORE_URLS, FIND_REPEAT_WORDS, IGNORE_CAPITALIZATION"
        super().__init__(self.message)

class FormatTextError(Exception):
    def __init__(self):
        self.message = "Format text must be one of the following: plain, html."
        super().__init__(self.message)

def check_text(query: str, lang: Language = 'ru,en', format_text: FormatText = 'plain', options: Options = None) -> dict[str] | None:
    """
    Проверяет орфографию в указанном отрывке текста. [Страница](https://speller.yandex.net/services/spellservice?op=checkText) для демонстрации работы метода. [Документация](https://yandex.ru/dev/speller/doc/dg/reference/checkText-docpage/). 

    :param query: Строка поискового запроса.
    :type query: str
    :param format_text: Формат текста (по умолчанию `plain`). Доступны `plain`, `html`.
    :type format_text: str
    :param lang: Язык проверки орфографии (по умолчанию `ru,en`). Доступны `en`, `uk`, `ru`.
    :type lang: str
    :type options: list[str] | None | str
    :param options: Дополнительные опции проверки орфографии (по умолчанию `None`). Доступны `IGNORE_DIGITS`, `IGNORE_URLS`, `FIND_REPEAT_WORDS`, `IGNORE_CAPITALIZATION`. Может быть список строк или строка с одним элементом.

    * `IGNORE_DIGITS` - Пропускать слова с цифрами, например, "авп17х4534".
    * `IGNORE_URLS` - Пропускать интернет-адреса, почтовые адреса и имена файлов.
    * `FIND_REPEAT_WORDS` - Подсвечивать повторы слов, идущие подряд. Например, "я полетел **на на** Кипр".
    * `IGNORE_CAPITALIZATION` - Игнорировать неверное употребление ПРОПИСНЫХ/строчных букв, например, в слове "**м**осква".

    :return: Словарь с результатами проверки орфографии или `None`, если ошибок нет.
    :return type: `dict[str, Any] | None`

    ### Параметры ответа:
    - **code**: Код ошибки (см. [список кодов ошибок](https://yandex.ru/dev/speller/doc/ru/reference/error-codes)).
        * 1 - Слова нет в словаре.
        * 2 - Повтор слова.
        * 3 - Неверное употребление прописных и строчных букв.
        * 4 - Текст содержит слишком много ошибок. При этом приложение может отправить Яндекс Спеллеру оставшийся непроверенным текст в следующем запросе.
    - **pos**: Позиция слова с ошибкой.
    - **row**: Номер строки.
    - **col**: Номер столбца.
    - **len**: Длина слова с ошибкой.
    - **word**: Исходное слово.
    - **s**: Список исправлений для ошибки.

    ### Пример использования:
    ```python
    result = check_text('масква', 'ru', 'plain', ['IGNORE_URLS', 'IGNORE_DIGITS'])
    print(result)
    >>> {'code': 1, 'pos': 0, 'row': 0, 'col': 0, 'len': 6, 'word': 'масква', 's': ['москва', 'массква', 'маска']}
    ```
    """
    
    if format_text not in ['plain', 'html']: raise FormatTextError()

    _options = {
        'IGNORE_DIGITS': 2,
        'IGNORE_URLS': 4,
        'FIND_REPEAT_WORDS': 8,
        'IGNORE_CAPITALIZATION': 512
    }

    if options is None: sum_options = 0
    elif isinstance(options, str):
        if options not in _options: raise OptionError()
        sum_options = _options[options]
    elif isinstance(options, list):
        for o in options:
            if o not in _options: raise OptionError()
        sum_options = sum([_options[o] for o in options if o in _options])

    url = f'{API_URL}/checkText'
    data = {'text': query, 'lang': lang, 'format': format_text, 'options': sum_options}
    response = requests.post(url, data=data)
    if response.json(): return response.json()[0]
    else: return 

def check_texts(query: list[str], lang: Language = 'ru,en', format_text: FormatText = 'plain', options: Options = None) -> list[dict[str]]:
    """
    Проверяет орфографию в указанных фрагментах текста. Для каждого фрагмента возвращается отдельный массив ошибок с подсказками. [Страница](https://speller.yandex.net/services/spellservice?op=checkTexts) для демонстрации работы метода. [Документация](https://yandex.ru/dev/speller/doc/dg/reference/checkTexts-docpage/).

    :param query: Список текстов для проверки.
    :type query: list[str]

    .. warning :: Максимальный размер передаваемого текста составляет 10000 символов.

    :param format_text: Формат текста (по умолчанию `plain`). Доступны `plain`, `html`.
    :type format_text: str
    :param lang: Язык проверки орфографии (по умолчанию `ru,en`). Доступны `en`, `uk`, `ru`.
    :type lang: str
    :type options: list[str] | None | str
    :param options: Дополнительные опции проверки орфографии (по умолчанию `None`). Доступны `IGNORE_DIGITS`, `IGNORE_URLS`, `FIND_REPEAT_WORDS`, `IGNORE_CAPITALIZATION`. Может быть список строк или строка с одним элементом.

    * `IGNORE_DIGITS` - Пропускать слова с цифрами, например, "авп17х4534".
    * `IGNORE_URLS` - Пропускать интернет-адреса, почтовые адреса и имена файлов.
    * `FIND_REPEAT_WORDS` - Подсвечивать повторы слов, идущие подряд. Например, "я полетел **на на** Кипр".
    * `IGNORE_CAPITALIZATION` - Игнорировать неверное употребление ПРОПИСНЫХ/строчных букв, например, в слове "**м**осква".

    :return: Список словарей с результатами проверки орфографии.
    :return type: `list[dict[str, Any]]`

    ### Параметры ответа:
    - **code**: Код ошибки (см. [список кодов ошибок](https://yandex.ru/dev/speller/doc/ru/reference/error-codes)).
        * 1 - Слова нет в словаре.
        * 2 - Повтор слова.
        * 3 - Неверное употребление прописных и строчных букв.
        * 4 - Текст содержит слишком много ошибок. При этом приложение может отправить Яндекс Спеллеру оставшийся непроверенным текст в следующем запросе.
    - **pos**: Позиция слова с ошибкой.
    - **row**: Номер строки.
    - **col**: Номер столбца.
    - **len**: Длина слова с ошибкой.
    - **word**: Исходное слово.
    - **s**: Список исправлений для ошибки.

    ### Пример использования:
    ```python
    result = check_texts(['синхрафазатрон', 'олексей'])
    print(result)
    >>> [
            {'code': 1, 'pos': 0, 'row': 0, 'col': 0, 'len': 14,
            'word': 'синхрафазатрон',
            's': ['синхрофазотрон', 'синхрофазатрон', 'синхрофазотрона']},

            {'code': 1, 'pos': 0, 'row': 0, 'col': 0, 'len': 7,
            'word': 'олексей',
            's': ['алексей', 'олесей', 'алекссей']}
        ]
    """
    if format_text not in ['plain', 'html']: raise FormatTextError()

    _options = {
        'IGNORE_DIGITS': 2,
        'IGNORE_URLS': 4,
        'FIND_REPEAT_WORDS': 8,
        'IGNORE_CAPITALIZATION': 512
    }

    if options is None: sum_options = 0
    elif isinstance(options, str):
        if options not in _options: raise OptionError()
        sum_options = _options[options]
    elif isinstance(options, list):
        for o in options:
            if o not in _options: raise OptionError()
        sum_options = sum([_options[o] for o in options if o in _options])

    url = f'{API_URL}/checkTexts'
    data = {'text': query, 'lang': lang, 'format': format_text, 'options': sum_options}
    response = requests.post(url, data=data)
    if response.json():
        _result = []
        for result in response.json():
            _result.append(result[0])
        return _result
    else: return
