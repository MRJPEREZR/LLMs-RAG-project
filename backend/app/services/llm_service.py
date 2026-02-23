# # app/services/llm/base.py
# from abc import ABC, abstractmethod
# from typing import List, Dict, Any, Optional, AsyncGenerator
# from dataclasses import dataclass

# @dataclass
# class LLMResponse:
#     text: str
#     tokens_used: int
#     model_used: str
#     processing_time: float
#     finish_reason: str
#     metadata: Optional[Dict] = None

# class BaseLLMService(ABC):
#     """Abstract base class for LLM services"""
    
#     @abstractmethod
#     async def generate(
#         self,
#         prompt: str,
#         system_prompt: Optional[str] = None,
#         temperature: float = 0.7,
#         max_tokens: int = 1000,
#         stop_sequences: Optional[List[str]] = None
#     ) -> LLMResponse:
#         """Generate a response from the LLM"""
#         pass
    
#     @abstractmethod
#     async def generate_with_history(
#         self,
#         messages: List[Dict[str, str]],
#         temperature: float = 0.7,
#         max_tokens: int = 1000
#     ) -> LLMResponse:
#         """Generate response with conversation history"""
#         pass
    
#     @abstractmethod
#     async def stream_generate(
#         self,
#         prompt: str,
#         system_prompt: Optional[str] = None
#     ) -> AsyncGenerator[str, None]:
#         """Stream tokens as they're generated"""
#         pass
    
#     @abstractmethod
#     async def count_tokens(self, text: str) -> int:
#         """Count tokens in text"""
#         pass