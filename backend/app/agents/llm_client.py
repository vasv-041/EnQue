"""LLM Client Wrapper supporting both Groq Cloud API and Local Ollama with automatic fallback.
Providers:
1. Groq API:
   - Primary model: openai/gpt-oss-120b or qwen/qwen3-32b
2. Ollama Local:
   - Local model: qwen2.5:7b, qwen2.5:14b, qwen2.5:3b, or any local Ollama model
3. Deterministic Grounding Fallback:
   - Uses real audience & post metrics computed from data when no LLM is reachable.
"""

import json
import logging
import urllib.request
import urllib.error
from typing import Dict, Any, Optional

from ..config import (
    LLM_PROVIDER,
    GROQ_API_KEY,
    GROQ_BASE_URL,
    PRIMARY_LLM_MODEL,
    FALLBACK_LLM_MODEL,
    OLLAMA_BASE_URL,
    OLLAMA_MODEL,
)

logger = logging.getLogger("EnQue.LLMClient")

class LLMClient:
    def __init__(self):
        self.provider = LLM_PROVIDER
        self.groq_api_key = GROQ_API_KEY
        self.groq_base_url = GROQ_BASE_URL.rstrip("/")
        self.primary_model = PRIMARY_LLM_MODEL
        self.fallback_model = FALLBACK_LLM_MODEL
        self.ollama_base_url = OLLAMA_BASE_URL.rstrip("/")
        self.ollama_model = OLLAMA_MODEL

    def _clean_json_string(self, text: str) -> str:
        clean = text.strip()
        if clean.startswith("```json"):
            clean = clean[7:]
        if clean.startswith("```"):
            clean = clean[3:]
        if clean.endswith("```"):
            clean = clean[:-3]
        return clean.strip()

    def _query_ollama(self, system_prompt: str, user_prompt: str) -> Optional[Dict[str, Any]]:
        """Queries local Ollama endpoint via /api/generate or /api/chat."""
        try:
            url = f"{self.ollama_base_url}/api/chat"
            payload = {
                "model": self.ollama_model,
                "messages": [
                    {"role": "system", "content": f"{system_prompt}\nIMPORTANT: Respond with valid JSON only."},
                    {"role": "user", "content": user_prompt}
                ],
                "format": "json",
                "stream": False,
                "options": {
                    "temperature": 0.2
                }
            }
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST"
            )
            with urllib.request.urlopen(req, timeout=45.0) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    raw = data.get("message", {}).get("content", "")
                    clean = self._clean_json_string(raw)
                    return json.loads(clean)
        except Exception as e:
            logger.warning(f"Ollama local query failed ({self.ollama_model}): {e}")
            return None

    def _query_groq(self, system_prompt: str, user_prompt: str) -> Optional[Dict[str, Any]]:
        """Queries Groq OpenAI-compatible API."""
        if not self.groq_api_key or self.groq_api_key.startswith("YOUR_"):
            return None

        for model in [self.primary_model, self.fallback_model]:
            try:
                url = f"{self.groq_base_url}/chat/completions"
                headers = {
                    "Authorization": f"Bearer {self.groq_api_key}",
                    "Content-Type": "application/json",
                    "User-Agent": "EnQue-Backend/1.0"
                }
                payload = {
                    "model": model,
                    "messages": [
                        {"role": "system", "content": f"{system_prompt}\nIMPORTANT: You must reply with raw valid JSON only without markdown formatting."},
                        {"role": "user", "content": user_prompt}
                    ],
                    "temperature": 0.2,
                    "response_format": {"type": "json_object"}
                }

                req = urllib.request.Request(
                    url,
                    data=json.dumps(payload).encode("utf-8"),
                    headers=headers,
                    method="POST"
                )

                with urllib.request.urlopen(req, timeout=25.0) as resp:
                    if resp.status == 200:
                        data = json.loads(resp.read().decode("utf-8"))
                        raw_content = data["choices"][0]["message"]["content"]
                        clean_content = self._clean_json_string(raw_content)
                        return json.loads(clean_content)
            except Exception as e:
                logger.warning(f"Groq API error on model {model}: {e}")

        return None

    async def generate_json(self, system_prompt: str, user_prompt: str) -> Optional[Dict[str, Any]]:
        """
        Orchestrates LLM calls:
        - If provider is 'ollama': calls local Ollama first.
        - If provider is 'groq': calls Groq first.
        - If provider is 'auto': tries Ollama local if available, then Groq, then falls back gracefully.
        """
        if self.provider == "ollama":
            result = self._query_ollama(system_prompt, user_prompt)
            if result:
                return result

        elif self.provider == "groq":
            result = self._query_groq(system_prompt, user_prompt)
            if result:
                return result

        else:  # auto
            # Try Ollama local first (if server is up)
            result = self._query_ollama(system_prompt, user_prompt)
            if result:
                return result

            # Try Groq API
            result = self._query_groq(system_prompt, user_prompt)
            if result:
                return result

        # Fallback to None (which triggers deterministic agent logic)
        return None

llm_client = LLMClient()
