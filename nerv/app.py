import dash
from dash import dcc
from dash import html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import ThemeSwitchAIO
from nerv import utility as util
from nerv import callbacks


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
    app.layout = html.Div(
        [
            ThemeSwitchAIO
            (
                aio_id="theme",
                themes=[theme1, theme2],
                icons={"left": "fa fa-sun", "right": "fa fa-moon"},
            ),
            dcc.Tabs
            (
                [
                    dcc.Tab
                    (
                        [
                            html.Br(),
                            html.Br(),
                            html.Div
                            (
                                [
                                    html.Div
                                    (
                                        dcc.Graph
                                        (
                                            id='histogram',
                                            figure=px.histogram
                                            (
                                                df[df['Result'] != -1],
                                                x='Result',
                                                color='Dataset-Pipeline',
                                                color_discrete_map={k: v for k, v in zip(
                                                    df['Dataset-Pipeline'].unique().tolist(), df['Color'].unique().tolist())},
                                                barmode='overlay',
                                                marginal='rug',
                                                hover_data=df.columns
                                            ).update_layout
                                            (
                                                xaxis_title=r'$\text {Hippocampus Volume } (mm^3)$',
                                                yaxis_title='Count',
                                                template=template1,
                                                xaxis={
                                                    'rangeslider': {'visible': True},
                                                    'range': [0, df['Result'].max() + 1000]
                                                }
                                            ).update_xaxes
                                            (
                                                ticks='outside',
                                                tickwidth=2,
                                                tickcolor='white',
                                                ticklen=10
                                            ),
                                            config={'displaylogo': False},
                                            style={'height': 820},
                                            mathjax=True
                                        ),
                                        id='histogram-div',
                                        style={
                                            'display': 'inline-block',
                                            'width': '75%'
                                        }
                                    ),
                                    html.Div
                                    (
                                        [
                                            html.Div
                                            (
                                                util.generate_summary(df),
                                                id='summary-div'
                                            ),
                                            html.Br(),
                                            html.Div(id='info-div')
                                        ],
                                        style={
                                            'width': '25%',
                                            'margin-left': '30px'
                                        }
                                    )
                                ],
                                style={
                                    'display': 'flex'
                                }
                            )
                        ],
                        label='Distribution Plot'
                    ),
                    dcc.Tab
                    (
                        [
                            html.Br(),
                            html.Br(),
                            html.Div
                            (
                                [
                                    html.Div
                                    (
                                        [
                                            html.Div
                                            (
                                                [
                                                    dcc.Dropdown
                                                    (
                                                        id='x',
                                                        options=[{'label': k, 'value': v} for k, v in zip(
                                                            df['Dataset-Pipeline'].unique().tolist(), df['Dataset-Pipeline'].unique().tolist())],
                                                        style={
                                                            'width': '250px',
                                                            'color': '#222'
                                                        },
                                                        value=df['Dataset-Pipeline'].unique().tolist()[
                                                            0],
                                                        placeholder='x'
                                                    ),
                                                    dcc.Dropdown
                                                    (
                                                        id='y',
                                                        options=[{'label': k, 'value': v} for k, v in zip(
                                                            df['Dataset-Pipeline'].unique().tolist(), df['Dataset-Pipeline'].unique().tolist())],
                                                        style={
                                                            'width': '250px',
                                                            'color': '#222'
                                                        },
                                                        value=df['Dataset-Pipeline'].unique(
                                                        ).tolist()[-1],
                                                        placeholder='y'
                                                    )
                                                ],
                                                style={
                                                    'display': 'flex',
                                                    'margin-left': 'auto',
                                                    'margin-right': 'auto',
                                                    'width': '50%'
                                                }
                                            ),
                                            html.Div
                                            (
                                                dcc.Graph
                                                (
                                                    id='scatter',
                                                    figure=px.scatter
                                                    (
                                                        df,
                                                        x=df[df['Dataset-Pipeline'] ==
                                                             df['Dataset-Pipeline'].unique().tolist()[0]]['Result'],
                                                        y=df[df['Dataset-Pipeline'] ==
                                                             df['Dataset-Pipeline'].unique().tolist()[-1]]['Result'],
                                                        marginal_x='histogram',
                                                        marginal_y='histogram',
                                                        template=template1,
                                                        color_discrete_sequence=px.colors.qualitative.G10[::-1]
                                                    ).update_layout
                                                    (
                                                        xaxis={
                                                            'rangeslider': {'visible': True}
                                                        },
                                                        xaxis_title=df['Dataset-Pipeline'].unique().tolist()[
                                                            0],
                                                        yaxis_title=df['Dataset-Pipeline'].unique(
                                                        ).tolist()[-1]
                                                    ),
                                                    config={
                                                        'displaylogo': False},
                                                    style={'height': 790}
                                                ),
                                            )
                                        ],
                                        style={
                                            'display': 'inline-block',
                                            'width': '75%'
                                        }
                                    ),
                                    html.Div
                                    (
                                        id='info-div-scatter',
                                        style={
                                            'width': '25%',
                                            'margin-left': '30px'
                                        }
                                    )
                                ],
                                style={'display': 'flex'}
                            )
                        ],
                        label='Joint Plot'
                    )
                ],
                colors={
                    'border': '#222',
                    'primary': '#222',
                    'background': '#f8f9fa'
                },
                style={
                    'color': '#222'
                }
            )
        ]
    )

    callbacks.single(df, template1, template2)
    if local:
        app.run_server()
    else:
        return app.server
