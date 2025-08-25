import cv2 as cv
import numpy as np


def recolor_hsv(image_bgr: np.ndarray, mask: np.ndarray, dh: int = 0, ds: float = 0.0, dv: float = 0.0) -> np.ndarray:
	if mask.ndim == 3:
		mask = cv.cvtColor(mask, cv.COLOR_BGR2GRAY)
	mask_bin = (mask > 0).astype(np.uint8) * 255
	hsv = cv.cvtColor(image_bgr, cv.COLOR_BGR2HSV).astype(np.float32)
	h, s, v = cv.split(hsv)
	h = (h + dh) % 180
	s = np.clip(s * (1.0 + ds), 0, 255)
	v = np.clip(v * (1.0 + dv), 0, 255)
	hsv2 = cv.merge([h, s, v]).astype(np.uint8)
	recolored = cv.cvtColor(hsv2, cv.COLOR_HSV2BGR)
	mask3 = cv.merge([mask_bin, mask_bin, mask_bin])
	out = np.where(mask3 > 0, recolored, image_bgr)
	return out

