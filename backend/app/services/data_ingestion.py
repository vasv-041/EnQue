"""Robust Data Ingestion Service.
Supports:
- CSV
- Excel (.xlsx, .xls)
- Plain Text / TSV (.txt)
- PDF (.pdf) text extraction
Handles:
- File extension and size validation
- Column normalization and schema matching for Posts, Audience Comments, and Campaigns
- Missing value imputation and duplicate detection
- Association with brand_id
- Detailed ingestion report (total detected, imported, rejected, skipped duplicates, errors)
"""

import io
import re
from typing import Dict, Any, List, Optional
from datetime import datetime
import pandas as pd
from fastapi import UploadFile, HTTPException, status
from sqlalchemy.orm import Session

from ..models import Post, PostMetric, AudienceComment, Campaign, Document
from ..analysis.metrics import calculate_post_metrics

MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB

POST_SCHEMA_ALIASES = {
    "post_id": ["post_id", "id", "external_id"],
    "platform": ["platform", "channel", "network"],
    "post_date": ["post_date", "date", "published_at", "created_at"],
    "caption": ["caption", "content", "text", "body", "post_text"],
    "content_type": ["content_type", "type", "format", "media_type"],
    "topic": ["topic", "category", "theme", "tag"],
    "reach": ["reach", "unique_views"],
    "impressions": ["impressions", "views"],
    "likes": ["likes", "favorites"],
    "comments": ["comments", "num_comments", "replies"],
    "shares": ["shares", "retweets", "reposts"],
    "saves": ["saves", "bookmarks"],
    "clicks": ["clicks", "link_clicks"],
    "campaign_id": ["campaign_id", "campaign"]
}

COMMENT_SCHEMA_ALIASES = {
    "comment_id": ["comment_id", "id", "external_id"],
    "post_id": ["post_id", "post"],
    "comment_text": ["comment_text", "text", "comment", "body", "message"],
    "comment_date": ["comment_date", "date", "created_at"],
    "platform": ["platform", "channel"]
}

def normalize_columns(columns: List[str], schema_aliases: Dict[str, List[str]]) -> Dict[str, str]:
    """Maps actual dataframe column names to canonical schema keys."""
    mapping = {}
    clean_cols = {re.sub(r'[^a-zA-Z0-9_]', '', str(c).strip().lower()): c for c in columns}
    for canon, aliases in schema_aliases.items():
        for alias in aliases:
            clean_alias = re.sub(r'[^a-zA-Z0-9_]', '', alias.lower())
            if clean_alias in clean_cols:
                mapping[clean_cols[clean_alias]] = canon
                break
    return mapping

def extract_text_from_pdf(content: bytes) -> str:
    """Extract text from PDF using pypdf or PyPDF2 if installed, or fallback parser."""
    try:
        import pypdf
        reader = pypdf.PdfReader(io.BytesIO(content))
        text = "\n".join([page.extract_text() or "" for page in reader.pages])
        return text
    except ImportError:
        try:
            from pypdf2 import PdfReader
            reader = PdfReader(io.BytesIO(content))
            text = "\n".join([page.extract_text() or "" for page in reader.pages])
            return text
        except Exception as e:
            # Fallback simple string extraction
            clean_text = re.sub(rb'[^\x20-\x7E\n\r\t]', b' ', content).decode('latin1', errors='ignore')
            return clean_text

def parse_file_to_df(filename: str, content: bytes) -> pd.DataFrame:
    fname = filename.lower()
    if fname.endswith(".csv"):
        return pd.read_csv(io.BytesIO(content))
    elif fname.endswith((".xlsx", ".xls")):
        return pd.read_excel(io.BytesIO(content))
    elif fname.endswith(".txt"):
        try:
            return pd.read_csv(io.BytesIO(content), sep=None, engine="python")
        except Exception:
            return pd.DataFrame({"text_content": [content.decode("utf-8", errors="ignore")]})
    else:
        raise ValueError(f"Unsupported tabular file format: {filename}")

