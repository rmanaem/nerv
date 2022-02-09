import base64
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
    html.H1(children='Dash',
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
    html.Div([
        html.Div(id='plot-div',
                 style={'width': '49%', 'display': 'inline-block'}),
        html.Div(id='info-div',
                 style={'width': '49%', 'display': 'inline-block'})
    ],
        style={
        'display': 'flex'
    })


])


def parse_contents(contents):
    content_type, content_string = contents.split(',')
    return base64.b64decode(content_string)


def process_data(contents):
    # Assuming the data was in json format
    data = str(parse_contents(contents).decode('utf8').replace("\'", '\"'))
    data = json.loads(data)
    fsl = [(k, 'FSL', data[k]['FSL']['Result']['result'], data[k]['FSL'])
           for k in data.keys()]
    fsl = [(i[0], i[1], -1, i[3]) if i[2] ==
           None else (i[0], i[1], float(i[2]), i[3]) for i in fsl]
    freesurfer = [(k, 'FreeSurfer', data[k]['FreeSurfer']['Result']
                   ['result'], data[k]['FreeSurfer']) for k in data.keys()]
    freesurfer = [(i[0], i[1], -1, i[3]) if i[2] ==
                  None else (i[0], i[1], float(i[2]), i[3]) for i in freesurfer]
    x = fsl + freesurfer
    df = pd.DataFrame({'Subject': [i[0] for i in x], 'Pipeline': [
                      i[1] for i in x], 'Result': [i[2] for i in x], 'Info': [i[3] for i in x]})
    return df


@app.callback(
    Output(component_id='plot-div', component_property='children'),
    Input(component_id='upload-data', component_property='contents'))
def plot_data(contents):
    df = process_data(contents)
    fig = px.histogram(df, x='Result', color='Pipeline',
                       barmode='overlay', marginal='rug', hover_data=df.columns)
    return dcc.Graph(id='plot', figure=fig, config={'displaylogo': False})


@app.callback(
    Output('info-div', 'children'),
    Input('plot', 'clickData'))
def process_click(clickData):
    if not clickData:
        return dash.no_update
    subject = "Subject: " + \
        clickData['points'][0]['customdata'][0]
    pipeline = "Pipeline: " + clickData['points'][0]['y']
    result = "Result: N/A" if clickData['points'][0]['x'] == - \
        1 else "Result: " + str(clickData['points'][0]['x'])
    info = [subject, html.Br(), pipeline, html.Br(), result, html.Br()]
    for k, v in list(clickData['points'][0]['customdata'][2].items())[:-1]:
        status = "Incomplete" if v['status'] == None else v['status']
        inp = "N/A" if v['inputID'] == None else str(v['inputID'])
        out = "N/A" if v['outputID'] == None else str(v['outputID'])
        task = "N/A" if v['taskID'] == None else str(v['taskID'])
        config = "N/A" if v['toolConfigID'] == None else str(v['toolConfigID'])
        step = [k + ":", html.Br(), "Status: " + status, html.Br(), "Input ID: " + inp, html.Br(),
                "Output ID: " + out, html.Br(), "Task ID: " + task, html.Br(), "Tool Configuration ID: " + config]
        info += step

    return info


if __name__ == '__main__':
    app.run_server(port=port, debug=True)
