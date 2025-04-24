import cv2
import numpy as np
import numpy.typing as npt


def convert_any_to_bgr(frame: npt.NDArray) -> npt.NDArray[np.uint8]:
    """
    Convert any image format to BGR format.

    Args:
        frame: The input image frame. Can be float or grayscale.

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
