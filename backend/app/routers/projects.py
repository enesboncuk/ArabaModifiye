from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime

from ..database import get_db, Project, User, Image
from ..services.auth import get_current_user

router = APIRouter()


class ProjectCreate(BaseModel):
    title: str


class ProjectUpdate(BaseModel):
    title: Optional[str] = None


class ProjectResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    image_count: int = 0

    class Config:
        from_attributes = True


class ProjectDetailResponse(BaseModel):
    id: int
    title: str
    created_at: datetime
    images: List[dict] = []

    class Config:
        from_attributes = True


@router.post("", response_model=ProjectResponse)
async def create_project(
    project_data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_project = Project(
        title=project_data.title,
        user_id=current_user.id
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    
    return ProjectResponse(
        id=db_project.id,
        title=db_project.title,
        created_at=db_project.created_at,
        image_count=0
    )


@router.get("", response_model=List[ProjectResponse])
async def get_projects(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    projects = db.query(Project).filter(Project.user_id == current_user.id).all()
    
    result = []
    for project in projects:
        image_count = db.query(Image).filter(Image.project_id == project.id).count()
        result.append(ProjectResponse(
            id=project.id,
            title=project.title,
            created_at=project.created_at,
            image_count=image_count
        ))
    
    return result


@router.get("/{project_id}", response_model=ProjectDetailResponse)
async def get_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    images = db.query(Image).filter(Image.project_id == project.id).all()
    image_data = [
        {
            "id": img.id,
            "url": img.url,
            "width": img.width,
            "height": img.height
        }
        for img in images
    ]
    
    return ProjectDetailResponse(
        id=project.id,
        title=project.title,
        created_at=project.created_at,
        images=image_data
    )


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    if project_data.title is not None:
        project.title = project_data.title
    
    db.commit()
    db.refresh(project)
    
    image_count = db.query(Image).filter(Image.project_id == project.id).count()
    return ProjectResponse(
        id=project.id,
        title=project.title,
        created_at=project.created_at,
        image_count=image_count
    )


@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    db.delete(project)
    db.commit()
    
    return {"message": "Project deleted successfully"}
