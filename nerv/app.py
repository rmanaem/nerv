import dash
import pandas as pd
import dash_bootstrap_components as dbc
from nerv import utility as util
from nerv import callbacks
from nerv import layouts


def start(path, local=True):
    files = util.pull_files(path)
    dfs = []
    for i, j in enumerate(files):
        dfs.append(util.process_file(j, i))
    df = pd.concat(dfs)

    dbc_css = (
        "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"
    )
    template1 = "plotly_dark"
    template2 = "simple_white"
    theme1 = dbc.themes.DARKLY
    theme2 = dbc.themes.FLATLY
    app = dash.Dash(__name__, external_stylesheets=[theme1, dbc_css])
    app.title = 'NeRV'

    app.layout = layouts.single(df, theme1, theme2, template1)

    callbacks.single(df, template1, template2)

    if local:
        app.run_server()
    else:
        return app.server