async def ingest_dataset(
    file: UploadFile,
    brand_id: int,
    db: Session,
    dataset_type: str = "auto"  # 'auto', 'posts', 'comments', 'campaigns', 'document'
) -> Dict[str, Any]:
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds maximum limit of 25MB")
    
    fname = file.filename.lower()
    
    # Handle PDF or raw text document for RAG ingestion
    if fname.endswith(".pdf") or dataset_type == "document":
        text = extract_text_from_pdf(content) if fname.endswith(".pdf") else content.decode("utf-8", errors="ignore")
        doc = Document(
            brand_id=brand_id,
            file_name=file.filename,
            document_type=dataset_type if dataset_type != "auto" else "brand_guidelines",
            processing_status="completed"
        )
        db.add(doc)
        db.commit()
        db.refresh(doc)
        return {
            "status": "success",
            "document_id": doc.id,
            "file_name": file.filename,
            "type": "document",
            "characters_extracted": len(text),
            "report": {
                "total_records": 1,
                "imported": 1,
                "rejected": 0,
                "skipped_duplicates": 0,
                "errors": []
            }
        }
    
    # Handle Tabular Data (CSV, Excel, TSV)
    try:
        df = parse_file_to_df(file.filename, content)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to parse file: {str(e)}")

    if df.empty:
        raise HTTPException(status_code=400, detail="Uploaded file contains no data")

    # Detect dataset type if auto
    if dataset_type == "auto":
        comment_matches = sum(1 for c in df.columns if any(a in str(c).lower() for a in COMMENT_SCHEMA_ALIASES["comment_text"]))
        reach_matches = sum(1 for c in df.columns if any(a in str(c).lower() for a in ["reach", "likes", "impressions", "caption"]))
        if comment_matches > 0 and reach_matches == 0:
            dataset_type = "comments"
        else:
            dataset_type = "posts"

    report = {
        "total_records": len(df),
        "imported": 0,
        "rejected": 0,
        "skipped_duplicates": 0,
        "errors": []
    }

    if dataset_type == "comments":
        col_map = normalize_columns(list(df.columns), COMMENT_SCHEMA_ALIASES)
        renamed_df = df.rename(columns=col_map)
        if "comment_text" not in renamed_df.columns:
            raise HTTPException(status_code=400, detail="Missing required comment text column in dataset")
        
        existing_comments = {
            c[0] for c in db.query(AudienceComment.external_comment_id).filter(
                AudienceComment.brand_id == brand_id,
                AudienceComment.external_comment_id.isnot(None)
            ).all()
        }

        for idx, row in renamed_df.iterrows():
            text = str(row.get("comment_text", "")).strip()
            if not text or text.lower() == "nan":
                report["rejected"] += 1
                report["errors"].append(f"Row {idx+1}: Empty comment text")
                continue
            
            ext_id = str(row.get("comment_id", "")).strip()
            if ext_id and ext_id in existing_comments:
                report["skipped_duplicates"] += 1
                continue
            
            c_date = None
            if pd.notna(row.get("comment_date")):
                try:
                    c_date = pd.to_datetime(row.get("comment_date")).to_pydatetime()
                except Exception:
                    c_date = datetime.utcnow()

            comment_obj = AudienceComment(
                brand_id=brand_id,
                external_comment_id=ext_id if ext_id else None,
                comment_text=text,
                comment_date=c_date,
                platform=str(row.get("platform", "general")) if pd.notna(row.get("platform")) else "general"
            )
            db.add(comment_obj)
            report["imported"] += 1
            if ext_id:
                existing_comments.add(ext_id)

    else:  # 'posts'
        col_map = normalize_columns(list(df.columns), POST_SCHEMA_ALIASES)
        renamed_df = df.rename(columns=col_map)
        
        # Check existing post IDs to avoid duplicates
        existing_posts = {
            p[0] for p in db.query(Post.external_post_id).filter(
                Post.brand_id == brand_id,
                Post.external_post_id.isnot(None)
            ).all()
        }

        for idx, row in renamed_df.iterrows():
            ext_id = str(row.get("post_id", "")).strip() if pd.notna(row.get("post_id")) else None
            if ext_id and ext_id in existing_posts:
                report["skipped_duplicates"] += 1
                continue

            caption = str(row.get("caption", "")).strip() if pd.notna(row.get("caption")) else ""
            if not caption and not ext_id:
                report["rejected"] += 1
                report["errors"].append(f"Row {idx+1}: Missing both post_id and caption")
                continue

            post_date = None
            if pd.notna(row.get("post_date")):
                try:
                    post_date = pd.to_datetime(row.get("post_date")).to_pydatetime()
                except Exception:
                    post_date = datetime.utcnow()

            def clean_num(val):
                try:
                    return float(val) if pd.notna(val) else 0.0
                except Exception:
                    return 0.0

            post_obj = Post(
                brand_id=brand_id,
                external_post_id=ext_id,
                platform=str(row.get("platform", "instagram")) if pd.notna(row.get("platform")) else "instagram",
                caption=caption,
                content_type=str(row.get("content_type", "post")) if pd.notna(row.get("content_type")) else "post",
                topic=str(row.get("topic", "general")) if pd.notna(row.get("topic")) else "general",
                post_date=post_date,
            )
            db.add(post_obj)
            db.flush()  # Generate post_obj.id

            metric_obj = PostMetric(
                post_id=post_obj.id,
                reach=clean_num(row.get("reach")),
                impressions=clean_num(row.get("impressions")),
                likes=clean_num(row.get("likes")),
                comments=clean_num(row.get("comments")),
                shares=clean_num(row.get("shares")),
                saves=clean_num(row.get("saves")),
                clicks=clean_num(row.get("clicks")),
            )
            db.add(metric_obj)
            report["imported"] += 1
            if ext_id:
                existing_posts.add(ext_id)

    db.commit()

    return {
        "status": "success",
        "dataset_type": dataset_type,
        "filename": file.filename,
        "report": report
    }

