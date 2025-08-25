from typing import List, Tuple, Dict, Any
from pydantic import BaseModel, Field
from fastapi import APIRouter, HTTPException

from ..services.segment import grabcut_segment
from ..services.recolor import recolor_hsv
from ..services.overlay import overlay_wheel
from ..services.storage import read_image_bgr_or_bgra, save_image_np, ensure_path_exists


router = APIRouter()


class Point(BaseModel):
	x: float
	y: float


class SegmentRequest(BaseModel):
	image_path: str = Field(..., description="Path returned from upload endpoint")


class RecolorRequest(BaseModel):
	image_path: str
	mask_path: str
	dh: int = 0
	ds: float = 0.0
	dv: float = 0.0


class OverlayWheelRequest(BaseModel):
	base_image_path: str
	wheel_image_path: str
	dst_pts: List[Point] = Field(..., min_items=4, max_items=4)


@router.post("/segment")
def segment_body(req: SegmentRequest) -> Dict[str, Any]:
	image = read_image_bgr_or_bgra(req.image_path)
	if image is None:
		raise HTTPException(status_code=400, detail="image_path not found or unreadable")
	mask = grabcut_segment(image)
	out_path = save_image_np(mask, subdir="masks", force_gray=True)
	return {"mask_path": out_path}


@router.post("/recolor")
def recolor(req: RecolorRequest) -> Dict[str, Any]:
	image = read_image_bgr_or_bgra(req.image_path)
	mask = read_image_bgr_or_bgra(req.mask_path, prefer_gray=True)
	if image is None or mask is None:
		raise HTTPException(status_code=400, detail="image_path or mask_path unreadable")
	result = recolor_hsv(image, mask, dh=req.dh, ds=req.ds, dv=req.dv)
	out_path = save_image_np(result, subdir="variants")
	return {"image_path": out_path}


@router.post("/overlay/wheel")
def overlay_wheel_api(req: OverlayWheelRequest) -> Dict[str, Any]:
	base = read_image_bgr_or_bgra(req.base_image_path)
	wheel = read_image_bgr_or_bgra(req.wheel_image_path, keep_alpha=True)
	if base is None or wheel is None:
		raise HTTPException(status_code=400, detail="base_image_path or wheel_image_path unreadable")
	h, w = wheel.shape[:2]
	src_pts = [(0, 0), (w - 1, 0), (w - 1, h - 1), (0, h - 1)]
	dst_pts = [(p.x, p.y) for p in req.dst_pts]
	result = overlay_wheel(base, wheel, src_pts, dst_pts)
	out_path = save_image_np(result, subdir="variants")
	return {"image_path": out_path}

