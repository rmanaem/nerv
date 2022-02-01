import dash
import dash_core_components as dcc
import dash_html_components as html

app = dash.Dash(__name__)
port = 8881

app.layout = html.Div([
    html.H1("Hello Dash!!!"),
    html.Div("Dash - GUI")
])

if __name__ == '__main__':
    app.run_server(port=port)
