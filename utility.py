import os
import json
import pandas as pd
from dash import dcc
from dash import html
import plotly.express as px


def pull_files(path):
    files = []
    for i in os.listdir(path):
        files.append(path + '/' + i)
    return files


def process_file(file):
    data = None
    with open(file, 'r') as file:
        data = json.load(file)
    x = []
    for k in data.keys():
        for v in data[k].keys():
            x.append((k, v, data[k][v]['Result']['result'], data[k][v]))
    x = [(i[0], i[1], -1, i[3]) if i[2] ==
         None else (i[0], i[1], float(i[2]), i[3]) for i in x]
    df = pd.DataFrame({'Subject': [i[0] for i in x], 'Pipeline': [
                      i[1] for i in x], 'Result': [i[2] for i in x], 'Info': [i[3] for i in x]})
    return df


def generate_summary(df):
    total = str(df.shape[0])
    miss = str(df[df['Result'] == -1].shape[0])
    header = html.H4('Summary', style={'textAlign': 'center'})
    summary = [header, "Total number of datapoints: " + total, html.Br(), "Total number of missing datapoints: "
               + miss, html.Br()]
    pipelines = df['Pipeline'].unique().tolist()
    for p in pipelines:
        s = p + ': ' + str(df[(df['Pipeline'] == p) &
                              (df['Result'] == -1)].shape[0])
        summary.append(s)
        summary.append(html.Br())
    return html.Div(html.P(summary, style={'margin-left': '10px'}),
                    style={
        'width': '90%',
        'box-shadow': 'rgba(0, 0, 0, 0.25) 0px 14px 28px, rgba(0, 0, 0, 0.22) 0px 10px 10px',
        'border-radius': '7px',
        'border': '0.25px solid'})


def plot_histogram(df):
    fig = px.histogram(df[df['Result'] != -1], x='Result', color='Pipeline',
                       barmode='overlay', marginal='rug', hover_data=df.columns).update_layout(
                           xaxis_title=r'$\text {Hippocampus Volume } (mm^3)$', yaxis_title='Count', template='plotly_dark')
    return fig


def plot_scatters(df1):
    df = pd.DataFrame()
    pipelines = df1['Pipeline'].unique().tolist()
    df['Subject'] = df1['Subject'].unique()
    for i in pipelines:
        df[i] = df1[df1['Pipeline'] == i]['Result'].reset_index(drop=True)
    plots = []
    for i in pipelines:
        for j in pipelines:
            if i != j:
                scatter = px.scatter(
                    df, x=i, y=j, marginal_x='histogram', marginal_y='histogram', template='plotly_dark').update_layout(xaxis={'rangeslider': {'visible': True}})
                plots.append(dcc.Tab(dcc.Graph(figure=scatter, config={
                             'displaylogo': False}, style={'height': 760, 'width': '100%'})))
    return dcc.Tabs(plots)


files = pull_files('./data')
dataframes = []
for i in files:
    dataframes.append(process_file(i))

all_data = pd.concat(dataframes)
