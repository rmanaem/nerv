"""
Test fixtures.
"""
import os

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


@pytest.fixture()
def clickData(request):
    if request.param == "histogram":
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
    else:
        return {
            "points": [
                {
                    "curveNumber": 0,
                    "pointNumber": 145,
                    "pointIndex": 145,
                    "x": 16709,
                    "y": 3703,
                    "bbox": {"x0": 901.12, "x1": 903.12, "y0": 396.842, "y1": 398.842},
                }
            ]
        }
