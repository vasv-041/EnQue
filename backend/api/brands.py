"""Brand management routes for EnQue API.
Implements full CRUD, user authorization, and automatic Hindsight memory bank assignment.
"""

import uuid
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.db import get_db
from backend.app.models import Brand, User
from backend.app.utils.auth_deps import get_current_user
from backend.app.schemas.brand import BrandCreate, BrandUpdate, BrandResponse

router = APIRouter(prefix="/api/brands", tags=["Brands"])

@router.post("", response_model=BrandResponse, status_code=status.HTTP_201_CREATED)
def create_brand(
    brand_in: BrandCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Isolated memory bank id for Hindsight
    bank_id = f"bank_{uuid.uuid4().hex[:12]}_{brand_in.brand_name.lower().replace(' ', '_')[:16]}"
    
    brand = Brand(
        user_id=current_user.id,
        brand_name=brand_in.brand_name,
        description=brand_in.description,
        industry=brand_in.industry,
        target_audience=brand_in.target_audience,
        objectives=brand_in.objectives,
        brand_voice=brand_in.brand_voice,
        hindsight_bank_id=bank_id
    )
    db.add(brand)
    db.commit()
    db.refresh(brand)
    return brand

@router.get("", response_model=List[BrandResponse])
def list_brands(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return db.query(Brand).filter(Brand.user_id == current_user.id).all()

@router.get("/{brand_id}", response_model=BrandResponse)
def get_brand(
    brand_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    brand = db.query(Brand).filter(Brand.id == brand_id, Brand.user_id == current_user.id).first()
    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found")
    return brand

@router.put("/{brand_id}", response_model=BrandResponse)
def update_brand(
    brand_id: int,
    brand_in: BrandUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    brand = db.query(Brand).filter(Brand.id == brand_id, Brand.user_id == current_user.id).first()
    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found")
    
    update_data = brand_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(brand, field, value)
    
    db.commit()
    db.refresh(brand)
    return brand

@router.delete("/{brand_id}", status_code=status.HTTP_200_OK)
def delete_brand(
    brand_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    brand = db.query(Brand).filter(Brand.id == brand_id, Brand.user_id == current_user.id).first()
    if not brand:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Brand not found")
    
    db.delete(brand)
    db.commit()
    return {"message": "Brand deleted successfully", "brand_id": brand_id}
