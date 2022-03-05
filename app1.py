# Implementation of latex for axis label was derived from: https://github.com/yueyericardo/dash_latex
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
import utility
# For latex
import dash_defer_js_import as dji

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])
port = 7777

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
                utility.scapes: true
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
        dcc.Tab(
            html.Div([
                html.Div([dcc.Graph('histogram', figure=utility.plot_histogram(utility.all_data), config={'displaylogo': False}, style={'height': 760})], 'histogram-div',
                         style={'display': 'inline-block', 'width': '75%'}),
                html.Div(
                    [html.Div([utility.generate_summary(utility.all_data)], 'summary-div'),
                     html.Br(), html.Div(id='info-div')],
                    style={'width': '25%', 'margin-left': '30px'}
                )
            ],
                style={
                'display': 'flex'
            }),


        ),
        dcc.Tab(
            html.Div(utility.plot_scatters(utility.all_data), "scatters-div")
        )
    ]

    )
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
