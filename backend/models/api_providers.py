"""
API Providers for cloud-based LLM services.

Supports:
- OpenAI (GPT-4, GPT-3.5, o1)
- Anthropic (Claude)
- Google (Gemini)
- Custom OpenAI-compatible endpoints
"""

import logging
from typing import AsyncIterator, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod

try:
    from openai import AsyncOpenAI
except ImportError:
    AsyncOpenAI = None

try:
    from anthropic import AsyncAnthropic
except ImportError:
    AsyncAnthropic = None

try:
    import google.generativeai as genai
except ImportError:
    genai = None


logger = logging.getLogger(__name__)


@dataclass
class APIProviderConfig:
    """Configuration for API providers."""
    api_key: str
    base_url: Optional[str] = None
    organization: Optional[str] = None
    timeout: int = 60


class APIProvider(ABC):
    """Base class for API providers."""

    @abstractmethod
    async def generate(
        self,
        prompt: str,
        model: str,
        **kwargs
    ) -> str:
        """Generate completion."""
        pass

    @abstractmethod
    async def generate_stream(
        self,
        prompt: str,
        model: str,
        **kwargs
    ) -> AsyncIterator[str]:
        """Generate streaming completion."""
        pass


class OpenAIProvider(APIProvider):
    """OpenAI API provider."""

    def __init__(self, config: APIProviderConfig):
        if AsyncOpenAI is None:
            raise ImportError("openai package required. Install with: pip install openai")
        
        self.client = AsyncOpenAI(
            api_key=config.api_key,
            base_url=config.base_url,
            organization=config.organization,
            timeout=config.timeout
        )
        logger.info("OpenAI provider initialized")

    async def generate(
        self,
        prompt: str,
        model: str,
        **kwargs
    ) -> str:
        """Generate completion using OpenAI API."""
        response = await self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        return response.choices[0].message.content

    async def generate_stream(
        self,
        prompt: str,
        model: str,
        **kwargs
    ) -> AsyncIterator[str]:
        """Generate streaming completion."""
        kwargs["stream"] = True
        
        stream = await self.client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content


class AnthropicProvider(APIProvider):
    """Anthropic (Claude) API provider."""

    def __init__(self, config: APIProviderConfig):
        if AsyncAnthropic is None:
            raise ImportError("anthropic package required. Install with: pip install anthropic")
        
        self.client = AsyncAnthropic(
            api_key=config.api_key,
            timeout=config.timeout
        )
        logger.info("Anthropic provider initialized")

    async def generate(
        self,
        prompt: str,
        model: str,
        max_tokens: int = 1024,
        **kwargs
    ) -> str:
        """Generate completion using Anthropic API."""
        response = await self.client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        )
        return response.content[0].text

    async def generate_stream(
        self,
        prompt: str,
        model: str,
        max_tokens: int = 1024,
        **kwargs
    ) -> AsyncIterator[str]:
        """Generate streaming completion."""
        async with self.client.messages.stream(
            model=model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
            **kwargs
        ) as stream:
            async for text in stream.text_stream:
                yield text


class GoogleProvider(APIProvider):
    """Google (Gemini) API provider."""

    def __init__(self, config: APIProviderConfig):
        if genai is None:
            raise ImportError(
                "google-generativeai package required. "
                "Install with: pip install google-generativeai"
            )
        
        genai.configure(api_key=config.api_key)
        self.config = config
        logger.info("Google provider initialized")

    async def generate(
        self,
        prompt: str,
        model: str,
        **kwargs
    ) -> str:
        """Generate completion using Google Gemini API."""
        model_obj = genai.GenerativeModel(model)
        response = await model_obj.generate_content_async(prompt, **kwargs)
        return response.text

    async def generate_stream(
        self,
        prompt: str,
        model: str,
        **kwargs
    ) -> AsyncIterator[str]:
        """Generate streaming completion."""
        model_obj = genai.GenerativeModel(model)
        response = await model_obj.generate_content_async(
            prompt,
            stream=True,
            **kwargs
        )
        
        async for chunk in response:
            if chunk.text:
                yield chunk.text


# Provider registry
PROVIDERS = {
    "openai": OpenAIProvider,
    "anthropic": AnthropicProvider,
    "google": GoogleProvider,
}


def get_provider(provider_name: str, config: APIProviderConfig) -> APIProvider:
    """
    Get an API provider instance.
    
    Args:
        provider_name: Name of provider (openai, anthropic, google)
        config: Provider configuration
        
    Returns:
        Initialized provider
        
    Raises:
        ValueError: If provider not found
    """
    if provider_name not in PROVIDERS:
        raise ValueError(f"Unknown provider: {provider_name}")
    
    return PROVIDERS[provider_name](config)
