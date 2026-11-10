"""Routers for data ingestion endpoints.
Provides a simple POST endpoint to upload files (CSV/Excel/etc.).
Actual validation/parsing will be implemented later.
"""

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from ..db import get_db
from sqlalchemy.orm import Session

router = APIRouter()

@router.post("/file")
async def ingest_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Call the ingestion service to process the uploaded file
    result = await ingest_posts(file, db)
    return result
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    return {"filename": file.filename, "content_type": file.content_type, "status": "received"}

