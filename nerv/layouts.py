"""Layout of the app."""
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import dcc, html

from nerv import utility as util


def layout(df):
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

    layout = dbc.Container(
        [
            dbc.Tabs(
                [hist_tab, scatter_tab],
            ),
        ],
        fluid=True,
    )

    return layout
