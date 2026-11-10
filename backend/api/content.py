"""Content Analytics and Performance API Endpoints.
Complies with Section 11 & Section 5.2 of the PRD:
- POST /api/content/analyze
- GET  /api/content/analytics
- GET  /api/content/top-performing
- GET  /api/content/underperforming
"""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import pandas as pd

from backend.app.db import get_db
from backend.app.models import Brand, Post, PostMetric
from backend.app.utils.auth_deps import get_current_user
from backend.app.analysis.metrics import calculate_post_metrics, summarize_content_performance

router = APIRouter(prefix="/api/content", tags=["Content Intelligence"])

def _get_posts_dataframe(brand_id: int, db: Session) -> pd.DataFrame:
    results = (
        db.query(
            Post.id,
            Post.external_post_id,
            Post.platform,
            Post.caption,
            Post.content_type,
            Post.topic,
            Post.post_date,
            PostMetric.reach,
            PostMetric.impressions,
            PostMetric.likes,
            PostMetric.comments,
            PostMetric.shares,
            PostMetric.saves,
            PostMetric.clicks
        )
        .outerjoin(PostMetric, Post.id == PostMetric.post_id)
        .filter(Post.brand_id == brand_id)
        .all()
    )
    if not results:
        return pd.DataFrame()
    
    data = []
    for r in results:
        data.append({
            "id": r[0],
            "external_post_id": r[1],
            "platform": r[2],
            "caption": r[3],
            "content_type": r[4],
            "topic": r[5],
            "post_date": str(r[6]) if r[6] else None,
            "reach": r[7] or 0.0,
            "impressions": r[8] or 0.0,
            "likes": r[9] or 0.0,
            "comments": r[10] or 0.0,
            "shares": r[11] or 0.0,
            "saves": r[12] or 0.0,
            "clicks": r[13] or 0.0
        })
    return pd.DataFrame(data)

@router.get("/analytics")
def get_content_analytics(
    brand_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    brand = db.query(Brand).filter(Brand.id == brand_id, Brand.user_id == current_user.id).first()
    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found")

    df = _get_posts_dataframe(brand_id, db)
    summary = summarize_content_performance(df)
    summary["brand_id"] = brand_id
    summary["brand_name"] = brand.brand_name
    return summary

@router.get("/top-performing")
def get_top_performing_content(
    brand_id: int,
    limit: int = 5,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    brand = db.query(Brand).filter(Brand.id == brand_id, Brand.user_id == current_user.id).first()
    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found")

    df = _get_posts_dataframe(brand_id, db)
    if df.empty:
        return []

    calculated = calculate_post_metrics(df)
    top = calculated.sort_values(by="engagement_rate", ascending=False).head(limit)
    return top.to_dict(orient="records")

@router.get("/underperforming")
def get_underperforming_content(
    brand_id: int,
    limit: int = 5,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    brand = db.query(Brand).filter(Brand.id == brand_id, Brand.user_id == current_user.id).first()
    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found")

    df = _get_posts_dataframe(brand_id, db)
    if df.empty:
        return []

    calculated = calculate_post_metrics(df)
    bottom = calculated.sort_values(by="engagement_rate", ascending=True).head(limit)
    return bottom.to_dict(orient="records")

@router.post("/analyze")
def trigger_content_analysis(
    brand_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    brand = db.query(Brand).filter(Brand.id == brand_id, Brand.user_id == current_user.id).first()
    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found")

    df = _get_posts_dataframe(brand_id, db)
    summary = summarize_content_performance(df)
    return {
        "status": "success",
        "brand_id": brand_id,
        "summary": summary
    }

