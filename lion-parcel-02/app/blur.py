import cv2
import numpy as np


def is_blurry(image_bytes: bytes, threshold: float = 100.0) -> bool:
    if not image_bytes:
        raise ValueError("Empty image bytes")

    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_GRAYSCALE)

    if image is None:
        raise ValueError("Failed to decode image")

    variance = cv2.Laplacian(image, cv2.CV_64F).var()
    return variance < threshold
