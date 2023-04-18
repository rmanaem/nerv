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
    """Tests get_metadata function using clickData, metadata, and df fixtures"""
    assert metadata == get_metadata(clickData, x, y, df)
