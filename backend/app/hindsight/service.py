"""Memory management service coordinating local persistence and Hindsight cloud operations."""

from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from ..models import Brand, Recommendation, Experiment, ExperimentOutcome
from .client import hindsight_client

class MemoryService:
    async def store_experience(
        self,
        brand: Brand,
        content: str,
        category: str = "experience",
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Stores experience into the brand's Hindsight memory bank."""
        bank_id = brand.hindsight_bank_id or f"bank_{brand.id}_{brand.brand_name.lower().replace(' ', '_')}"
        return await hindsight_client.retain(bank_id, content, category=category, metadata=metadata)

    async def retrieve_memories(
        self,
        brand: Brand,
        query: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """Recalls relevant memories from Hindsight for strategy generation."""
        bank_id = brand.hindsight_bank_id or f"bank_{brand.id}_{brand.brand_name.lower().replace(' ', '_')}"
        memories = await hindsight_client.recall(bank_id, query=query, limit=limit)
        return memories

    async def trigger_reflection(
        self,
        brand: Brand,
        topic: Optional[str] = None
    ) -> Dict[str, Any]:
        """Triggers higher-level reflection across past experiences."""
        bank_id = brand.hindsight_bank_id or f"bank_{brand.id}_{brand.brand_name.lower().replace(' ', '_')}"
        return await hindsight_client.reflect(bank_id, topic=topic)

memory_service = MemoryService()

