import cv2
import numpy as np


def convert_any_to_bgr(frame: np.ndarray) -> np.ndarray:
    """
    Convert any image format to BGR format.

    Args:
        frame: The input image frame.

    Returns:
        The converted image in BGR format.
    """
    if frame.dtype != np.uint8:
        # Scale the frame to uint8 if necessary
        cv2.normalize(frame, frame, 0, 255, cv2.NORM_MINMAX)
        frame = frame.astype(np.uint8)

    if len(frame.shape) == 2:
        # If the frame is grayscale, convert it to BGR
        frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)

    return frame
