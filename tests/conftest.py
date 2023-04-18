"""
Test fixtures.
"""
import os

import plotly.express as px
import pytest
from dash.html import H4, A, Br
from dash_bootstrap_components import Accordion, AccordionItem, Card, CardBody

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
def hist_clickData():
    return {
        "points": [
            {
                "curveNumber": 7,
                "pointNumber": 491,
                "pointIndex": 491,
                "x": 3489,
                "y": "some_dataset-pipeline",
                "bbox": {
                    "x0": 484.66,
                    "x1": 490.66,
                    "y0": 127.27,
                    "y1": 133.26999999999998,
                },
                "customdata": [
                    "some_subject",
                    "some_dataset-pipeline",
                    {
                        "first_step": {
                            "inputID": 6435319,
                            "toolConfigID": 678,
                            "taskID": 5616972,
                            "status": "Completed",
                            "outputID": 4283122,
                            "isUsed": True,
                        },
                        "second_step": {
                            "inputID": 4283122,
                            "toolConfigID": 1024,
                            "taskID": 1896642,
                            "status": "Completed",
                            "outputID": 1947652,
                            "isUsed": True,
                        },
                        "third_step": {
                            "inputID": 1947652,
                            "toolConfigID": 1024,
                            "taskID": 8735432,
                            "status": "Completed",
                            "outputID": 1285429,
                            "isUsed": True,
                        },
                        "Result": {"result": "3489", "isUsed": True},
                    },
                    "rgb(59, 115, 143)",
                ],
            }
        ]
    }


@pytest.fixture(scope="session")
def hist_metadata():
    return Card(
        CardBody(
            children=[
                H4(children="Metadata", className="card-title"),
                "Subject: some_subject",
                Br(None),
                "Dataset-Pipeline: some_dataset-pipeline",
                Br(None),
                "Result: 3489",
                Br(None),
                "Pipeline steps:",
                Br(None),
                Br(None),
                Accordion(
                    children=[
                        AccordionItem(
                            children=[
                                "Status: ",
                                "Completed",
                                Br(None),
                                "Input ID: ",
                                A(
                                    children="6435319",
                                    href="https://portal.cbrain.mcgill.ca/userfiles/6435319",
                                ),
                                Br(None),
                                "Output ID: ",
                                A(
                                    children="4283122",
                                    href="https://portal.cbrain.mcgill.ca/userfiles/4283122",
                                ),
                                Br(None),
                                "Task ID: ",
                                A(
                                    children="5616972",
                                    href="https://portal.cbrain.mcgill.ca/tasks/5616972",
                                ),
                                Br(None),
                                "Tool Configuration ID: ",
                                "678",
                            ],
                            title="first_step",
                        )
                    ],
                    start_collapsed=True,
                ),
                Accordion(
                    children=[
                        AccordionItem(
                            children=[
                                "Status: ",
                                "Completed",
                                Br(None),
                                "Input ID: ",
                                A(
                                    children="4283122",
                                    href="https://portal.cbrain.mcgill.ca/userfiles/4283122",
                                ),
                                Br(None),
                                "Output ID: ",
                                A(
                                    children="1947652",
                                    href="https://portal.cbrain.mcgill.ca/userfiles/1947652",
                                ),
                                Br(None),
                                "Task ID: ",
                                A(
                                    children="1896642",
                                    href="https://portal.cbrain.mcgill.ca/tasks/1896642",
                                ),
                                Br(None),
                                "Tool Configuration ID: ",
                                "1024",
                            ],
                            title="second_step",
                        )
                    ],
                    start_collapsed=True,
                ),
                Accordion(
                    children=[
                        AccordionItem(
                            children=[
                                "Status: ",
                                "Completed",
                                Br(None),
                                "Input ID: ",
                                A(
                                    children="1947652",
                                    href="https://portal.cbrain.mcgill.ca/userfiles/1947652",
                                ),
                                Br(None),
                                "Output ID: ",
                                A(
                                    children="1285429",
                                    href="https://portal.cbrain.mcgill.ca/userfiles/1285429",
                                ),
                                Br(None),
                                "Task ID: ",
                                A(
                                    children="8735432",
                                    href="https://portal.cbrain.mcgill.ca/tasks/8735432",
                                ),
                                Br(None),
                                "Tool Configuration ID: ",
                                "1024",
                            ],
                            title="third_step",
                        )
                    ],
                    start_collapsed=True,
                ),
            ],
            className="card-text",
        )
    )


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
