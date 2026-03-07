"""Custom exceptions for ESPN API client."""

from __future__ import annotations


class ESPNApiError(Exception):
    """Base exception for ESPN API errors."""

    def __init__(self, message: str, status_code: int | None = None):
        self.status_code = status_code
        super().__init__(message)


class ESPNNotFoundError(ESPNApiError):
    """Resource not found (HTTP 404)."""

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=404)


class ESPNRateLimitError(ESPNApiError):
    """Rate limited by ESPN API (HTTP 429)."""

    def __init__(self, message: str = "Rate limited by ESPN API"):
        super().__init__(message, status_code=429)


class ESPNServerError(ESPNApiError):
    """ESPN API server error (HTTP 5xx)."""

    def __init__(self, message: str = "ESPN API server error", status_code: int = 500):
        super().__init__(message, status_code=status_code)


class ESPNTimeoutError(ESPNApiError):
    """Request to ESPN API timed out."""

    def __init__(self, message: str = "Request timed out"):
        super().__init__(message, status_code=None)


class ESPNResponseError(ESPNApiError):
    """Invalid or unparseable response from ESPN API."""

    def __init__(self, message: str = "Invalid response from ESPN API"):
        super().__init__(message, status_code=None)
