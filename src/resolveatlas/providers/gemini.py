"""Adapter for Google's documented public Gemini generateContent REST API."""

from __future__ import annotations

import asyncio
import json
from collections.abc import Awaitable, Callable
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from resolveatlas.providers.base import GenerationRequest, GenerationResponse
from resolveatlas.providers.prompt import render_request
from resolveatlas.security.outbound import OutboundPolicy

JsonTransport = Callable[[Request, float], Awaitable[dict]]


async def _urlopen_json(request: Request, timeout: float) -> dict:
    def send() -> dict:
        try:
            # The request URL is constructed from a fixed public origin and is
            # validated by OutboundPolicy immediately before this transport.
            with urlopen(request, timeout=timeout) as response:  # nosec B310
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as error:
            # Response bodies may contain request content or provider details. Do not
            # include them in exceptions that could enter application logs.
            raise RuntimeError(
                f"Gemini API request failed with HTTP {error.code}"
            ) from error

    return await asyncio.to_thread(send)


class GeminiProvider:
    """Send bounded evidence to one explicitly selected Gemini model."""

    provider_id = "gemini"
    _HOST = "generativelanguage.googleapis.com"
    _BASE_URL = "https://generativelanguage.googleapis.com"

    def __init__(
        self,
        *,
        api_key: str,
        default_model: str,
        timeout_seconds: float = 30.0,
        transport: JsonTransport = _urlopen_json,
    ) -> None:
        if not api_key.strip() or not default_model.strip():
            raise ValueError("api_key and default_model must not be empty")
        if timeout_seconds <= 0:
            raise ValueError("timeout_seconds must be positive")
        self._api_key = api_key
        self._default_model = default_model
        self._timeout = timeout_seconds
        self._transport = transport
        self._policy = OutboundPolicy(frozenset({self._HOST}))

    async def generate(self, request: GenerationRequest) -> GenerationResponse:
        model = request.model or self._default_model
        url = f"{self._BASE_URL}/v1beta/models/{model}:generateContent"
        self._policy.validate(url)
        payload = {
            "contents": [
                {"role": "user", "parts": [{"text": render_request(request)}]}
            ],
            "generationConfig": {"maxOutputTokens": request.max_output_tokens},
        }
        http_request = Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "x-goog-api-key": self._api_key,
            },
            method="POST",
        )
        raw = await self._transport(http_request, self._timeout)
        try:
            parts = raw["candidates"][0]["content"]["parts"]
            text = "".join(part.get("text", "") for part in parts).strip()
        except (KeyError, IndexError, TypeError) as error:
            raise RuntimeError(
                "Gemini API returned an unexpected response shape"
            ) from error
        usage = raw.get("usageMetadata", {})
        return GenerationResponse(
            text=text,
            provider=self.provider_id,
            model=model,
            usage={
                "input_tokens": int(usage.get("promptTokenCount", 0)),
                "output_tokens": int(usage.get("candidatesTokenCount", 0)),
            },
        )
