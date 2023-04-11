import dash
import dash_bootstrap_components as dbc
import pandas as pd

from nerv import callbacks
from nerv.layouts import layout
from nerv.utility import process_file, pull_files


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
        files = pull_files(path)
        dfs = []
        for i, j in enumerate(files):
            dfs.append(process_file(j, i))
        global df
        df = pd.concat(dfs)

        return layout(df, theme1, theme2, template1)

    app.layout = serve_layout

    if local:
        app.run_server()
    else:
        return app.server
