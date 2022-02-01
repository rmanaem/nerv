from turtle import color
import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__)
port = 8881

colors = {
    'text': 'black',
    'plot': '#778899',
    'paper': 'white'
}

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


    dcc.Graph(
        id='SampleChart',
        figure={
            'data': [
                {'x': [4, 6, 8], 'y':[12, 16, 18],
                    'type':'bar', 'name':'First Chart'},
                {'x': [4, 6, 8], 'y':[10, 24, 26],
                    'type':'bar', 'name':'First Chart'}
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
    )
])


if __name__ == '__main__':
    app.run_server(port=port)
