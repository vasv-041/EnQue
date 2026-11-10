"""Central Agent Orchestrator.
Coordinates the four specialized AI agents adhering to PRD Section 7:
1. Receives user strategic request.
2. Retrieves brand information.
3. Retrieves relevant persistent memories from Hindsight (hindsight recall).
4. Retrieves relevant document context via RAG.
5. Executes Audience Intelligence Agent & Content Intelligence Agent.
6. Invokes Strategy Agent supplying accumulated history & current data.
7. Validates & stores structured recommendations into PostgreSQL.
8. Returns evidence-grounded strategy to the user.
"""

from typing import Dict, Any, List, Optional
from sqlalchemy.orm import Session
import logging

from ..models import Brand, Recommendation, AnalysisRun
from ..hindsight.service import memory_service
from ..rag.retriever import rag_retriever
from .audience_agent import audience_agent
from .content_agent import content_agent
from .strategy_agent import strategy_agent
from .evaluator_agent import evaluation_agent

logger = logging.getLogger("EnQue.Orchestrator")

class CentralAgentOrchestrator:
    def __init__(self):
        self.audience_agent = audience_agent
        self.content_agent = content_agent
        self.strategy_agent = strategy_agent
        self.evaluation_agent = evaluation_agent

    async def execute_strategy_cycle(
        self,
        brand: Brand,
        user_query: str,
        db: Session
    ) -> Dict[str, Any]:
        """
        Coordinates full intelligence cycle:
        Collect -> Analyze -> Remember -> Strategize
        """
        logger.info(f"Orchestrating strategy workflow for Brand: {brand.brand_name} (ID: {brand.id})")

        # 1. Retrieve Historical Experiential Memories from Hindsight
        recalled_memories = await memory_service.retrieve_memories(
            brand=brand,
            query=user_query,
            limit=5
        )

        # 2. Retrieve Relevant Guidelines / Docs via RAG
        rag_chunks = rag_retriever.retrieve_relevant_chunks(
            brand_id=brand.id,
            query=user_query,
            db=db,
            top_k=3
        )

        # 3. Run Audience Intelligence Agent
        audience_output = await self.audience_agent.analyze(brand=brand, db=db)

        # 4. Run Content Intelligence Agent
        content_output = await self.content_agent.analyze(brand=brand, db=db)

        # 5. Run Strategy Agent (combining Current Data + Hindsight Memories + RAG)
        recommendations = await self.strategy_agent.generate_strategy(
            brand=brand,
            audience_data=audience_output,
            content_data=content_output,
            recalled_memories=recalled_memories,
            rag_chunks=rag_chunks,
            user_query=user_query
        )

        # 6. Persist Recommendations into DB
        saved_recs = []
        for r in recommendations:
            rec_obj = Recommendation(
                brand_id=brand.id,
                recommendation=r.get("recommendation", ""),
                reasoning=r.get("reasoning", ""),
                evidence={
                    "audience_evidence": r.get("audience_evidence"),
                    "historical_evidence": r.get("historical_evidence"),
                    "confidence_level": r.get("confidence_level"),
                    "measurement_method": r.get("measurement_method")
                },
                expected_outcome=r.get("expected_outcome", ""),
                status="proposed"
            )
            db.add(rec_obj)
            db.flush()
            saved_recs.append({
                "id": rec_obj.id,
                "recommendation": rec_obj.recommendation,
                "reasoning": rec_obj.reasoning,
                "audience_evidence": r.get("audience_evidence"),
                "historical_evidence": r.get("historical_evidence"),
                "expected_outcome": rec_obj.expected_outcome,
                "confidence_level": r.get("confidence_level"),
                "measurement_method": r.get("measurement_method"),
                "status": rec_obj.status
            })

        db.commit()

        # Log run
        run = AnalysisRun(
            brand_id=brand.id,
            analysis_type="orchestrated_strategy",
            execution_status="completed",
            result={
                "user_query": user_query,
                "recalled_memories_count": len(recalled_memories),
                "recommendations_count": len(saved_recs)
            }
        )
        db.add(run)
        db.commit()

        return {
            "status": "success",
            "brand_id": brand.id,
            "brand_name": brand.brand_name,
            "user_query": user_query,
            "hindsight_memories_used": recalled_memories,
            "rag_chunks_used": [c.get("text") for c in rag_chunks],
            "audience_intelligence": audience_output,
            "content_intelligence": content_output,
            "recommendations": saved_recs
        }

orchestrator = CentralAgentOrchestrator()

