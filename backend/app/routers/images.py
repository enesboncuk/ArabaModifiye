import os
import uuid
import json
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Form
from fastapi import status
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from ..services.storage import save_upload_file
from ..database import get_db, Image, Project
from ..services.auth import get_current_user, User


router = APIRouter()


@router.post("")
async def upload_image(
    file: UploadFile = File(...),
    project_id: Optional[int] = Form(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Only image uploads are allowed")
    
    # Save file to storage
    path, meta = await save_upload_file(file, subdir="images")
    
    # If project_id is provided, verify ownership and save to database
    if project_id:
        project = db.query(Project).filter(
            Project.id == project_id,
            Project.user_id == current_user.id
        ).first()
        
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        
        # Save image record to database
        db_image = Image(
            project_id=project_id,
            url=path,
            width=meta.get("width"),
            height=meta.get("height"),
            exif=json.dumps(meta) if meta else None
        )
        db.add(db_image)
        db.commit()
        db.refresh(db_image)
        
        return {
            "image_id": db_image.id,
            "image_path": path,
            "meta": meta,
            "project_id": project_id
        }
    
    return {"image_path": path, "meta": meta}


@router.get("/{image_id}")
async def get_image(
    image_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
) -> Dict[str, Any]:
    # Get image and verify ownership through project
    image = db.query(Image).join(Project).filter(
        Image.id == image_id,
        Project.user_id == current_user.id
    ).first()
    
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    
    return {
        "id": image.id,
        "url": image.url,
        "width": image.width,
        "height": image.height,
        "project_id": image.project_id
    }


@router.delete("/{image_id}")
async def delete_image(
    image_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get image and verify ownership through project
    image = db.query(Image).join(Project).filter(
        Image.id == image_id,
        Project.user_id == current_user.id
    ).first()
    
    if not image:
        raise HTTPException(status_code=404, detail="Image not found")
    
    # Delete file from storage (optional - you might want to keep files)
    # os.remove(image.url) if os.path.exists(image.url) else None
    
    # Delete from database
    db.delete(image)
    db.commit()
    
    return {"message": "Image deleted successfully"}

