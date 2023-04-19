"""Unit tests for app callbacks."""
import pytest
from plotly.graph_objs import Figure

from nerv.callbacks import plot_scatter_func
from nerv.utility import extract_metadata


@pytest.mark.parametrize(
    "clickData, metadata, x, y",
    [
        ("histogram", "histogram", "prevent-AD-FSL", None),
        ("histogram", "histogram", None, "prevent-AD-FreeSurfer"),
        ("scatter", "scatter", "prevent-AD-FSL", "prevent-AD-FreeSurfer"),
    ],
    indirect=["clickData", "metadata"],
)
def test_extract_metadata(metadata, clickData, x, y, df):
    """
    Tests whether extract_metadata condition that determines from which graph the
    clickData is coming work as intended.
    It utilizes clickData, metadata, and df fixtures for testing.
    """
    assert metadata == extract_metadata(clickData, x, y, df)


@pytest.mark.parametrize(
    "x, y, exp_x, exp_y",
    [
        (None, "prevent-AD-FreeSurfer", "prevent-AD-FSL", "compass-nd-IZK"),
        ("compass-nd-CSM", None, "prevent-AD-FSL", "compass-nd-IZK"),
        (None, None, "prevent-AD-FSL", "compass-nd-IZK"),
        (
            "prevent-AD-FreeSurfer",
            "compass-nd-CSM",
            "prevent-AD-FreeSurfer",
            "compass-nd-CSM",
        ),
    ],
)
def test_plot_scatter_func(x, y, exp_x, exp_y, df):
    """
    Tests whether plot_scatter_func returns an instance of Figure class and
    whether the plot axes are updated properly based on the input.
    It utilizes df fixtures for testing.
    """
    output = plot_scatter_func(x, y, df)
    assert isinstance(output, Figure)
    assert output["layout"]["xaxis"]["title"]["text"] == exp_x
    assert output["layout"]["yaxis"]["title"]["text"] == exp_y
