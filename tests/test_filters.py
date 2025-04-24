import numpy as np

from ctk_opencv.processing.filter import FilterFactory, NormalFilter


def test_filter_factory() -> None:
    """
    Test the FilterFactory class to ensure it creates all filters correctly.
    """
    filters = FilterFactory.create_all_filters()

    # Check that the number of filters created is as expected
    assert len(filters) == 7, "Expected 7 filters to be created"

    # Check that each filter has a name and an apply method
    for filter in filters:
        assert hasattr(filter, "name"), f"Filter {filter} should have a name"
        assert hasattr(filter, "apply"), f"Filter {filter} should have an apply method"


def test_normal_filter() -> None:
    """
    Test the NormalFilter class to ensure it applies the filter correctly.
    """
    normal_filter = NormalFilter()

    # Create a dummy image
    dummy_image = np.zeros((100, 100, 3), dtype=np.uint8)

    # Apply the normal filter
    filtered_image = normal_filter.apply(dummy_image)

    # Check that the filtered image is the same as the input image
    assert np.array_equal(filtered_image, dummy_image), "NormalFilter should return the input image unchanged"
