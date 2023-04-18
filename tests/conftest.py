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


@pytest.fixture()
def metadata(request):
    if request.param == "histogram":
        return {
            "subject": "some_subject",
            "dataset-pipeline": "some_dataset-pipeline",
            "result": "3489",
            "first_step": {
                "status": "Completed",
                "inputID": "6435319",
                "outputID": "4283122",
                "taskID": "5616972",
                "toolConfigID": "678",
            },
            "second_step": {
                "status": "Completed",
                "inputID": "4283122",
                "outputID": "1947652",
                "taskID": "1896642",
                "toolConfigID": "1024",
            },
            "third_step": {
                "status": "Completed",
                "inputID": "1947652",
                "outputID": "1285429",
                "taskID": "8735432",
                "toolConfigID": "1024",
            },
        }
    else:
        return {
            "x": {
                "subject": "sub-2017146_ses-NAPFU48_run-002_T1w.nii.gz",
                "dataset-pipeline": "prevent-AD-FSL",
                "result": "16709",
                "FSL_First": {
                    "status": "Completed",
                    "inputID": "3680817",
                    "outputID": "3681957",
                    "taskID": "1888425",
                    "toolConfigID": "721",
                },
                "Subfolder_File_Extractor_FSL": {
                    "status": "Completed",
                    "inputID": "3681957",
                    "outputID": "3682428",
                    "taskID": "1889025",
                    "toolConfigID": "2094",
                },
                "FSL_Stats": {
                    "status": "Completed",
                    "inputID": "3682428",
                    "outputID": "3682749",
                    "taskID": "1889307",
                    "toolConfigID": "1698",
                },
            },
            "y": {
                "subject": "sub-2017146_ses-NAPFU48_run-002_T1w.nii.gz",
                "dataset-pipeline": "prevent-AD-FreeSurfer",
                "result": "Result: 3703",
                "FreeSurfer_Recon_all": {
                    "status": "Completed",
                    "inputID": "3680817",
                    "outputID": "3683955",
                    "taskID": "1888725",
                    "toolConfigID": "583",
                },
                "Subfolder_File_Extractor_FreeSurfer_1": {
                    "status": "Completed",
                    "inputID": "3683955",
                    "outputID": "3684015",
                    "taskID": "1890132",
                    "toolConfigID": "2094",
                },
                "Subfolder_File_Extractor_FreeSurfer_2": {
                    "status": "Completed",
                    "inputID": "3684015",
                    "outputID": "3684129",
                    "taskID": "1890222",
                    "toolConfigID": "2094",
                },
            },
        }
