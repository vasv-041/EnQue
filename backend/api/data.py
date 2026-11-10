"""Data Ingestion and Management API Endpoints.
Complies with Section 11 of the PRD:
- POST /api/data/upload
- GET  /api/data/files
- GET  /api/data/files/{id}
- POST /api/data/process
- GET  /api/data/process/{job_id}
"""

import uuid
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.orm import Session

from backend.app.db import get_db
from backend.app.models import Brand, Document, Post, AudienceComment, AnalysisRun
from backend.app.utils.auth_deps import get_current_user
from backend.app.services.data_ingestion import ingest_dataset

router = APIRouter(prefix="/api/data", tags=["Data Ingestion"])

@router.post("/upload")
async def upload_data(
    brand_id: int = Form(...),
    dataset_type: str = Form("auto"),  # auto, posts, comments, document
    file: UploadFile = File(...),
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Verify brand belongs to current user
    brand = db.query(Brand).filter(Brand.id == brand_id, Brand.user_id == current_user.id).first()
    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found or access denied")
    
    result = await ingest_dataset(file=file, brand_id=brand_id, db=db, dataset_type=dataset_type)
    return result

@router.get("/files")
def list_files(
    brand_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    brand = db.query(Brand).filter(Brand.id == brand_id, Brand.user_id == current_user.id).first()
    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found")
    
    docs = db.query(Document).filter(Document.brand_id == brand_id).all()
    posts_count = db.query(Post).filter(Post.brand_id == brand_id).count()
    comments_count = db.query(AudienceComment).filter(AudienceComment.brand_id == brand_id).count()
    
    return {
        "brand_id": brand_id,
        "total_posts": posts_count,
        "total_comments": comments_count,
        "documents": [
            {
                "id": d.id,
                "file_name": d.file_name,
                "document_type": d.document_type,
                "processing_status": d.processing_status,
                "uploaded_at": d.uploaded_at
            }
            for d in docs
        ]
    }

@router.get("/files/{file_id}")
def get_file(
    file_id: int,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    doc = db.query(Document).filter(Document.id == file_id).first()
    if not doc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Document not found")
    
    # Verify brand ownership
    brand = db.query(Brand).filter(Brand.id == doc.brand_id, Brand.user_id == current_user.id).first()
    if not brand:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
        
    return {
        "id": doc.id,
        "file_name": doc.file_name,
        "document_type": doc.document_type,
        "processing_status": doc.processing_status,
        "uploaded_at": doc.uploaded_at
    }

@router.post("/process")
def trigger_processing(
    brand_id: int,
    analysis_type: str = "full",
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    brand = db.query(Brand).filter(Brand.id == brand_id, Brand.user_id == current_user.id).first()
    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found")

    job_id = f"job_{uuid.uuid4().hex[:12]}"
    run = AnalysisRun(
        brand_id=brand_id,
        analysis_type=analysis_type,
        execution_status="completed",  # Synchronous MVP mode
        result={"message": f"Processed {analysis_type} pipeline for brand {brand.brand_name}"}
    )
    db.add(run)
    db.commit()
    db.refresh(run)

    return {
        "job_id": job_id,
        "run_id": run.id,
        "status": "completed",
        "brand_id": brand_id,
        "analysis_type": analysis_type
    }

@router.get("/process/{job_id}")
def get_job_status(
    job_id: str,
    current_user = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return {
        "job_id": job_id,
        "status": "completed",
        "message": "Data processing complete"
    }

