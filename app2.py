# Implementation of latex for axis label was derived from: https://github.com/yueyericardo/dash_latex
import base64
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots
from dash.dependencies import Input, Output
import pandas as pd
import json
import dash_bootstrap_components as dbc
import utility as util
# For latex
import dash_defer_js_import as dji

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
port = 7777

files = util.pull_files('./data')
dfs = []
for i in files:
    dfs.append(util.process_file(i))
df = pd.concat(dfs)


# For latex
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            <script type="text/x-mathjax-config">
            MathJax.Hub.Config({
                tex2jax: {
                inlineMath: [ ['$','$'],],
                processEscapes: true
                }
            });
            </script>
            {%renderer%}
        </footer>
    </body>
</html>
'''

# For latex
axis_latex_script = dji.Import(
    src="https://cdn.jsdelivr.net/gh/yueyericardo/simuc@master/apps/dash/resources/redraw.js")
mathjax_script = dji.Import(
    src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.7/latest.js?config=TeX-AMS-MML_SVG")

app.layout = html.Div([
    # For latex
    axis_latex_script,
    # For latex
    mathjax_script,
    html.H1(children='Dash',
            style={
                'textAlign': 'center',
            }),

    html.Br(),
    html.Br(),
    html.Br(),

    html.Div([
        html.Div(dcc.Graph(id='histogram',
                           figure=px.histogram(df[df['Result'] != -1], x='Result', color='Pipeline',
                                               barmode='overlay', marginal='rug', hover_data=df.columns).update_layout(
                               xaxis_title=r'$\text {Hippocampus Volume } (mm^3)$', yaxis_title='Count',
                               template='plotly_dark', xaxis={'rangeslider': {'visible': True}}),
                           config={'displaylogo': False}, style={'height': 760}), id='histogram-div',
                 style={'display': 'inline-block', 'width': '75%'}),
        html.Div(
            [html.Div(util.generate_summary(df), id='summary-div'),
             html.Br(), html.Div(id='info-div')],
            style={'width': '25%', 'margin-left': '30px'}
        )
    ],
        style={
        'display': 'flex'
    }),

    html.Div(util.plot_scatters(df), id="scatter-matrix-div")

])


def parse_contents(contents):
    content_type, content_string = contents.split(',')
    return str(base64.b64decode(content_string).decode('utf8').replace("\'", '\"'))


def process_data(contents):
    data = json.loads(parse_contents(contents))
    x = []
    for k in data.keys():
        for v in data[k].keys():
            x.append((k, v, data[k][v]['Result']['result'], data[k][v]))
    x = [(i[0], i[1], -1, i[3]) if i[2] ==
         None else (i[0], i[1], float(i[2]), i[3]) for i in x]
    df = pd.DataFrame({'Subject': [i[0] for i in x], 'Pipeline': [
                      i[1] for i in x], 'Result': [i[2] for i in x], 'Info': [i[3] for i in x]})
    return df


# @app.callback(
#     Output(component_id='histogram-div', component_property='children'),
#     Input(component_id='upload-data', component_property='contents'))
# def plot_histogram(contents):
#     if not contents:
#         return dash.no_update
#     df = process_data(contents)
#     fig = px.histogram(df[df['Result'] != -1], x='Result', color='Pipeline',
#                        barmode='overlay', marginal='rug', hover_data=df.columns).update_layout(
#                            xaxis_title=r'$\text {Hippocampus Volume } (mm^3)$', yaxis_title='Count', template='plotly_dark')
#     return dcc.Graph(id='histogram', figure=fig, config={'displaylogo': False}, style={'height': 760})


# @app.callback(Output('summary-div', 'children'))
# def generate_summary(df):
#     if not df:
#         return dash.no_update
#     # df = process_data(contents)
#     total = str(df.shape[0])
#     miss = str(df[df['Result'] == -1].shape[0])
#     header = html.H4('Summary', style={'textAlign': 'center'})
#     summary = [header, "Total number of datapoints: " + total, html.Br(), "Total number of missing datapoints: "
#                + miss, html.Br()]
#     pipelines = df['Pipeline'].unique().tolist()
#     for p in pipelines:
#         s = p + ': ' + str(df[(df['Pipeline'] == p) &
#                               (df['Result'] == -1)].shape[0])
#         summary.append(s)
#         summary.append(html.Br())
#     return html.Div(html.P(summary, style={'margin-left': '10px'}),
#                     style={
#         'width': '90%',
#         'box-shadow': 'rgba(0, 0, 0, 0.25) 0px 14px 28px, rgba(0, 0, 0, 0.22) 0px 10px 10px',
#         'border-radius': '7px',
#         'border': '0.25px solid'})


@app.callback(
    Output('info-div', 'children'),
    Input('histogram', 'clickData'))
def process_click(clickData):
    if not clickData:
        return dash.no_update
    subject = "Subject: " + \
        clickData['points'][0]['customdata'][0]
    pipeline = "Pipeline: " + clickData['points'][0]['y']
    result = "Result: N/A" if clickData['points'][0]['x'] == - \
        1 else "Result: " + str(clickData['points'][0]['x'])
    header = html.H4('Information', style={'textAlign': 'center'})
    info = [header, subject, html.Br(), pipeline, html.Br(), result, html.Br()]

    for k, v in list(clickData['points'][0]['customdata'][2].items())[:-1]:
        status = "Incomplete" if v['status'] == None else v['status']
        inp = "N/A" if v['inputID'] == None else html.A(str(
            v['inputID']), href='https://portal.cbrain.mcgill.ca/userfiles/' + str(v['inputID']))
        out = "N/A" if v['outputID'] == None else html.A(str(
            v['outputID']), href='https://portal.cbrain.mcgill.ca/userfiles/' + str(v['outputID']))
        task = "N/A" if v['taskID'] == None else html.A(str(
            v['taskID']), href='https://portal.cbrain.mcgill.ca/tasks/inser_ID_here' + str(v['taskID']))
        config = "N/A" if v['toolConfigID'] == None else str(v['toolConfigID'])
        step = html.Details(children=[html.Summary(k), "Status: " + status, html.Br(), "Input ID: ", inp,
                                      html.Br(), "Output ID: ", out, html.Br(), "Task ID: ", task, html.Br(), "Tool Configuration ID: " + config])
        info.append(step)

    return html.Div(html.P(info, style={'margin-left': '10px'}),
                    style={
        'width': '90%',
        'box-shadow': 'rgba(0, 0, 0, 0.25) 0px 14px 28px, rgba(0, 0, 0, 0.22) 0px 10px 10px',
        'border-radius': '7px',
        'border': '0.25px solid'})


# @app.callback(Output('scatter-matrix-div', 'children'),
#               Input('upload-data', 'contents'))
# def scatter_matrix(contents):
#     if not contents:
#         return dash.no_update
#     df1 = process_data(contents)
#     df = pd.DataFrame()
#     pipelines = df1['Pipeline'].unique().tolist()
#     df['Subject'] = df1['Subject'].unique()
#     for i in pipelines:
#         df[i] = df1[df1['Pipeline'] == i]['Result'].reset_index(drop=True)
#     plots = []
#     for i, j in enumerate(pipelines):
#         for z, w in enumerate(pipelines):
#             if j != w:
#                 scatter = px.scatter(
#                     df, x=j, y=w, marginal_x='histogram', marginal_y='histogram')
#                 plots.append(dcc.Graph(figure=scatter))
#     return plots


if __name__ == '__main__':
    app.run_server(port=port, debug=True)
