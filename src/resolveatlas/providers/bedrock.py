"""Adapter for the documented AWS Bedrock Runtime Converse API."""

from __future__ import annotations

import asyncio
import inspect
from typing import Any

from resolveatlas.providers.base import GenerationRequest, GenerationResponse
from resolveatlas.providers.prompt import render_request


class BedrockProvider:
    """Use a caller-configured Bedrock Runtime client and explicit model ID."""

    provider_id = "bedrock"

    def __init__(self, *, client: Any, default_model: str) -> None:
        if client is None:
            raise ValueError("client must be supplied")
        if not default_model.strip():
            raise ValueError("default_model must not be empty")
        self._client = client
        self._default_model = default_model

    @classmethod
    def from_boto3(cls, *, default_model: str, region_name: str | None = None):
        """Build from boto3's normal public credential chain when installed."""

        try:
            import boto3
        except ImportError as error:
            raise RuntimeError(
                "install ResolveAtlas with the 'aws' extra to use Bedrock"
            ) from error
        return cls(
            client=boto3.client("bedrock-runtime", region_name=region_name),
            default_model=default_model,
        )

    async def generate(self, request: GenerationRequest) -> GenerationResponse:
        model = request.model or self._default_model
        arguments = {
            "modelId": model,
            "messages": [
                {"role": "user", "content": [{"text": render_request(request)}]}
            ],
            "inferenceConfig": {"maxTokens": request.max_output_tokens},
        }
        if inspect.iscoroutinefunction(self._client.converse):
            raw = await self._client.converse(**arguments)
        else:
            raw = await asyncio.to_thread(self._client.converse, **arguments)
        try:
            blocks = raw["output"]["message"]["content"]
            text = "".join(block.get("text", "") for block in blocks).strip()
        except (KeyError, TypeError) as error:
            raise RuntimeError(
                "Bedrock Converse returned an unexpected response shape"
            ) from error
        usage = raw.get("usage", {})
        return GenerationResponse(
            text=text,
            provider=self.provider_id,
            model=model,
            usage={
                "input_tokens": int(usage.get("inputTokens", 0)),
                "output_tokens": int(usage.get("outputTokens", 0)),
            },
        )
