"""Agent Operations API Endpoints.
Complies with Section 11 of the PRD:
- POST /api/agents/analyze
- POST /api/agents/strategy
- POST /api/agents/chat
- GET  /api/agents/runs/{run_id}
"""

import uuid
from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import Brand, User, AnalysisRun
from ..utils.auth_deps import get_current_user
from ..agents.audience_agent import audience_agent
from ..agents.content_agent import content_agent
from ..agents.orchestrator import orchestrator

router = APIRouter()

class AgentAnalysisRequest(BaseModel):
    brand_id: int
    agent_type: str = "both"  # "audience", "content", "both"

class AgentStrategyRequest(BaseModel):
    brand_id: int
    query: Optional[str] = "What should our brand post next month to maximize engagement and authority?"

class AgentChatRequest(BaseModel):
    brand_id: int
    message: str

@router.post("/strategy")
async def generate_orchestrated_strategy(
    req: AgentStrategyRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    brand = db.query(Brand).filter(Brand.id == req.brand_id, Brand.user_id == current_user.id).first()
    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found")

    result = await orchestrator.execute_strategy_cycle(
        brand=brand,
        user_query=req.query,
        db=db
    )
    return result

@router.post("/analyze")
async def run_agent_analysis(
    req: AgentAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    brand = db.query(Brand).filter(Brand.id == req.brand_id, Brand.user_id == current_user.id).first()
    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found")

    results: Dict[str, Any] = {}

    if req.agent_type in ("audience", "both"):
        audience_output = await audience_agent.analyze(brand, db)
        results["audience_intelligence"] = audience_output

    if req.agent_type in ("content", "both"):
        content_output = await content_agent.analyze(brand, db)
        results["content_intelligence"] = content_output

    run = AnalysisRun(
        brand_id=brand.id,
        analysis_type=f"agent_{req.agent_type}",
        execution_status="completed",
        result=results
    )
    db.add(run)
    db.commit()
    db.refresh(run)

    return {
        "status": "success",
        "run_id": run.id,
        "brand_id": brand.id,
        "brand_name": brand.brand_name,
        "results": results
    }

@router.get("/runs/{run_id}")
def get_run_details(
    run_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    run = db.query(AnalysisRun).filter(AnalysisRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Analysis run not found")
    
    brand = db.query(Brand).filter(Brand.id == run.brand_id, Brand.user_id == current_user.id).first()
    if not brand:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    return {
        "run_id": run.id,
        "brand_id": run.brand_id,
        "analysis_type": run.analysis_type,
        "execution_status": run.execution_status,
        "result": run.result,
        "created_at": run.created_at
    }

@router.post("/chat")
async def chat_with_agents(
    req: AgentChatRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    brand = db.query(Brand).filter(Brand.id == req.brand_id, Brand.user_id == current_user.id).first()
    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found")

    strategy_res = await orchestrator.execute_strategy_cycle(brand=brand, user_query=req.message, db=db)
    top_rec = strategy_res["recommendations"][0] if strategy_res["recommendations"] else {}

    return {
        "user_query": req.message,
        "brand": brand.brand_name,
        "primary_recommendation": top_rec.get("recommendation"),
        "reasoning": top_rec.get("reasoning"),
        "historical_evidence": top_rec.get("historical_evidence"),
        "audience_evidence": top_rec.get("audience_evidence"),
        "agent_response": (
            f"Based on real audience insights and past memory for '{brand.brand_name}': "
            f"{top_rec.get('recommendation', 'Continue evaluating educational formats')}. "
            f"Reasoning: {top_rec.get('reasoning', '')}"
        )
    }
