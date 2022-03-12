# Implementation of latex for axis label was derived from: https://github.com/yueyericardo/dash_latex
import dash
from dash import dcc
from dash import html
import plotly.express as px
from dash.dependencies import Input, Output
import pandas as pd
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
    dcc.Tabs([
        dcc.Tab(html.Div([
            html.Div(dcc.Graph(id='histogram',
                               figure=px.histogram(df[df['Result'] != -1], x='Result', color='Dataset-Pipeline',
                                                   barmode='overlay', marginal='rug', hover_data=df.columns).update_layout(
                                   xaxis_title=r'$\text {Hippocampus Volume } (mm^3)$', yaxis_title='Count',
                                   template='plotly_dark', xaxis={'rangeslider': {'visible': True}}),
                               config={'displaylogo': False}, style={'height': 760}), id='histogram-div',
                     style={'display': 'inline-block', 'width': '75%'}),
            html.Div(
                [
                    html.Div(util.generate_summary(df), id='summary-div'),
                    html.Br(),
                    html.Div(id='info-div')
                ],
                style={'width': '25%', 'margin-left': '30px'}
            )
        ],
            style={
            'display': 'flex'
        })),
        dcc.Tab(
            [
                html.Br(),
                html.Div
                (
                    [
                        html.Div(
                            [
                                html.Label('X: '),
                                dcc.Dropdown(
                                    id='x-dropdown',
                                    options=[{'label': k, 'value': v} for k, v in zip(
                                        df['Dataset-Pipeline'].unique().tolist(), df['Dataset-Pipeline'].unique().tolist())],
                                    style={'width': '300px'}
                                )
                            ],
                            style={'display': 'flex', 'width': '50%'})
                    ],
                    style={'text-align': 'center'}
                )
            ])])
])


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


if __name__ == '__main__':
    app.run_server(port=port, debug=True)
