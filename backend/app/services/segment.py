import cv2 as cv
import numpy as np


def grabcut_segment(image_bgr: np.ndarray, rect=None) -> np.ndarray:
	h, w = image_bgr.shape[:2]
	if rect is None:
		rect = (int(0.05 * w), int(0.1 * h), int(0.9 * w), int(0.8 * h))
	mask = np.zeros((h, w), np.uint8)
	bgd = np.zeros((1, 65), np.float64)
	fgd = np.zeros((1, 65), np.float64)
	try:
		cv.grabCut(image_bgr, mask, rect, bgd, fgd, 5, cv.GC_INIT_WITH_RECT)
	except Exception:
		mask[:] = 1
	result = np.where((mask == 2) | (mask == 0), 0, 255).astype(np.uint8)
	return result

