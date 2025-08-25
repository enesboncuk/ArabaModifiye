from typing import List, Optional
from fastapi import APIRouter, Query, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from ..database import get_db, Asset, VehicleSpec

router = APIRouter()


class WheelAssetResponse(BaseModel):
    id: int
    brand: str
    model: str
    thumb_url: Optional[str] = None
    meta_json: Optional[str] = None

    class Config:
        from_attributes = True


class VehicleSpecResponse(BaseModel):
    id: int
    make: str
    model: str
    year: int
    trim: Optional[str] = None
    bolt_pattern: Optional[str] = None
    rim_diameter: Optional[float] = None
    rim_width: Optional[float] = None
    offset: Optional[float] = None
    center_bore: Optional[float] = None

    class Config:
        from_attributes = True


@router.get("/wheels", response_model=List[WheelAssetResponse])
async def get_wheels(
    brand: Optional[str] = Query(None, description="Filter by wheel brand"),
    db: Session = Depends(get_db)
):
    query = db.query(Asset).filter(Asset.kind == "wheel")
    
    if brand:
        query = query.filter(Asset.brand.ilike(f"%{brand}%"))
    
    wheels = query.all()
    return wheels


@router.get("/wheels/{wheel_id}", response_model=WheelAssetResponse)
async def get_wheel(wheel_id: int, db: Session = Depends(get_db)):
    wheel = db.query(Asset).filter(
        Asset.id == wheel_id,
        Asset.kind == "wheel"
    ).first()
    
    if not wheel:
        raise HTTPException(status_code=404, detail="Wheel not found")
    
    return wheel


@router.get("/vehicles", response_model=List[VehicleSpecResponse])
async def get_vehicle_specs(
    make: Optional[str] = Query(None, description="Filter by vehicle make"),
    model: Optional[str] = Query(None, description="Filter by vehicle model"),
    year: Optional[int] = Query(None, description="Filter by vehicle year"),
    db: Session = Depends(get_db)
):
    query = db.query(VehicleSpec)
    
    if make:
        query = query.filter(VehicleSpec.make.ilike(f"%{make}%"))
    if model:
        query = query.filter(VehicleSpec.model.ilike(f"%{model}%"))
    if year:
        query = query.filter(VehicleSpec.year == year)
    
    specs = query.all()
    return specs


@router.get("/vehicles/{spec_id}", response_model=VehicleSpecResponse)
async def get_vehicle_spec(spec_id: int, db: Session = Depends(get_db)):
    spec = db.query(VehicleSpec).filter(VehicleSpec.id == spec_id).first()
    
    if not spec:
        raise HTTPException(status_code=404, detail="Vehicle specification not found")
    
    return spec


@router.get("/wheels/compatible")
async def get_compatible_wheels(
    vehicle_spec_id: int,
    db: Session = Depends(get_db)
):
    """Get wheels compatible with a specific vehicle specification"""
    spec = db.query(VehicleSpec).filter(VehicleSpec.id == vehicle_spec_id).first()
    
    if not spec:
        raise HTTPException(status_code=404, detail="Vehicle specification not found")
    
    # Simple compatibility check based on rim diameter
    compatible_wheels = []
    if spec.rim_diameter:
        # Allow wheels within ±1 inch of the specified diameter
        min_diameter = spec.rim_diameter - 1
        max_diameter = spec.rim_diameter + 1
        
        wheels = db.query(Asset).filter(
            Asset.kind == "wheel"
        ).all()
        
        for wheel in wheels:
            # This is a simplified check - in reality you'd need to parse meta_json
            # to get actual wheel specifications
            compatible_wheels.append({
                "id": wheel.id,
                "brand": wheel.brand,
                "model": wheel.model,
                "thumb_url": wheel.thumb_url
            })
    
    return {
        "vehicle_spec": {
            "make": spec.make,
            "model": spec.model,
            "year": spec.year,
            "rim_diameter": spec.rim_diameter
        },
        "compatible_wheels": compatible_wheels
    }
