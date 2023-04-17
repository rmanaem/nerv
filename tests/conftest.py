"""
Test fixtures.
"""
import os

import plotly.express as px
import pytest

from nerv.utility import process_files


@pytest.fixture(scope="session")
def path():
    """
    Provides the path of directory containing test data.

    Returns
    -------
    str
        Path of directory containing test data.
    """
    test_dir = os.path.dirname(os.path.abspath(__file__))
    print("Using", os.path.join(test_dir, "data"), "as the path for app")
    yield os.path.join(test_dir, "data")


@pytest.fixture(scope="session")
def df(path):
    """
    Provides a dataframe containing test data.
    It utilizes process_files function to generate
    the dataframe.

    Returns
    -------
    pandas.core.frame.DataFrame
        A dataframe containing test data.
    """

    yield process_files(path)


@pytest.fixture(scope="session")
def histogram(data):
    return px.histogram(data[data["Result"] != -1], x="Result", template="plotly_dark")


@pytest.fixture(scope="session")
def scatter(data):
    return px.scatter(
        data,
        x=data[
            data["Dataset-Pipeline"] == data["Dataset-Pipeline"].unique().tolist()[0]
        ]["Result"],
        y=data[
            data["Dataset-Pipeline"] == data["Dataset-Pipeline"].unique().tolist()[-1]
        ]["Result"],
        template="plotly_dark",
    )
