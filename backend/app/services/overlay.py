import cv2 as cv
import numpy as np
from typing import List, Tuple


def overlay_wheel(base_bgr: np.ndarray, wheel_bgra: np.ndarray, src_pts: List[Tuple[float, float]], dst_pts: List[Tuple[float, float]]) -> np.ndarray:
	H, status = cv.findHomography(np.array(src_pts, dtype=np.float32), np.array(dst_pts, dtype=np.float32))
	h, w = base_bgr.shape[:2]
	warped = cv.warpPerspective(wheel_bgra, H, (w, h), flags=cv.INTER_LINEAR, borderMode=cv.BORDER_TRANSPARENT)
	alpha = warped[..., 3:4] / 255.0
	base = base_bgr.astype(np.float32)
	wheel_rgb = warped[..., :3].astype(np.float32)
	result = (base * (1.0 - alpha) + wheel_rgb * alpha).astype(np.uint8)
	return result

