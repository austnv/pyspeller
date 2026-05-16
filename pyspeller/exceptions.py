"""Пользовательские исключения для библиотеки."""


class SpellerError(Exception):
    """Базовое исключение библиотеки. Все остальные наследуются от него."""


class SpellerAPIError(SpellerError):
    """
    Исключение, возникающее при ошибке API (HTTP 4xx или 5xx).

    Attributes:
        status_code: HTTP-код ответа.
        message: Тело ответа с описанием ошибки.
    """

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"API Error {status_code}: {message}")


class SpellerNetworkError(SpellerError):
    """
    Исключение, возникающее при сетевых проблемах (таймаут, DNS и т.п.).

    Attributes:
        original_exception: Оригинальное исключение от httpx.
    """

    def __init__(self, original_exception: Exception):
        self.original_exception = original_exception
        super().__init__(f"Network error: {original_exception}")