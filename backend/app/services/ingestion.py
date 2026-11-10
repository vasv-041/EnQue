"""Service layer for data ingestion.
- Validates file type (CSV, XLSX, PDF, TXT).
- Reads tabular data with pandas for CSV/XLSX.
- Performs basic column validation according to PRD.
- Persists records to the database (placeholder implementation).
"""
import pandas as pd
import io
from fastapi import UploadFile, HTTPException
from sqlalchemy.orm import Session
from ..models import Post, PostMetric, Campaign, Brand
from ..db import get_db

# Expected columns for posts (as per PRD section 5.1)
POST_COLUMNS = [
    "post_id",
    "platform",
    "post_date",
    "caption",
    "content_type",
    "topic",
    "reach",
    "impressions",
    "likes",
    "comments",
    "shares",
    "saves",
    "clicks",
    "campaign_id",
]

def _read_file_to_df(file: UploadFile) -> pd.DataFrame:
    filename = file.filename.lower()
    content = file.file.read()
    if filename.endswith('.csv'):
        return pd.read_csv(io.BytesIO(content))
    elif filename.endswith('.xlsx'):
        return pd.read_excel(io.BytesIO(content))
    elif filename.endswith('.txt'):
        return pd.read_csv(io.BytesIO(content), sep="\t")
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

def validate_columns(df: pd.DataFrame, required: list) -> None:
    missing = [col for col in required if col not in df.columns]
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required columns: {', '.join(missing)}",
        )

def ingest_posts(file: UploadFile, db: Session) -> dict:
    df = _read_file_to_df(file)
    validate_columns(df, POST_COLUMNS)
    # Simple bulk insert placeholder – in real code you would map to ORM models and handle duplicates
    inserted = 0
    for _, row in df.iterrows():
        post = Post(
            brand_id=row.get('brand_id', None),  # optional – you may derive from auth context later
            campaign_id=row.get('campaign_id'),
            platform=row.get('platform'),
            caption=row.get('caption'),
            content_type=row.get('content_type'),
            topic=row.get('topic'),
            post_date=row.get('post_date'),
        )
        db.add(post)
        db.flush()  # obtain post.id
        metric = PostMetric(
            post_id=post.id,
            reach=row.get('reach'),
            impressions=row.get('impressions'),
            likes=row.get('likes'),
            comments=row.get('comments'),
            shares=row.get('shares'),
            saves=row.get('saves'),
            clicks=row.get('clicks'),
        )
        db.add(metric)
        inserted += 1
    db.commit()
    return {"inserted": inserted, "status": "success"}

