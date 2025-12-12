"""
AI client abstraction layer supporting multiple providers
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import openai
import boto3
from ..core.config import settings


class AIClient(ABC):
    """Abstract base class for AI providers"""
    
    @abstractmethod
    async def call_llm(self, prompt: str, model: str = None, **kwargs) -> str:
        """Call language model with prompt"""
        pass
    
    @abstractmethod
    async def analyze_image(self, image_url: str, prompt: str) -> str:
        """Analyze image with vision capabilities"""
        pass


class OpenAIClient(AIClient):
    """OpenAI GPT client implementation"""
    
    def __init__(self):
        if not settings.openai_api_key:
            raise ValueError("OpenAI API key not configured")
        openai.api_key = settings.openai_api_key
        self.client = openai.OpenAI(api_key=settings.openai_api_key)
    
    async def call_llm(self, prompt: str, model: str = "gpt-4", **kwargs) -> str:
        """Call OpenAI GPT model"""
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "user", "content": prompt}
                ],
                max_tokens=kwargs.get("max_tokens", 2000),
                temperature=kwargs.get("temperature", 0.7)
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI API error: {str(e)}")
    
    async def analyze_image(self, image_url: str, prompt: str) -> str:
        """Analyze image using GPT-4 Vision"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-4-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
                            {"type": "image_url", "image_url": {"url": image_url}}
                        ]
                    }
                ],
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"OpenAI Vision API error: {str(e)}")


class BedrockClient(AIClient):
    """AWS Bedrock client implementation"""
    
    def __init__(self):
        if not settings.aws_access_key_id or not settings.aws_secret_access_key:
            raise ValueError("AWS credentials not configured")
        
        self.bedrock = boto3.client(
            'bedrock-runtime',
            aws_access_key_id=settings.aws_access_key_id,
            aws_secret_access_key=settings.aws_secret_access_key,
            region_name=settings.aws_region
        )
    
    async def call_llm(self, prompt: str, model: str = "anthropic.claude-3-sonnet-20240229-v1:0", **kwargs) -> str:
        """Call AWS Bedrock model (Claude)"""
        try:
            import json
            
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": kwargs.get("max_tokens", 2000),
                "messages": [
                    {"role": "user", "content": prompt}
                ],
                "temperature": kwargs.get("temperature", 0.7)
            }
            
            response = self.bedrock.invoke_model(
                modelId=model,
                body=json.dumps(body)
            )
            
            response_body = json.loads(response['body'].read())
            return response_body['content'][0]['text']
        except Exception as e:
            raise Exception(f"Bedrock API error: {str(e)}")
    
    async def analyze_image(self, image_url: str, prompt: str) -> str:
        """Analyze image using Bedrock vision models"""
        # TODO: Implement Bedrock vision capabilities
        raise NotImplementedError("Bedrock vision analysis not yet implemented")


class AIClientFactory:
    """Factory for creating AI clients based on configuration"""
    
    @staticmethod
    def create_client() -> AIClient:
        """Create AI client based on settings"""
        if settings.ai_provider == "openai":
            return OpenAIClient()
        elif settings.ai_provider == "bedrock":
            return BedrockClient()
        else:
            raise ValueError(f"Unsupported AI provider: {settings.ai_provider}")


# Global AI client instance
ai_client: Optional[AIClient] = None


def get_ai_client() -> AIClient:
    """Get or create AI client instance"""
    global ai_client
    if ai_client is None:
        ai_client = AIClientFactory.create_client()
    return ai_client


# Convenience function for common use cases
async def call_ai(prompt: str, model: str = None, **kwargs) -> str:
    """Convenience function to call AI with prompt"""
    client = get_ai_client()
    return await client.call_llm(prompt, model, **kwargs)