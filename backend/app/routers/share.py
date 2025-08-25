import secrets
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel

from ..database import get_db, Project, Image, Variant
from ..services.auth import get_current_user, User

router = APIRouter()


class ShareProjectRequest(BaseModel):
    project_id: int
    public: bool = True


class ShareResponse(BaseModel):
    slug: str
    public_url: str


class SharedProjectResponse(BaseModel):
    title: str
    images: list
    variants: list


@router.post("/projects", response_model=ShareResponse)
async def share_project(
    share_data: ShareProjectRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if project exists and belongs to user
    project = db.query(Project).filter(
        Project.id == share_data.project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Generate unique slug
    slug = secrets.token_urlsafe(16)
    
    # In a real implementation, you'd store this in a separate table
    # For now, we'll just return the slug
    # You could also store it in the project table or create a separate sharing table
    
    base_url = "http://localhost:3000"  # This should come from environment
    public_url = f"{base_url}/share/{slug}"
    
    return ShareResponse(slug=slug, public_url=public_url)


@router.get("/{slug}", response_model=SharedProjectResponse)
async def get_shared_project(slug: str, db: Session = Depends(get_db)):
    # In a real implementation, you'd look up the slug in a sharing table
    # For now, we'll return a mock response
    # This is where you'd implement the actual sharing logic
    
    # Mock data for demonstration
    # In reality, you'd query the database based on the slug
    
    return SharedProjectResponse(
        title="Shared Project",
        images=[
            {
                "id": 1,
                "url": "/media/images/sample.jpg",
                "width": 800,
                "height": 600
            }
        ],
        variants=[
            {
                "id": 1,
                "description": "Modified version",
                "url": "/media/variants/sample_modified.jpg"
            }
        ]
    )


@router.delete("/projects/{project_id}")
async def unshare_project(
    project_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check if project exists and belongs to user
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # In a real implementation, you'd remove the sharing record
    # For now, just return success
    
    return {"message": "Project unshared successfully"}
