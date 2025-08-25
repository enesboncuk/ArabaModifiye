import os
import uuid
from typing import Tuple, Dict, Any, Optional
import aiofiles
import cv2 as cv
import numpy as np
from fastapi import UploadFile


BASE_MEDIA_DIR = os.path.join("media")


def ensure_path_exists(path: str) -> None:
	dirname = os.path.dirname(path)
	if dirname and not os.path.exists(dirname):
		os.makedirs(dirname, exist_ok=True)


async def save_upload_file(file: UploadFile, subdir: str = "") -> Tuple[str, Dict[str, Any]]:
	uid = str(uuid.uuid4())
	ext = os.path.splitext(file.filename or "upload")[-1].lower()
	if ext not in [".jpg", ".jpeg", ".png", ".webp", ".bmp"]:
		ext = ".png"
	out_dir = os.path.join(BASE_MEDIA_DIR, subdir)
	os.makedirs(out_dir, exist_ok=True)
	out_path = os.path.join(out_dir, f"{uid}{ext}")
	async with aiofiles.open(out_path, "wb") as f:
		content = await file.read()
		await f.write(content)
	# try to read as image to get meta
	img = cv.imdecode(np.frombuffer(content, dtype=np.uint8), cv.IMREAD_UNCHANGED)
	meta: Dict[str, Any] = {}
	if img is not None:
		h, w = img.shape[:2]
		meta = {"width": w, "height": h, "channels": img.shape[2] if len(img.shape) == 3 else 1}
	return out_path.replace("\\", "/"), meta


def read_image_bgr_or_bgra(path: str, keep_alpha: bool = False, prefer_gray: bool = False) -> Optional[np.ndarray]:
	if not os.path.exists(path):
		return None
	flag = cv.IMREAD_UNCHANGED
	img = cv.imread(path, flag)
	if img is None:
		return None
	if prefer_gray:
		if img.ndim == 3:
			img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
		return img
	if keep_alpha and img.ndim == 3 and img.shape[2] == 4:
		return img
	if img.ndim == 2:
		img = cv.cvtColor(img, cv.COLOR_GRAY2BGR)
	elif img.shape[2] == 4 and not keep_alpha:
		img = img[..., :3]
	return img


def save_image_np(image: np.ndarray, subdir: str = "", filename: Optional[str] = None, force_gray: bool = False) -> str:
	out_dir = os.path.join(BASE_MEDIA_DIR, subdir)
	os.makedirs(out_dir, exist_ok=True)
	uid = filename or str(uuid.uuid4())
	path = os.path.join(out_dir, f"{uid}.png")
	if force_gray and image.ndim == 3:
		image = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
	cv.imwrite(path, image)
	return path.replace("\\", "/")

