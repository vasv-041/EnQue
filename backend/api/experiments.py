"""Recommendations & Experiments Lifecycle API Endpoints.
Complies with Section 11 & Section 14 of the PRD:
- POST  /api/recommendations
- GET   /api/recommendations
- PATCH /api/recommendations/{id}
- POST  /api/experiments
- GET   /api/experiments
- POST  /api/experiments/{id}/evaluate
- GET   /api/experiments/{id}/outcome
"""

from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from backend.app.db import get_db
from backend.app.models import Brand, User, Recommendation, Experiment, ExperimentOutcome
from backend.app.utils.auth_deps import get_current_user
from backend.app.agents.evaluator_agent import evaluation_agent

router = APIRouter(tags=["Recommendations & Experiments"])

class RecommendationStatusUpdate(BaseModel):
    status: str  # proposed, implemented, rejected

class ExperimentCreate(BaseModel):
    brand_id: int
    recommendation_id: Optional[int] = None
    hypothesis: str
    measurement_method: Optional[str] = None

class ExperimentEvaluateRequest(BaseModel):
    actual_results: Dict[str, Any]  # e.g. {"save_rate": 8.4, "engagement_rate": 6.2, "reach_growth": 14.5}

# --- Recommendations ---

@router.get("/api/recommendations")
def list_recommendations(
    brand_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    brand = db.query(Brand).filter(Brand.id == brand_id, Brand.user_id == current_user.id).first()
    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found")

    recs = db.query(Recommendation).filter(Recommendation.brand_id == brand_id).order_by(Recommendation.created_at.desc()).all()
    return [
        {
            "id": r.id,
            "recommendation": r.recommendation,
            "reasoning": r.reasoning,
            "evidence": r.evidence,
            "expected_outcome": r.expected_outcome,
            "status": r.status,
            "created_at": r.created_at
        }
        for r in recs
    ]

@router.patch("/api/recommendations/{rec_id}")
def update_recommendation_status(
    rec_id: int,
    body: RecommendationStatusUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    rec = db.query(Recommendation).filter(Recommendation.id == rec_id).first()
    if not rec:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Recommendation not found")

    brand = db.query(Brand).filter(Brand.id == rec.brand_id, Brand.user_id == current_user.id).first()
    if not brand:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    rec.status = body.status
    db.commit()
    db.refresh(rec)
    return {"id": rec.id, "status": rec.status, "message": f"Recommendation updated to {rec.status}"}

# --- Experiments & Learning ---

@router.post("/api/experiments")
def create_experiment(
    exp: ExperimentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    brand = db.query(Brand).filter(Brand.id == exp.brand_id, Brand.user_id == current_user.id).first()
    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found")

    experiment = Experiment(
        brand_id=brand.id,
        recommendation_id=exp.recommendation_id,
        hypothesis=exp.hypothesis,
        measurement_method=exp.measurement_method,
        status="active"
    )
    db.add(experiment)
    db.commit()
    db.refresh(experiment)
    return {"id": experiment.id, "status": experiment.status, "hypothesis": experiment.hypothesis}

@router.get("/api/experiments")
def list_experiments(
    brand_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    brand = db.query(Brand).filter(Brand.id == brand_id, Brand.user_id == current_user.id).first()
    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found")

    exps = db.query(Experiment).filter(Experiment.brand_id == brand_id).order_by(Experiment.created_at.desc()).all()
    return [
        {
            "id": e.id,
            "recommendation_id": e.recommendation_id,
            "hypothesis": e.hypothesis,
            "measurement_method": e.measurement_method,
            "status": e.status,
            "created_at": e.created_at
        }
        for e in exps
    ]

@router.post("/api/experiments/{exp_id}/evaluate")
async def evaluate_experiment(
    exp_id: int,
    body: ExperimentEvaluateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    exp = db.query(Experiment).filter(Experiment.id == exp_id).first()
    if not exp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experiment not found")

    brand = db.query(Brand).filter(Brand.id == exp.brand_id, Brand.user_id == current_user.id).first()
    if not brand:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    # If linked to a recommendation, use it; otherwise create a proxy
    rec = db.query(Recommendation).filter(Recommendation.id == exp.recommendation_id).first() if exp.recommendation_id else None
    if not rec:
        rec = Recommendation(
            brand_id=brand.id,
            recommendation=exp.hypothesis,
            expected_outcome=exp.measurement_method or "Increase engagement",
            status="implemented"
        )
        db.add(rec)
        db.flush()

    res = await evaluation_agent.evaluate_and_learn(
        brand=brand,
        recommendation=rec,
        actual_results=body.actual_results,
        db=db
    )
    return res

@router.get("/api/experiments/{exp_id}/outcome")
def get_experiment_outcome(
    exp_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    exp = db.query(Experiment).filter(Experiment.id == exp_id).first()
    if not exp:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experiment not found")

    brand = db.query(Brand).filter(Brand.id == exp.brand_id, Brand.user_id == current_user.id).first()
    if not brand:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")

    outcome = db.query(ExperimentOutcome).filter(ExperimentOutcome.experiment_id == exp_id).first()
    if not outcome:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Outcome not yet evaluated")

    return {
        "experiment_id": exp.id,
        "hypothesis": exp.hypothesis,
        "evaluation": outcome.evaluation,
        "learning_summary": outcome.learning_summary,
        "actual_results": outcome.actual_results,
        "evaluated_at": outcome.evaluated_at
    }

