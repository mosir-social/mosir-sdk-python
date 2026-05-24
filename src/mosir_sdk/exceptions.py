from __future__ import annotations

from typing import Any


class MosirSdkError(Exception):
    """Base exception for mosir-sdk-python."""


class GraphQLRequestError(MosirSdkError):
    """Raised when the Mosir API returns GraphQL errors."""

    def __init__(self, errors: list[dict[str, Any]]) -> None:
        self.errors = errors
        message = "\n".join(str(error.get("message", error)) for error in errors)
        super().__init__(message)


class GraphQLTransportError(MosirSdkError):
    """Raised when the Mosir API returns a non-GraphQL transport failure."""
