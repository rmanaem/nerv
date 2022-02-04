import base64
from turtle import bgcolor
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
import numpy as np
import json


app = dash.Dash(__name__)
port = 7777

app.layout = html.Div([
    html.H1(children='Dashboard',
            style={
                'textAlign': 'center',
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
    ),

    html.Div(id='output-div')

])


def parse_contents(contents):
    content_type, content_string = contents.split(',')
    return base64.b64decode(content_string)


@app.callback(
    Output(component_id='output-div', component_property='children'),
    Input(component_id='upload-data', component_property='contents'))
def parse_data(contents):
    data = str(parse_contents(contents).decode('utf8').replace("\'", '\"'))
    data = json.loads(data)
    fsl = [(k, data[k]['FSL']['Result']['result']) for k, v in data.items()]
    freesurfer = [(k, data[k]['FreeSurfer']['Result']['result'])
                  for k, v in data.items()]
    return dcc.Graph(id='line-plot',
                     figure={
                         'data': [
                             {'x': [i[0] for i in fsl], 'y':[i[1] for i in fsl],
                              'name': 'FSL', 'color': '#7FFFD4', 'marker': {'color': '#B82E2E'}},
                             {'x': [i[0] for i in freesurfer], 'y':[i[1] for i in freesurfer],
                              'name':'FreeSurfer', 'marker': {'color': '#54A24B'}},
                         ],
                         'layout': {
                             'height': 500,
                             'xaxis': {'title': 'Subject', 'showgrid': False, 'showticklabels': False},
                             'yaxis': {'title': 'Result'}
                         },
                     },
                     style={
                         'plot-bgcolor': 'rgba(0,0,0,0)',
                         'paper-bgcolor': 'rgba(0,0,0,0)'

                     },
                     config={
                         'displaylogo': False,
                     }
                     )


if __name__ == '__main__':
    app.run_server(port=port)
