from __future__ import annotations

import json
from collections.abc import AsyncIterator, Awaitable, Mapping
from typing import Any, TypeAlias, cast

import httpx
from graphql import OperationDefinitionNode, OperationType, get_operation_ast, parse
from httpx_sse import aconnect_sse

from ._operations import OPERATION_REGISTRY, OperationSpec
from .exceptions import GraphQLRequestError, GraphQLTransportError

DEFAULT_ENDPOINT = "https://beta.mosir.app/api/v1"
JSONMapping: TypeAlias = dict[str, Any]


class AsyncMosirClient:
    """Async client for the Mosir public GraphQL API.

    Wrapped snake_case methods are resolved dynamically from `public.operations.graphql`.
    For example: `get_post(...)`, `get_notifications(...)`, `post_updated(...)`.
    """

    def __init__(
        self,
        *,
        token: str | None = None,
        endpoint: str = DEFAULT_ENDPOINT,
        headers: Mapping[str, str] | None = None,
        timeout: float | httpx.Timeout | None = None,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        self.token = token
        self.endpoint = endpoint
        self._default_headers = dict(headers or {})
        self._owns_client = client is None
        self._client = client or httpx.AsyncClient(timeout=timeout)

    async def __aenter__(self) -> AsyncMosirClient:
        return self

    async def __aexit__(self, exc_type: object, exc: object, tb: object) -> None:
        await self.aclose()

    def __getattr__(self, name: str) -> Any:
        spec = OPERATION_REGISTRY.get(name)
        if spec is None:
            raise AttributeError(f"{type(self).__name__!s} has no attribute {name!r}")

        if spec.operation_type == "subscription":
            def subscription_method(**variables: Any) -> AsyncIterator[JSONMapping]:
                return self.subscribe_operation(name, **variables)

            return subscription_method

        async def operation_method(**variables: Any) -> JSONMapping:
            return await self.operation(name, **variables)

        return operation_method

    async def aclose(self) -> None:
        if self._owns_client:
            await self._client.aclose()

    async def request(
        self,
        document: str,
        variables: Mapping[str, Any] | None = None,
        *,
        operation_name: str | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> JSONMapping:
        operation = _get_operation(document, operation_name)
        if operation.operation is OperationType.SUBSCRIPTION:
            raise ValueError("Use subscribe(...) for subscription operations.")

        response = await self._client.post(
            self.endpoint,
            json=_build_payload(document, variables, operation_name),
            headers=self._build_headers(headers),
        )
        return _parse_json_response(response)

    def execute(
        self,
        document: str,
        variables: Mapping[str, Any] | None = None,
        *,
        operation_name: str | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> Awaitable[JSONMapping] | AsyncIterator[JSONMapping]:
        operation = _get_operation(document, operation_name)
        if operation.operation is OperationType.SUBSCRIPTION:
            return self.subscribe(
                document,
                variables,
                operation_name=operation_name,
                headers=headers,
            )
        return self.request(
            document,
            variables,
            operation_name=operation_name,
            headers=headers,
        )

    async def operation(self, name: str, /, **variables: Any) -> JSONMapping:
        spec = _get_operation_spec(name)
        if spec.operation_type == "subscription":
            raise ValueError(f"Operation {name!r} is a subscription. Use subscribe_operation(...).")

        return await self.request(
            spec.document,
            _normalize_variables(variables, spec.variable_map) or None,
            operation_name=spec.operation_name,
        )

    def subscribe_operation(self, name: str, /, **variables: Any) -> AsyncIterator[JSONMapping]:
        spec = _get_operation_spec(name)
        if spec.operation_type != "subscription":
            raise ValueError(f"Operation {name!r} is not a subscription. Use operation(...).")

        return self.subscribe(
            spec.document,
            _normalize_variables(variables, spec.variable_map) or None,
            operation_name=spec.operation_name,
        )

    def subscribe(
        self,
        document: str,
        variables: Mapping[str, Any] | None = None,
        *,
        operation_name: str | None = None,
        headers: Mapping[str, str] | None = None,
    ) -> AsyncIterator[JSONMapping]:
        operation = _get_operation(document, operation_name)
        if operation.operation is not OperationType.SUBSCRIPTION:
            raise ValueError("Use request(...) for query and mutation operations.")

        async def iterator() -> AsyncIterator[JSONMapping]:
            async with aconnect_sse(
                self._client,
                "POST",
                self.endpoint,
                json=_build_payload(document, variables, operation_name),
                headers=self._build_headers(headers),
            ) as event_source:
                async for event in event_source.aiter_sse():
                    if event.event == "complete":
                        break
                    if not event.data:
                        continue

                    payload = json.loads(event.data)
                    errors = payload.get("errors")
                    if errors:
                        raise GraphQLRequestError(errors)

                    data = payload.get("data")
                    if data is not None:
                        if not isinstance(data, dict):
                            raise GraphQLTransportError("Expected a GraphQL data object in the SSE payload.")
                        yield cast(JSONMapping, data)

        return iterator()

    def _build_headers(self, headers: Mapping[str, str] | None = None) -> dict[str, str]:
        merged = dict(self._default_headers)
        if self.token:
            merged["Authorization"] = f"Bearer {self.token}"
        if headers:
            merged.update(headers)
        return merged


def _get_operation_spec(name: str) -> OperationSpec:
    spec = OPERATION_REGISTRY.get(name)
    if spec is None:
        raise KeyError(f"Unknown Mosir operation: {name}")
    return spec


def _normalize_variables(variables: Mapping[str, Any], variable_map: Mapping[str, str]) -> dict[str, Any]:
    normalized: dict[str, Any] = {}
    for key, value in variables.items():
        normalized[variable_map.get(key, key)] = value
    return normalized


def _build_payload(
    document: str,
    variables: Mapping[str, Any] | None,
    operation_name: str | None,
) -> JSONMapping:
    payload: JSONMapping = {"query": document}
    if variables is not None:
        payload["variables"] = dict(variables)
    if operation_name is not None:
        payload["operationName"] = operation_name
    return payload


def _get_operation(document: str, operation_name: str | None) -> OperationDefinitionNode:
    operation = get_operation_ast(parse(document), operation_name)
    if operation is None:
        raise ValueError(
            "Unable to resolve GraphQL operation. Provide a single operation document or pass operation_name.",
        )
    return operation


def _parse_json_response(response: httpx.Response) -> JSONMapping:
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as exc:
        raise GraphQLTransportError(str(exc)) from exc

    payload = response.json()
    if not isinstance(payload, dict):
        raise GraphQLTransportError("Expected a JSON object response from the Mosir API.")

    errors = payload.get("errors")
    if isinstance(errors, list) and errors:
        raise GraphQLRequestError(errors)

    data = payload.get("data")
    if not isinstance(data, dict):
        raise GraphQLTransportError("Expected a GraphQL data object in the response.")

    return cast(JSONMapping, data)
