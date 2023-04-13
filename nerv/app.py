import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, callback
from dash_bootstrap_templates import ThemeSwitchAIO

from nerv.callbacks import (
    histogram_click_func,
    scatter_click_func,
    switch_template_func,
)
from nerv.layouts import layout
from nerv.utility import process_files


def start(path, local=True):
    dbc_css = (
        "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
    )
    template1 = "plotly_dark"
    template2 = "simple_white"
    theme1 = dbc.themes.DARKLY
    theme2 = dbc.themes.FLATLY
    app = dash.Dash(
        __name__, routes_pathname_prefix="/", external_stylesheets=[theme1, dbc_css]
    )
    app.title = "NeRV"

    def serve_layout():
        global df
        df = process_files(path)

        return layout(df, theme1, theme2, template1)

    app.layout = serve_layout

    @callback(
        Output("histogram", "figure"),
        Output("scatter", "figure"),
        Input(ThemeSwitchAIO.ids.switch("theme"), "value"),
        Input("histogram", "figure"),
        Input("scatter", "figure"),
    )
    def switch_template(value, histogram_fig, scatter_fig):
        return switch_template_func(
            value, histogram_fig, scatter_fig, template1, template2
        )

    @callback(Output("info-div", "children"), Input("histogram", "clickData"))
    def process_click(clickData):
        return histogram_click_func(clickData)

    @callback(
        Output("info-div-scatter", "children"),
        Input("scatter", "clickData"),
        Input("x", "value"),
        Input("y", "value"),
    )
    def process_click_scatter(clickData, x, y):
        return scatter_click_func(clickData, x, y, df)

    if local:
        app.run_server(debug=True)
    else:
        return app.server
