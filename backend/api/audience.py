"""Audience Intelligence Analytics Engine and Routes.
Implements:
- POST /api/audience/analyze
- GET  /api/audience/insights
- GET  /api/audience/trends
Uses rule-based NLP / sentiment polarity & recurring topic extraction for deterministic baseline.
"""

from typing import List, Dict, Any
from collections import Counter
import re
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import pandas as pd

from backend.app.db import get_db
from backend.app.models import Brand, AudienceComment
from backend.app.utils.auth_deps import get_current_user

router = APIRouter(prefix="/api/audience", tags=["Audience Intelligence"])

# Sentiment word lists for deterministic baseline analysis
POSITIVE_WORDS = {
    "love", "amazing", "great", "best", "good", "obsessed", "effective", "hydrating",
    "clean", "recommend", "holy grail", "smooth", "glow", "perfect", "favorite", "helpful"
}
NEGATIVE_WORDS = {
    "breakout", "broke out", "irritation", "allergic", "dry", "bad", "worst", "greasy",
    "expensive", "waste", "burning", "rash", "damaged", "scam", "disappointed", "sticky"
}
QUESTION_INDICATORS = {"?", "how", "what", "when", "where", "why", "can i", "is this", "does it", "routine"}
PAIN_POINT_KEYWORDS = {"purge", "acne", "sensitive", "drying", "smell", "scent", "reaction", "packaging"}

def analyze_comments(comments: List[AudienceComment]) -> Dict[str, Any]:
    if not comments:
        return {
            "total_comments": 0,
            "sentiment_breakdown": {"positive": 0, "neutral": 0, "negative": 0},
            "overall_sentiment": "Neutral",
            "dominant_topics": [],
            "common_questions": [],
            "pain_points": [],
            "emerging_trends": []
        }

    positive_count = 0
    negative_count = 0
    neutral_count = 0
    
    questions = []
    pain_points = []
    word_freq = Counter()

    for c in comments:
        text = c.comment_text.lower()
        
        # Sentiment
        pos = any(w in text for w in POSITIVE_WORDS)
        neg = any(w in text for w in NEGATIVE_WORDS)
        if pos and not neg:
            positive_count += 1
            c.sentiment = "Positive"
        elif neg and not pos:
            negative_count += 1
            c.sentiment = "Negative"
        else:
            neutral_count += 1
            c.sentiment = "Neutral"

        # Questions
        if any(q in text for q in QUESTION_INDICATORS):
            questions.append(c.comment_text)

        # Pain points
        if any(p in text for p in PAIN_POINT_KEYWORDS) or neg:
            pain_points.append(c.comment_text)

        # Word frequency for topics (excluding common stopwords)
        words = re.findall(r'[a-zA-Z]{3,}', text)
        stopwords = {"this", "that", "with", "have", "from", "your", "what", "about", "product", "using", "like"}
        filtered = [w for w in words if w not in stopwords]
        word_freq.update(filtered)

    total = len(comments)
    if positive_count > negative_count and positive_count > neutral_count:
        overall = "Positive"
    elif negative_count > positive_count:
        overall = "Negative"
    else:
        overall = "Mixed / Neutral"

    dominant_topics = [word for word, count in word_freq.most_common(6)]

    return {
        "total_comments": total,
        "sentiment_breakdown": {
            "positive": positive_count,
            "neutral": neutral_count,
            "negative": negative_count,
            "positive_ratio": round(positive_count / total * 100, 1) if total else 0,
            "negative_ratio": round(negative_count / total * 100, 1) if total else 0
        },
        "overall_sentiment": overall,
        "dominant_topics": dominant_topics,
        "common_questions": questions[:5],
        "pain_points": pain_points[:5],
        "emerging_trends": [w.capitalize() for w, _ in word_freq.most_common(3)]
    }

@router.get("/insights")
def get_audience_insights(
    brand_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    brand = db.query(Brand).filter(Brand.id == brand_id, Brand.user_id == current_user.id).first()
    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found")

    comments = db.query(AudienceComment).filter(AudienceComment.brand_id == brand_id).all()
    analysis = analyze_comments(comments)
    analysis["brand_id"] = brand_id
    analysis["brand_name"] = brand.brand_name
    return analysis

@router.get("/trends")
def get_audience_trends(
    brand_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    brand = db.query(Brand).filter(Brand.id == brand_id, Brand.user_id == current_user.id).first()
    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found")

    comments = db.query(AudienceComment).filter(AudienceComment.brand_id == brand_id).all()
    analysis = analyze_comments(comments)
    return {
        "brand_id": brand_id,
        "dominant_topics": analysis["dominant_topics"],
        "emerging_trends": analysis["emerging_trends"],
        "common_questions_sample": analysis["common_questions"]
    }

@router.post("/analyze")
def trigger_audience_analysis(
    brand_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    brand = db.query(Brand).filter(Brand.id == brand_id, Brand.user_id == current_user.id).first()
    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found")

    comments = db.query(AudienceComment).filter(AudienceComment.brand_id == brand_id).all()
    analysis = analyze_comments(comments)
    db.commit()  # Save individual sentiment labels
    return {
        "status": "success",
        "brand_id": brand_id,
        "insights": analysis
    }

