import dash
from dash import html, dcc
import pandas as pd
import dash_bootstrap_components as dbc
from nerv import utility as util
from nerv import layouts
from nerv import callbacks


def start(path, local=True, single=True):

    dbc_css = (
        "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
    )
    template1 = "plotly_dark"
    template2 = "simple_white"
    theme1 = dbc.themes.DARKLY
    theme2 = dbc.themes.FLATLY
    app = dash.Dash(__name__, routes_pathname_prefix='/',
                    external_stylesheets=[theme1, dbc_css])
    app.title = 'NeRV'
    if single:
        files = util.pull_files(path)
        dfs = []
        for i, j in enumerate(files):
            dfs.append(util.process_file(j, i))
        df = pd.concat(dfs)

        app.layout = layouts.single(df, theme1, theme2, template1)

        callbacks.single(df, template1, template2)
    else:
        app.layout = html.Div(layouts.multiple(path, theme1, theme2, template1)[0])
        app.validation_layout = html.Div(layouts.multiple(path, theme1, theme2, template1))
        callbacks.multiple(path, theme1, theme2, template1, template2)

    if local:
        app.run_server(debug=True)
    else:
        return app.server
