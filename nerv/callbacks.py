import dash
import plotly.express as px
from dash import html


def switch_template_func(value):
    template = template1 if value else template2
    if value:
        return (
            px.histogram(
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
                template=template,
                xaxis={
                    "rangeslider": {"visible": True},
                    "range": [-1000, df["Result"].max() + 1000],
                },
            )
            .update_xaxes(ticks="outside", tickwidth=2, tickcolor="#f8f9fa", ticklen=10)
        )

    else:
        return (
            px.histogram(
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
                template=template,
                xaxis={
                    "rangeslider": {"visible": True},
                    "range": [-1000, df["Result"].max() + 1000],
                },
            )
            .update_xaxes(ticks="outside", tickwidth=2, tickcolor="#343a40", ticklen=10)
        )


def histogram_click_func(clickData):
    if not clickData:
        return dash.no_update
    subject = "Subject: " + clickData["points"][0]["customdata"][0]
    pipeline = "Pipeline: " + clickData["points"][0]["y"]
    result = (
        "Result: N/A"
        if clickData["points"][0]["x"] == -1
        else "Result: " + str(clickData["points"][0]["x"])
    )
    header = html.H4("Information", style={"textAlign": "center"})
    info = [header, subject, html.Br(), pipeline, html.Br(), result, html.Br()]

    for k, v in list(clickData["points"][0]["customdata"][2].items())[:-1]:
        status = "Incomplete" if v["status"] is None else v["status"]
        inp = (
            "N/A"
            if v["inputID"] is None
            else html.A(
                str(v["inputID"]),
                href="https://portal.cbrain.mcgill.ca/userfiles/" + str(v["inputID"]),
                style={"color": "#4673a3"},
            )
        )
        out = (
            "N/A"
            if v["outputID"] is None
            else html.A(
                str(v["outputID"]),
                href="https://portal.cbrain.mcgill.ca/userfiles/" + str(v["outputID"]),
                style={"color": "#4673a3"},
            )
        )
        task = (
            "N/A"
            if v["taskID"] is None
            else html.A(
                str(v["taskID"]),
                href="https://portal.cbrain.mcgill.ca/tasks/inser_ID_here"
                + str(v["taskID"]),
                style={"color": "#4673a3"},
            )
        )
        config = "N/A" if v["toolConfigID"] is None else str(v["toolConfigID"])
        step = html.Details(
            [
                html.Summary(k),
                "Status: " + status,
                html.Br(),
                "Input ID: ",
                inp,
                html.Br(),
                "Output ID: ",
                out,
                html.Br(),
                "Task ID: ",
                task,
                html.Br(),
                "Tool Configuration ID: " + config,
            ]
        )
        info.append(step)

    return html.Div(
        html.P(info, style={"margin-left": "10px", "word-wrap": "break-word"}),
        style={
            "width": "90%",
            "box-shadow": "rgba(0, 0, 0, 0.25) 0px 14px 28px, rgba(0, 0, 0, 0.22) 0px 10px 10px",
            "border-radius": "7px",
            "border": "0.25px solid",
        },
    )


def plot_scatter_func(x, y, value):
    template = template1 if value else template2
    if not x or not y:
        if value:
            return px.scatter(
                df,
                x=df[
                    df["Dataset-Pipeline"]
                    == df["Dataset-Pipeline"].unique().tolist()[0]
                ]["Result"],
                y=df[
                    df["Dataset-Pipeline"]
                    == df["Dataset-Pipeline"].unique().tolist()[-1]
                ]["Result"],
                marginal_x="histogram",
                marginal_y="histogram",
                template=template,
                color_discrete_sequence=px.colors.qualitative.G10[::-1],
            ).update_layout(
                xaxis={"rangeslider": {"visible": True}},
                xaxis_title=df["Dataset-Pipeline"].unique().tolist()[0],
                yaxis_title=df["Dataset-Pipeline"].unique().tolist()[-1],
            )
        else:
            return px.scatter(
                df,
                x=df[
                    df["Dataset-Pipeline"]
                    == df["Dataset-Pipeline"].unique().tolist()[0]
                ]["Result"],
                y=df[
                    df["Dataset-Pipeline"]
                    == df["Dataset-Pipeline"].unique().tolist()[-1]
                ]["Result"],
                marginal_x="histogram",
                marginal_y="histogram",
                template=template,
                color_discrete_sequence=px.colors.qualitative.G10[::-1],
            ).update_layout(
                xaxis={"rangeslider": {"visible": True}},
                xaxis_title=df["Dataset-Pipeline"].unique().tolist()[0],
                yaxis_title=df["Dataset-Pipeline"].unique().tolist()[-1],
            )
    else:
        if value:
            return px.scatter(
                df,
                x=df[df["Dataset-Pipeline"] == x]["Result"],
                y=df[df["Dataset-Pipeline"] == y]["Result"],
                marginal_x="histogram",
                marginal_y="histogram",
                template=template,
                color_discrete_sequence=px.colors.qualitative.G10[::-1],
            ).update_layout(
                xaxis={"rangeslider": {"visible": True}},
                xaxis_title=x,
                yaxis_title=y,
            )
        else:
            return px.scatter(
                df,
                x=df[df["Dataset-Pipeline"] == x]["Result"],
                y=df[df["Dataset-Pipeline"] == y]["Result"],
                marginal_x="histogram",
                marginal_y="histogram",
                template=template,
                color_discrete_sequence=px.colors.qualitative.G10[::-1],
            ).update_layout(
                xaxis={"rangeslider": {"visible": True}},
                xaxis_title=x,
                yaxis_title=y,
            )


