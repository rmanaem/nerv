import dash
import dash_core_components as dcc
import plotly.graph_objects as go
import dash_html_components as html
import pandas as pd
import numpy as np

app = dash.Dash(__name__)
port = 7777

app.layout = html.Div([
    html.H1(children='Dashboard',
            style={
                'textAlign': 'center'
            })
])


if __name__ == '__main__':
    app.run_server(port=port)
