from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, ForeignKey, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.sql import func
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./arabamodifiye.db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    projects = relationship("Project", back_populates="user")


class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    title = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="projects")
    images = relationship("Image", back_populates="project")


class Image(Base):
    __tablename__ = "images"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), nullable=False)
    url = Column(String, nullable=False)
    width = Column(Integer)
    height = Column(Integer)
    exif = Column(Text)  # JSON string
    
    project = relationship("Project", back_populates="images")
    masks = relationship("Mask", back_populates="image")
    variants = relationship("Variant", back_populates="image")


class Mask(Base):
    __tablename__ = "masks"
    
    id = Column(Integer, primary_key=True, index=True)
    image_id = Column(Integer, ForeignKey("images.id"), nullable=False)
    kind = Column(String, nullable=False)  # body, wheel, etc.
    url = Column(String, nullable=False)
    
    image = relationship("Image", back_populates="masks")


class Variant(Base):
    __tablename__ = "variants"
    
    id = Column(Integer, primary_key=True, index=True)
    image_id = Column(Integer, ForeignKey("images.id"), nullable=False)
    description = Column(String)
    url = Column(String, nullable=False)
    layers_json = Column(Text)  # JSON string for layer information
    
    image = relationship("Image", back_populates="variants")


class Asset(Base):
    __tablename__ = "assets"
    
    id = Column(Integer, primary_key=True, index=True)
    kind = Column(String, nullable=False)  # wheel, spoiler, paint
    brand = Column(String)
    model = Column(String)
    meta_json = Column(Text)  # JSON string for metadata
    thumb_url = Column(String)
    file_url = Column(String)


class VehicleSpec(Base):
    __tablename__ = "vehicle_specs"
    
    id = Column(Integer, primary_key=True, index=True)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    trim = Column(String)
    bolt_pattern = Column(String)
    rim_diameter = Column(Float)  # inches
    rim_width = Column(Float)     # inches
    offset = Column(Float)        # mm
    center_bore = Column(Float)   # mm


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    Base.metadata.create_all(bind=engine)
