import numpy as np

from ctk_opencv.processing.utils import convert_any_to_bgr


def test_convert_float_to_bgr() -> None:
    """
    Test the convert_any_to_bgr function with a float image.
    """
    # Create a float image
    float_image = np.random.rand(100, 100, 3).astype(np.float32) * 255

    # Convert the float image to BGR format
    bgr_image = convert_any_to_bgr(float_image)

    # Check the data type of the converted image
    assert bgr_image.dtype == np.uint8, "The converted image should be of type uint8"
    assert bgr_image.shape == (
        100,
        100,
        3,
    ), "The converted image should have the same shape as the input image"


def test_convert_gray_to_bgr() -> None:
    """
    Test the convert_any_to_bgr function with a grayscale image.
    """
    # Create a grayscale image
    gray_image = np.random.rand(100, 100) * 255
    gray_image = gray_image.astype(np.uint8)

    # Convert the grayscale image to BGR format
    bgr_image = convert_any_to_bgr(gray_image)

    # Check the data type of the converted image
    assert bgr_image.dtype == np.uint8, "The converted image should be of type uint8"
    assert bgr_image.shape == (
        100,
        100,
        3,
    ), "The converted image should have the same shape as the input image"