def scatter_click_func(clickData, x, y):
    if not clickData:
        return dash.no_update

    header = html.H4("Information", style={"textAlign": "center"})
    x_subject = (
        "Subject: "
        + df[
            (df["Dataset-Pipeline"] == x)
            & (df["Result"] == clickData["points"][0]["x"])
        ]["Subject"].iloc[0]
    )
    x_pipeline = "Pipeline: " + x
    x_result = (
        "Result: N/A"
        if clickData["points"][0]["x"] == -1
        else "Result: " + str(clickData["points"][0]["x"])
    )
    info = [
        header,
        x_subject,
        html.Br(),
        x_pipeline,
        html.Br(),
        x_result,
        html.Br(),
    ]
    x_info = df[
        (df["Dataset-Pipeline"] == x) & (df["Result"] == clickData["points"][0]["x"])
    ]["Info"].iloc[0]
    for k, v in list(x_info.items())[:-1]:
        status = "Incomplete" if v["status"] is None else v["status"]
        inp = (
            "N/A"
            if v["inputID"] is None
            else html.A(
                str(v["inputID"]),
                href="https://portal.cbrain.mcgill.ca/userfiles/" + str(v["inputID"]),
                style={"color": "#4673a3"},
            )
        )
        out = (
            "N/A"
            if v["outputID"] is None
            else html.A(
                str(v["outputID"]),
                href="https://portal.cbrain.mcgill.ca/userfiles/" + str(v["outputID"]),
                style={"color": "#4673a3"},
            )
        )
        task = (
            "N/A"
            if v["taskID"] is None
            else html.A(
                str(v["taskID"]),
                href="https://portal.cbrain.mcgill.ca/tasks/inser_ID_here"
                + str(v["taskID"]),
                style={"color": "#4673a3"},
            )
        )
        config = "N/A" if v["toolConfigID"] is None else str(v["toolConfigID"])
        step = html.Details(
            [
                html.Summary(k),
                "Status: " + status,
                html.Br(),
                "Input ID: ",
                inp,
                html.Br(),
                "Output ID: ",
                out,
                html.Br(),
                "Task ID: ",
                task,
                html.Br(),
                "Tool Configuration ID: " + config,
            ]
        )
        info.append(step)

    y_subject = (
        "Subject: "
        + df[
            (df["Dataset-Pipeline"] == y)
            & (df["Result"] == clickData["points"][0]["y"])
        ]["Subject"].iloc[0]
    )
    y_pipeline = "Pipeline: " + y
    y_result = (
        "Result: N/A"
        if clickData["points"][0]["y"] == -1
        else "Result: " + str(clickData["points"][0]["y"])
    )
    info += [
        html.Br(),
        y_subject,
        html.Br(),
        y_pipeline,
        html.Br(),
        y_result,
        html.Br(),
    ]
    y_info = df[
        (df["Dataset-Pipeline"] == y) & (df["Result"] == clickData["points"][0]["y"])
    ]["Info"].iloc[0]
    for k, v in list(y_info.items())[:-1]:
        status = "Incomplete" if v["status"] is None else v["status"]
        inp = (
            "N/A"
            if v["inputID"] is None
            else html.A(
                str(v["inputID"]),
                href="https://portal.cbrain.mcgill.ca/userfiles/" + str(v["inputID"]),
                style={"color": "#4673a3"},
            )
        )
        out = (
            "N/A"
            if v["outputID"] is None
            else html.A(
                str(v["outputID"]),
                href="https://portal.cbrain.mcgill.ca/userfiles/" + str(v["outputID"]),
                style={"color": "#4673a3"},
            )
        )
        task = (
            "N/A"
            if v["taskID"] is None
            else html.A(
                str(v["taskID"]),
                href="https://portal.cbrain.mcgill.ca/tasks/inser_ID_here"
                + str(v["taskID"]),
                style={"color": "#4673a3"},
            )
        )
        config = "N/A" if v["toolConfigID"] is None else str(v["toolConfigID"])
        step = html.Details(
            [
                html.Summary(k),
                "Status: " + status,
                html.Br(),
                "Input ID: ",
                inp,
                html.Br(),
                "Output ID: ",
                out,
                html.Br(),
                "Task ID: ",
                task,
                html.Br(),
                "Tool Configuration ID: " + config,
            ]
        )
        info.append(step)

    return html.Div(
        html.P(info, style={"margin-left": "10px", "word-wrap": "break-word"}),
        style={
            "width": "90%",
            "box-shadow": "rgba(0, 0, 0, 0.25) 0px 14px 28px, rgba(0, 0, 0, 0.22) 0px 10px 10px",
            "border-radius": "7px",
            "border": "0.25px solid",
        },
    )
