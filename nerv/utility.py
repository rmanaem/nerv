"""Utility functions and constants of the app."""
import json
import os

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import html

colors = [
    px.colors.qualitative.G10,
    px.colors.sequential.Teal,
    px.colors.sequential.Brwnyl,
    px.colors.sequential.Burg,
    px.colors.sequential.Purp,
]


def pull_files(path):
    files = []
    for i in os.listdir(path):
        if i[-5:] == ".json":
            files.append((path + "/" + i, i[: len(i) - 5]))
    return files


def process_file(file, color):
    data = None
    with open(file[0], "r") as dataset:
        data = json.load(dataset)
    x = []
    for k in data.keys():
        z = len(colors[color]) - 1
        for v in data[k].keys():
            x.append(
                (k, v, data[k][v]["Result"]["result"], data[k][v], colors[color][z])
            )
            z -= 1
    x = [
        (i[0], i[1], -1, i[3], i[4])
        if i[2] is None
        else (i[0], i[1], float(i[2]), i[3], i[4])
        for i in x
    ]
    df = pd.DataFrame(
        {
            "Subject": [i[0] for i in x],
            "Dataset-Pipeline": [file[1] + "-" + i[1] for i in x],
            "Result": [i[2] for i in x],
            "Info": [i[3] for i in x],
            "Color": [i[4] for i in x],
        }
    )
    return df


def process_files(path):
    files = pull_files(path)
    dfs = []
    for i, j in enumerate(files):
        dfs.append(process_file(j, i))
    return pd.concat(dfs)


def pull_directories(path):
    files = []
    for directory in os.listdir(path):
        files.append((directory, pull_files(os.path.join(path, directory)), []))
    for i in files:
        for z, w in enumerate(i[1]):
            i[2].append(process_file(w, z))
    return [(i[0], pd.concat(i[2])) for i in files]


def generate_summary(df):
    total = str(df.shape[0])
    missing = str(df[df["Result"] == -1].shape[0])
    header = html.H4("Summary", className="card-title")
    summary = [
        header,
        "Total number of datapoints: " + total,
        html.Br(),
        "Total number of missing datapoints: " + missing,
        html.Br(),
    ]
    pipelines = df["Dataset-Pipeline"].unique().tolist()
    for p in pipelines:
        s = (
            p
            + ": "
            + str(df[(df["Dataset-Pipeline"] == p) & (df["Result"] == -1)].shape[0])
        )
        summary.append(s)
        summary.append(html.Br())

    return dbc.Card(dbc.CardBody(summary, className="card-text"))
