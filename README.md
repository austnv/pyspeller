# pyspeller

Библиотека для проверки орфографии с использованием [API Яндекс Спеллер][я]. Обертка Python для [Яндекс.Спеллер][я].

Без зависимостей.

## Установка

```bash
pip install pyspeller
```

## Использование

```python
from pyspeller import *

result = check_text('масква', 'ru', 'plain', ['IGNORE_URLS', 'IGNORE_DIGITS'])
print(result)

result = check_texts(['синхрафазатрон', 'олексей'])
print(result)
```

## Документация

- [Страница][1] для демонстрации работы метода `check_text`.
- [Документация][3] для метода `check_text`.
- [Страница][2] для демонстрации работы метода `check_texts`.
- [Документация][4] для метода `check_texts`.
- [Условия использования][5] сервиса «API Яндекс.Спеллер»


## Контакты

- [GitVerse][6]
- [Email][7]
- [Telegram][8]

## Лицензия

[The MIT License (MIT)][9] - лицензия в репозитории

[Постоянная ссылка][10] на лицензию



[я]: https://yandex.ru/dev/speller/
[1]: https://speller.yandex.net/services/spellservice?op=checkText
[2]: https://speller.yandex.net/services/spellservice?op=checkTexts
[3]: https://yandex.ru/dev/speller/doc/dg/reference/checkText-docpage/
[4]: https://yandex.ru/dev/speller/doc/dg/reference/checkTexts-docpage/
[5]: https://yandex.ru/legal/speller_api/
[6]: https://gitverse.ru/ustinov
[7]: mailto:lesin2798@mail.ru?subject=pyspeller
[8]: https://t.me/austnv?text=pyspeller
[9]: LICENSE
[10]: https://ustinov.mit-license.org/