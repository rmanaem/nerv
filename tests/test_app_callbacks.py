"""Unit tests for app callbacks."""
import pytest

from nerv.utility import get_metadata


@pytest.mark.parametrize(
    "clickData, metadata, x, y",
    [
        ("histogram", "histogram", "prevent-AD-FSL", None),
        ("histogram", "histogram", None, "prevent-AD-FreeSurfer"),
        ("scatter", "scatter", "prevent-AD-FSL", "prevent-AD-FreeSurfer"),
    ],
    indirect=["clickData", "metadata"],
)
def test_get_metadata(metadata, clickData, x, y, df):
    """
    Tests whether get_metadata condition that determines from which graph the
    clickData is coming work as intended.
    It utilizes clickData, metadata, and df fixtures for testing.
    """
    assert metadata == get_metadata(clickData, x, y, df)
