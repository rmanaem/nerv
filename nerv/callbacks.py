"""
Logic of app callback functions.
"""
import dash
import dash_bootstrap_components as dbc
import plotly.express as px
from dash import html

from nerv.utility import extract_metadata


def hist_click_func(clickData):
    """
    Processes data from the histogram graph click event and creates
    UI elements to display the metadata.

    Parameters
    ----------
    clickData : dict
        Data from latest histogram graph click event.

    Returns
    ----------
    dash._callback.Noupdate or dash_bootstrap_components._components.Card.Card
        No dash update if clickData is None otherwise, structured and styled
        metadata to be displayed in hist-metadata-div.
    """
    if not clickData:
        return dash.no_update

    metadata = extract_metadata(clickData)

    card_body_content = [
        html.H4("Metadata", className="card-title"),
        "Subject: " + metadata["subject"],
        html.Br(),
        "Dataset-Pipeline: " + metadata["dataset-pipeline"],
        html.Br(),
        "Result: " + metadata["result"],
        html.Br(),
        "Pipeline steps: ",
        html.Br(),
        html.Br(),
    ]

    for k, v in list(metadata.items())[3:]:
        card_body_content.append(
            dbc.Accordion(
                [
                    dbc.AccordionItem(
                        [
                            "Status: " + v["status"],
                            html.Br(),
                            "Input ID: ",
                            v["inputID"]
                            if v["inputID"] == "N/A"
                            else html.A(
                                str(v["inputID"]),
                                href="https://portal.cbrain.mcgill.ca/userfiles/"
                                + str(v["inputID"]),
                            ),
                            html.Br(),
                            "Output ID: ",
                            v["outputID"]
                            if v["outputID"] == "N/A"
                            else html.A(
                                str(v["outputID"]),
                                href="https://portal.cbrain.mcgill.ca/userfiles/"
                                + str(v["outputID"]),
                            ),
                            html.Br(),
                            "Task ID: ",
                            v["taskID"]
                            if v["taskID"] == "N/A"
                            else html.A(
                                str(v["taskID"]),
                                href="https://portal.cbrain.mcgill.ca/tasks/"
                                + str(v["taskID"]),
                            ),
                            html.Br(),
                            "Tool Configuration ID: " + v["toolConfigID"],
                        ],
                        title=k,
                    )
                ],
                start_collapsed=True,
            )
        )

    return dbc.Card(dbc.CardBody(card_body_content, className="card-text"))


def plot_scatter_func(x, y, df):
    """
    Creates a scatter plot figure.
    If x or y is None, it uses the first and last dataset-pipeline
    in the dataframe as x and y.

    Parameters
    ----------
        x : str
            Name of the x-axis dataset-pipeline.
        y : str
            Name of the y-axis dataset-pipeline.
        df : pandas.core.frame.DataFrame
            Dataframe containing the data.

    Returns
    ----------
    plotly.graph_objs._figure.Figure
        A plotly graph figure object for the scatter plot
        where x and y inputs are the axes.
    """
    if not x or not y:
        return px.scatter(
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
        )
    else:
        return px.scatter(
            df,
            x=df[df["Dataset-Pipeline"] == x]["Result"],
            y=df[df["Dataset-Pipeline"] == y]["Result"],
            marginal_x="histogram",
            marginal_y="histogram",
            color_discrete_sequence=px.colors.qualitative.G10[::-1],
        ).update_layout(
            xaxis={"rangeslider": {"visible": True}}, xaxis_title=x, yaxis_title=y
        )


