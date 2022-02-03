import base64
from tkinter import Y
import dash
import dash_core_components as dcc
import plotly.graph_objects as go
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import json

app = dash.Dash(__name__)
port = 7777

app.layout = html.Div([
    html.H1(children='Dashboard',
            style={
                'textAlign': 'center'
            }),
    html.Br(),
    html.Br(),

    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=True
    ),

])


def parse_contents(contents):
    content_type, content_string = contents.split(',')
    return base64.b64decode(content_string)


@app.callback(
    Output(component_id='Scatter-plot', component_property='figure'),
    Input(component_id='upload-data', component_property='contents'))
def parse_data(data):
    data = parse_contents(data)
    data = json.load(data)
    fsl = [(k, k['FSL']['Result']['result']) for k, v in data.items()]
    freesurfer = [(k, k['FreeSurfer']['Result']['result'])
                  for k, v in data.items()]
    fig = go.Figure(data=[go.Scatter(x=[i[0]
                    for i in fsl], y=[i[1] for i in fsl])])


if __name__ == '__main__':
    app.run_server(port=port)
