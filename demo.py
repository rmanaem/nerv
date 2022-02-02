from pickle import TRUE
from turtle import color
import dash
import dash_core_components as dcc
import plotly.graph_objects as go
import dash_html_components as html
import pandas as pd
import numpy as np

app = dash.Dash(__name__)
port = 8881

colors = {
    'text': 'black',
    'plot': '#778899',
    'paper': 'white'
}

np.random.seed(0)
x = np.random.randint(1, 61, 60)
y = np.random.randint(1, 61, 60)


# Specifying the app layout
app.layout = html.Div([
    html.H1(children="Hello Dash!!!",
            style={
                'textAlign': 'center',
                'color':  colors['text']
            }
            ),
    html.Div(children="Dash - A Data product development framework from plotly",
             style={
                 'textAlign': 'center',
                 'color': colors['text']
             }
             ),

    html.Label("Select a city"),

    dcc.Dropdown(
        id='dropdown',
        options=[
            {'label': 'San Francisco', 'value': 'SF'},
            {'label': 'New York City', 'value': 'NYC'}
        ],
        value='NYC',
        multi=True,
        placeholder='City',
    ),

    html.Label('Slider'),
    dcc.Slider(
        min=1,
        max=10,
        value=7,
        step=0.5,
        marks={i: i for i in range(10)}
    ),

    html.Label('Range slider'),
    dcc.RangeSlider(
        min=1,
        max=10,
        step=0.5,
        value=[3, 7],
        marks={i: i for i in range(10)}
    ),

    html.Br(),
    html.Br(),
    html.Div([
        html.Label('Input box'),
        dcc.Input(
            placeholder='Input name',
            type='text',
            value=''
        ),
    ]),

    dcc.Textarea(
        placeholder='Input feedback',
        value='Placeholder',
        style={'width': '50%'}
    ),

    html.Br(),
    html.Br(),
    dcc.Checklist(
        id='checklist',
        options=[
            {'label': 'San Francisco', 'value': 'SF'},
            {'label': 'New York City', 'value': 'NYC'}
        ],
        value=['NYC']
    ),

    html.Br(),
    html.Br(),
    dcc.RadioItems(
        id='radiobutton',
        options=[
            {'label': 'San Francisco', 'value': 'SF'},
            {'label': 'New York City', 'value': 'NYC'}
        ],
        value=['NYC']
    ),

    dcc.Graph(
        id='bar_plot',
        figure={
            'data': [
                {'x': [4, 6, 8], 'y':[12, 16, 18],
                    'type':'bar', 'name':'First Chart'},
                {'x': [4, 6, 8], 'y':[10, 24, 26],
                    'type':'bar', 'name':'Second Chart'}
            ],
            'layout': {
                'plot_bgcolor': colors['plot'],
                'paper_bgcolor': colors['paper'],  # Plot bg color
                'font': {
                    'color': colors['text']

                },
                'title': 'Simple Bar Chart'
            }
        }
    ),

    dcc.Graph(
        id='scatter_plit',
        figure={
            'data': [
                go.Scatter(
                    x=x,
                    y=y,
                    mode='markers'
                )
            ],
            'layout': go.Layout(
                title='Scatterplot of random values',
                xaxis={'title': 'random x values'},
                yaxis={'title': 'random y values'}
            )

        }
    )
])


if __name__ == '__main__':
    app.run_server(port=port)