def scatter_click_func(clickData, x, y, df):
    """
    Processes data from the scatter plot graph click event and creates
    UI elements to display the metadata.
    If x or y is None, it uses the first and last dataset-pipeline
    in the dataframe as x and y.

    Parameters
    ----------
    clickData : dict
        Data from latest histogram graph click event.
    x : str
        Name of the x-axis dataset-pipeline.
    y : str
        Name of the y-axis dataset-pipeline.
    df : pandas.core.frame.DataFrame
            Dataframe containing the data.

    Returns
    ----------
    dash._callback.Noupdate or dash_bootstrap_components._components.Card.Card
        No dash update if clickData is None otherwise, structured and styled
        metadata to be displayed in scatter-metadata-div.
    """
    if not clickData:
        return dash.no_update

    elif not x or not y:
        xys = df["Dataset-Pipeline"].unique().tolist()
        x, y = xys[0], xys[-1]

    metadata = extract_metadata(clickData, x, y, df)
    card_body_content = [
        html.H4("Metadata", className="card-title"),
        "Subject: " + metadata["x"]["subject"],
        html.Br(),
        "Dataset-Pipeline: " + metadata["x"]["dataset-pipeline"],
        html.Br(),
        "Result: " + metadata["x"]["result"],
        html.Br(),
        "Pipeline steps: ",
        html.Br(),
        html.Br(),
    ]

    for k, v in list(metadata["x"].items())[3:]:
        card_body_content.append(
            dbc.Accordion(
                [
                    dbc.AccordionItem(
                        [
                            "Status: " + v["status"],
                            html.Br(),
                            "Input ID: ",
                            v["inputID"]
                            if v["inputID"] == "N/A"
                            else html.A(
                                str(v["inputID"]),
                                href="https://portal.cbrain.mcgill.ca/userfiles/"
                                + str(v["inputID"]),
                            ),
                            html.Br(),
                            "Output ID: ",
                            v["outputID"]
                            if v["outputID"] == "N/A"
                            else html.A(
                                str(v["outputID"]),
                                href="https://portal.cbrain.mcgill.ca/userfiles/"
                                + str(v["outputID"]),
                            ),
                            html.Br(),
                            "Task ID: ",
                            v["taskID"]
                            if v["taskID"] == "N/A"
                            else html.A(
                                str(v["taskID"]),
                                href="https://portal.cbrain.mcgill.ca/tasks/"
                                + str(v["taskID"]),
                            ),
                            html.Br(),
                            "Tool Configuration ID: " + v["toolConfigID"],
                        ],
                        title=k,
                    )
                ],
                start_collapsed=True,
            )
        )

    card_body_content += [
        html.Br(),
        "Subject: " + metadata["y"]["subject"],
        html.Br(),
        "Dataset-Pipeline: " + metadata["y"]["dataset-pipeline"],
        html.Br(),
        "Result: " + metadata["y"]["result"],
        html.Br(),
        "Pipeline steps: ",
        html.Br(),
        html.Br(),
    ]
    for k, v in list(metadata["y"].items())[3:]:
        card_body_content.append(
            dbc.Accordion(
                [
                    dbc.AccordionItem(
                        [
                            "Status: " + v["status"],
                            html.Br(),
                            "Input ID: ",
                            v["inputID"]
                            if v["inputID"] == "N/A"
                            else html.A(
                                str(v["inputID"]),
                                href="https://portal.cbrain.mcgill.ca/userfiles/"
                                + str(v["inputID"]),
                            ),
                            html.Br(),
                            "Output ID: ",
                            v["outputID"]
                            if v["outputID"] == "N/A"
                            else html.A(
                                str(v["outputID"]),
                                href="https://portal.cbrain.mcgill.ca/userfiles/"
                                + str(v["outputID"]),
                            ),
                            html.Br(),
                            "Task ID: ",
                            v["taskID"]
                            if v["taskID"] == "N/A"
                            else html.A(
                                str(v["taskID"]),
                                href="https://portal.cbrain.mcgill.ca/tasks/"
                                + str(v["taskID"]),
                            ),
                            html.Br(),
                            "Tool Configuration ID: " + v["toolConfigID"],
                        ],
                        title=k,
                    )
                ],
                start_collapsed=True,
            )
        )

    return dbc.Card(dbc.CardBody(card_body_content, className="card-text"))
