import base64
from re import X
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
            'width': '40%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': 'auto'
        },
    ),
    html.Br(),
    html.Div([
        html.Div(id='plot-div',
                 style={'display': 'inline-block', 'width': '75%'}),
        html.Div(
            [html.Div(id='summary-div'),
             html.Div(id='info-div')],
            style={'width': '25%', 'margin-top': '60px'}
        )
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
    # fsl = [(k, 'FSL', data[k]['FSL']['Result']['result'], data[k]['FSL'])
    #        for k in data.keys()]
    # fsl = [(i[0], i[1], -1, i[3]) if i[2] ==
    #        None else (i[0], i[1], float(i[2]), i[3]) for i in fsl]
    # freesurfer = [(k, 'FreeSurfer', data[k]['FreeSurfer']['Result']
    #                ['result'], data[k]['FreeSurfer']) for k in data.keys()]
    # freesurfer = [(i[0], i[1], -1, i[3]) if i[2] ==
    #               None else (i[0], i[1], float(i[2]), i[3]) for i in freesurfer]
    # x = fsl + freesurfer
    x = []
    for k in data.keys():
        for v in data[k].keys():
            x.append((k, v, data[k][v]['Result']['result'], data[k][v]))
    x = [(i[0], i[1], -1, i[3]) if i[2] ==
         None else (i[0], i[1], float(i[2]), i[3]) for i in x]
    df = pd.DataFrame({'Subject': [i[0] for i in x], 'Pipeline': [
                      i[1] for i in x], 'Result': [i[2] for i in x], 'Info': [i[3] for i in x]})
    return df


@app.callback(
    Output(component_id='plot-div', component_property='children'),
    Input(component_id='upload-data', component_property='contents'))
def plot_data(contents):
    if not contents:
        return dash.no_update
    df = process_data(contents)
    fig = px.histogram(df, x='Result', color='Pipeline',
                       barmode='overlay', marginal='rug', hover_data=df.columns)
    return dcc.Graph(id='plot', figure=fig, config={'displaylogo': False}, style={'height': 700})


@app.callback(Output('summary-div', 'children'),
              Input('upload-data', 'contents'))
def generate_summary(contents):
    if not contents:
        return dash.no_update
    df = process_data(contents)
    total = str(df.shape[0])
    miss = str(df[df['Result'] == -1].shape[0])
    summary = ["Total number of datapoints: " + total, html.Br(), "Total number of missing datapoints: "
               + miss, html.Br()]
    pipelines = df['Pipeline'].unique().tolist()
    for p in pipelines:
        s = p + ': ' + str(df[(df['Pipeline'] == p) &
                              (df['Result'] == -1)].shape[0])
        summary.append(s)
        summary.append(html.Br())
    # fsl = str(df[(df['Pipeline'] == 'FSL') & (df['Result'] == -1)].shape[0])
    # freesurfer = str(df[(df['Pipeline'] == 'FreeSurfer')
    #                  & (df['Result'] == -1)].shape[0])
    return summary


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
        # step = [k + ":", html.Br(), "Status: " + status, html.Br(), "Input ID: " + inp, html.Br(),
        #         "Output ID: " + out, html.Br(), "Task ID: " + task, html.Br(), "Tool Configuration ID: " + config]
        step = html.Details(children=[html.Summary(k), "Status: " + status, html.Br(), "Input ID: " + inp,
                                      html.Br(), "Output ID: " + out, html.Br(), "Task ID: " + task, html.Br(), "Tool Configuration ID: " + config])
        info.append(step)

    return info


if __name__ == '__main__':
    app.run_server(port=port, debug=True)
