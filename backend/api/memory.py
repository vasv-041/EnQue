"""Hindsight Memory & Learning API Endpoints.
Complies with Section 11 of the PRD:
- GET  /api/memory/overview
- GET  /api/memory/recall
- POST /api/memory/reflect
- GET  /api/memory/history
"""

from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from pydantic import BaseModel

from backend.app.db import get_db
from backend.app.models import Brand, User, Recommendation, Experiment, ExperimentOutcome
from backend.app.utils.auth_deps import get_current_user
from backend.app.hindsight.service import memory_service

router = APIRouter(prefix="/api/memory", tags=["Hindsight Persistent Memory"])

class ReflectRequest(BaseModel):
    brand_id: int
    topic: Optional[str] = None

@router.get("/overview")
async def get_memory_overview(
    brand_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    brand = db.query(Brand).filter(Brand.id == brand_id, Brand.user_id == current_user.id).first()
    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found")

    outcomes = (
        db.query(ExperimentOutcome)
        .join(Experiment, ExperimentOutcome.experiment_id == Experiment.id)
        .filter(Experiment.brand_id == brand_id)
        .all()
    )

    learnings = [
        {
            "id": o.id,
            "experiment_id": o.experiment_id,
            "evaluation": o.evaluation,
            "learning_summary": o.learning_summary,
            "evaluated_at": o.evaluated_at
        }
        for o in outcomes
    ]

    return {
        "brand_id": brand.id,
        "brand_name": brand.brand_name,
        "hindsight_bank_id": brand.hindsight_bank_id,
        "stored_brand_knowledge": {
            "identity": brand.brand_name,
            "target_audience": brand.target_audience,
            "brand_voice": brand.brand_voice,
            "objectives": brand.objectives
        },
        "total_campaign_learnings": len(learnings),
        "recent_learnings": learnings[:10]
    }

@router.get("/recall")
async def recall_memories(
    brand_id: int,
    query: str = Query(..., description="Context query to recall past experiences"),
    limit: int = 5,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    brand = db.query(Brand).filter(Brand.id == brand_id, Brand.user_id == current_user.id).first()
    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found")

    memories = await memory_service.retrieve_memories(brand=brand, query=query, limit=limit)
    return {
        "brand_id": brand.id,
        "bank_id": brand.hindsight_bank_id,
        "query": query,
        "recalled_memories": memories
    }

@router.post("/reflect")
async def trigger_reflection(
    req: ReflectRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    brand = db.query(Brand).filter(Brand.id == req.brand_id, Brand.user_id == current_user.id).first()
    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found")

    reflection = await memory_service.trigger_reflection(brand=brand, topic=req.topic)
    return reflection

@router.get("/history")
async def get_learning_history(
    brand_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    brand = db.query(Brand).filter(Brand.id == brand_id, Brand.user_id == current_user.id).first()
    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found")

    recs = db.query(Recommendation).filter(Recommendation.brand_id == brand_id).all()
    experiments = db.query(Experiment).filter(Experiment.brand_id == brand_id).all()

    return {
        "brand_id": brand.id,
        "total_recommendations": len(recs),
        "total_experiments": len(experiments),
        "recommendations": [
            {
                "id": r.id,
                "recommendation": r.recommendation,
                "status": r.status,
                "expected_outcome": r.expected_outcome,
                "created_at": r.created_at
            }
            for r in recs
        ],
        "experiments": [
            {
                "id": e.id,
                "hypothesis": e.hypothesis,
                "status": e.status,
                "measurement_method": e.measurement_method,
                "start_date": e.start_date,
                "end_date": e.end_date
            }
            for e in experiments
        ]
    }

