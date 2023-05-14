"""Layout of the app."""
import datetime
import os

import dash_bootstrap_components as dbc
import plotly.express as px
from dash import dcc, html

from nerv import utility as util


def navbar():
    return dbc.Container(
        dbc.Spinner(
            [
                dbc.Nav(
                    [
                        dbc.NavLink(
                            [
                                html.I(className="bi bi-gear-fill"),
                                dbc.Offcanvas(
                                    id="offcanvas",
                                    title="Settings",
                                    scrollable=True,
                                ),
                            ],
                            id="settings",
                            href="#",
                            className="col-md-1",
                        ),
                        dbc.NavLink("Home", id="home", href="/", className="col-md-1"),
                    ],
                ),
                dcc.Store(id="store", storage_type="local"),
                dcc.Location(id="url"),
                html.Div(id="content"),
            ],
            delay_hide=250,
            delay_show=250,
            fullscreen=True,
            type="grow",
        ),
        fluid=True,
    )


def index_layout(path):
    return dbc.Container(
        [
            dcc.Link(
                [
                    dbc.Card(
                        [
                            html.H5(x),
                            html.P(
                                "Last modified: "
                                + datetime.datetime.fromtimestamp(
                                    os.path.getmtime(os.path.join(path, x))
                                ).strftime("%c"),
                                className="small",
                            ),
                        ],
                        body=True,
                    )
                ],
                href="/" + x,
                id=x,
                className="m-2 col-md-3 text-center",
            )
            for x in os.listdir(path)
        ],
        className="d-flex flex-row flex-wrap justify-content-center align-items-center",
    )


def vis_layout(df):
    """
    Generates the app layout.

    Parameters
    ----------
    df : pandas.core.frame.DataFrame
        Dataframe containing the data for graphs.

    Returns
    -------
    dash_bootstrap_components._components.Container.Container
        The app layout made up of various dash bootstrap components and
        dash core components wrapped with a dash bootstrap componenets
        container component.
    """
    hist_plot = dcc.Graph(
        id="histogram",
        figure=px.histogram(
            df[df["Result"] != -1],
            x="Result",
            color="Dataset-Pipeline",
            color_discrete_map={
                k: v
                for k, v in zip(
                    df["Dataset-Pipeline"].unique().tolist(),
                    df["Color"].unique().tolist(),
                )
            },
            barmode="overlay",
            marginal="rug",
            hover_data=df.columns,
        )
        .update_layout(
            xaxis_title=r"$\text {Hippocampus Volume } (mm^3)$",
            yaxis_title="Count",
            xaxis={
                "rangeslider": {"visible": True},
                "range": [
                    -1000,
                    df["Result"].max() + 1000,
                ],
            },
        )
        .update_xaxes(
            ticks="outside",
            tickwidth=2,
            tickcolor="white",
            ticklen=10,
        ),
        config={"displaylogo": False},
        mathjax=True,
    )

    summary = util.generate_summary(df)

    hist_metadata = html.Div(id="hist-metadata-div")

    hist_tab = dbc.Tab(
        [
            dbc.Row(
                [
                    dbc.Col(hist_plot, width="9"),
                    dbc.Col(
                        [dbc.Row(dbc.Col(summary)), dbc.Row(dbc.Col(hist_metadata))]
                    ),
                ],
            ),
        ],
        label="Distribution Plot",
    )

    x_dropdown = dcc.Dropdown(
        id="x",
        options=[
            {
                "label": k,
                "value": v,
            }
            for k, v in zip(
                df["Dataset-Pipeline"].unique().tolist(),
                df["Dataset-Pipeline"].unique().tolist(),
            )
        ],
        value=df["Dataset-Pipeline"].unique().tolist()[0],
        placeholder="x",
    )

    y_dropdown = dcc.Dropdown(
        id="y",
        options=[
            {
                "label": k,
                "value": v,
            }
            for k, v in zip(
                df["Dataset-Pipeline"].unique().tolist(),
                df["Dataset-Pipeline"].unique().tolist(),
            )
        ],
        value=df["Dataset-Pipeline"].unique().tolist()[-1],
        placeholder="y",
    )

    scatter_plot = dcc.Graph(
        id="scatter",
        figure=px.scatter(
            df,
            x=df[df["Dataset-Pipeline"] == df["Dataset-Pipeline"].unique().tolist()[0]][
                "Result"
            ],
            y=df[
                df["Dataset-Pipeline"] == df["Dataset-Pipeline"].unique().tolist()[-1]
            ]["Result"],
            marginal_x="histogram",
            marginal_y="histogram",
            color_discrete_sequence=px.colors.qualitative.G10[::-1],
        ).update_layout(
            xaxis={"rangeslider": {"visible": True}},
            xaxis_title=df["Dataset-Pipeline"].unique().tolist()[0],
            yaxis_title=df["Dataset-Pipeline"].unique().tolist()[-1],
        ),
        config={"displaylogo": False},
    )

    scatter_metadata = html.Div(id="scatter-metadata-div")

    scatter_tab = dbc.Tab(
        [
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Row([dbc.Col(x_dropdown), dbc.Col(y_dropdown)]),
                            dbc.Row(dbc.Col(scatter_plot)),
                        ],
                        width="9",
                    ),
                    dbc.Col(scatter_metadata),
                ]
            )
        ],
        label="Joint Plot",
    )

    return (
        dbc.Tabs(
            [hist_tab, scatter_tab],
        ),
    )
