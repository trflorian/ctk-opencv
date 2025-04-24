from typing import Protocol

import numpy.typing as npt
import cv2

class Filter(Protocol):
    """
    A protocol for image filters.
    """

    name: str

    def apply(self, frame: npt.NDArray) -> npt.NDArray:
        """
        Apply the filter to the given frame.

        Args:
            frame (np.ndarray): The input image frame.

        Returns:
            np.ndarray: The filtered image frame.
        """
        raise NotImplementedError()


class NormalFilter(Filter):
    """
    A filter that does nothing (identity filter).
    """

    name = "Normal"

    def apply(self, frame: npt.NDArray) -> npt.NDArray:
        return frame


class GrayscaleFilter(Filter):
    """
    A filter that converts the image to grayscale.
    """

    name = "Grayscale"

    def apply(self, frame: npt.NDArray) -> npt.NDArray:
        return cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


class BlurFilter(Filter):
    """
    A filter that applies Gaussian blur to the image.
    """

    name = "Blur"

    def __init__(self, kernel_size: tuple[int, int] = (15, 15)) -> None:
        self.kernel_size = kernel_size

    def apply(self, frame: npt.NDArray) -> npt.NDArray:
        return cv2.GaussianBlur(frame, ksize=self.kernel_size, sigmaX=0)


class ThresholdFilter(Filter):
    """
    A filter that applies binary thresholding to the image.
    """

    name = "Threshold"

    def __init__(self, threshold: int = 127) -> None:
        self.threshold = threshold

    def apply(self, frame: npt.NDArray) -> npt.NDArray:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        _, thresholded_frame = cv2.threshold(
            gray, self.threshold, 255, cv2.THRESH_BINARY
        )
        return thresholded_frame


class CannyFilter(Filter):
    """
    A filter that applies Canny edge detection to the image.
    """

    name = "Canny"

    def __init__(self, threshold1: int = 100, threshold2: int = 200) -> None:
        self.threshold1 = threshold1
        self.threshold2 = threshold2

    def apply(self, frame: npt.NDArray) -> npt.NDArray:
        return cv2.Canny(frame, self.threshold1, self.threshold2)


class SobelFilter(Filter):
    """
    A filter that applies Sobel edge detection to the image.
    """

    name = "Sobel"

    def __init__(self, dx: int = 1, dy: int = 0, ksize: int = 5) -> None:
        self.dx = dx
        self.dy = dy
        self.ksize = ksize

    def apply(self, frame: npt.NDArray) -> npt.NDArray:
        return cv2.Sobel(frame, cv2.CV_64F, self.dx, self.dy, ksize=self.ksize)


class LaplacianFilter(Filter):
    """
    A filter that applies Laplacian edge detection to the image.
    """

    name = "Laplacian"

    def apply(self, frame: npt.NDArray) -> npt.NDArray:
        return cv2.Laplacian(frame, cv2.CV_64F)

class FilterFactory:
    """
    A factory class to create filter instances based on the filter name.
    """

    @staticmethod
    def create_all_filters() -> list[Filter]:
        """
        Create and return a list of all available filters.
        """
        return [
            NormalFilter(),
            GrayscaleFilter(),
            BlurFilter(),
            ThresholdFilter(),
            CannyFilter(),
            SobelFilter(),
            LaplacianFilter(),
        ]