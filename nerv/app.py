"""
The entry point of the app.
"""
import os
import urllib

import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, callback

from nerv.callbacks import hist_click_func, plot_scatter_func, scatter_click_func
from nerv.layouts import index_layout, navbar, vis_layout
from nerv.utility import process_files


def start(path, local=True):
    """
    Creates and configures a Dash app instance that can either be
    run locally or used for deployment.

    Parameters
    ----------
    path : str
        Path of the directory containing files to be visualized.
    local : bool, optional
        Whether or not to start the app locally in the terminal or return
        a Flask app containing the Dash app for deployment, by default True.

    Returns
    -------
    None or flask.app.Flask
        None if local parameter is set to True, otherwise
        returns a flask app instance.
    """
    app = dash.Dash(
        __name__,
        routes_pathname_prefix="/",
        external_stylesheets=[
            dbc.themes.BOOTSTRAP,
            dbc.icons.BOOTSTRAP,
            dbc.themes.BOOTSTRAP,
        ],
    )
    app.title = "NeRV"

    def serve_layout():
        """
        Generates and updates the app layout.
        Used by the app.layout to dynamically generate/update
        app layout on page referesh or whenever change is detected.

        Returns
        -------
        dash_bootstrap_components._components.Container.Container
            The app layout made up of various dash bootstrap components and
            dash core components wrapped with a dash bootstrap componenets
            container component.
        """
        return navbar()

    app.layout = serve_layout

    @callback(Output("store", "data"), Input("url", "pathname"))
    def update_store(pathname):
        """
        Parses and stores the pathname from dcc.Location dash component.
        It utilizes urllib.parse module's unquote_pluse function to
        parse pathname and stores it in local memory.

        Parameters
        ----------
        pathname : str
            pathname in window.location - e.g., "/experiment1".

        Returns
        ----------
        str
            Parsed pathname.
        """
        return urllib.parse.unquote_plus(pathname)

    @callback(Output("content", "children"), Input("store", "data"))
    def display_page(url):
        """
        Displays page based on url stored in the local memory.
        If the input url is `/`, it returns index page layout otherwise it
        returns the visualization layout for a dataframe created using
        the input url and the input path of start function.

        Parameters
        ----------
        url : str
            url of the page to be displayed.

        Returns
        ----------
        dash_bootstrap_components._components.Container.Container or
        dash_bootstrap_components._components.Tabs.Tabs
            Index page layout if the url is `/` otherwise visualization
            layout.
        """
        if url == "/":
            return index_layout(path)
        else:
            global df
            df = process_files(os.path.join(path, url[1:]))
            return vis_layout(df)

    @app.callback(
        Output("offcanvas", "is_open"),
        Input("settings", "n_clicks"),
        [State("offcanvas", "is_open")],
    )
    def toggle_offcanvas(n, is_open):
        if n:
            return not is_open
        return is_open

    app.clientside_callback(
        """
    function(url) {
        var stylesheets = document.querySelectorAll('link[rel=stylesheet][href^="https://cdn.jsdelivr.net"]')

        stylesheets[stylesheets.length - 1].href = url

        setTimeout(function() {stylesheets[0].href = url;}, 100);
    }
    """,
        Output("blank_output", "children"),
        Input("themes", "value"),
    )

    @callback(Output("hist-metadata-div", "children"), Input("histogram", "clickData"))
    def hist_click(clickData):
        """
        Processes data from the histogram graph click event.

        Parameters
        ----------
        clickData : dict
            Data from latest histogram graph click event.

        Returns
        ----------
        dash._callback.Noupdate or dash_bootstrap_components._components.Card.Card
            No dash update if clickData is None otherwise, styled and structured
            metadata to be displayed in hist-metadata-div.
        """
        return hist_click_func(clickData)

    @callback(
        Output("scatter", "figure"),
        Input("x", "value"),
        Input("y", "value"),
    )
    def plot_scatter(x, y):
        """
        Creates a scatter plot figure.

        Parameters
        ----------
            x : str
                Name of the x-axis dataset-pipeline.
            y : str
                Name of the y-axis dataset-pipeline.

        Returns
        ----------
        plotly.graph_objs._figure.Figure
            A plotly graph figure object for the scatter plot
            where x and y inputs are the axes.
        """
        return plot_scatter_func(x, y, df)

    @callback(
        Output("scatter-metadata-div", "children"),
        Input("scatter", "clickData"),
        Input("x", "value"),
        Input("y", "value"),
    )
    def scatter_click(clickData, x, y):
        """
        Processes data from the scatter plot graph click event.

        Parameters
        ----------
        clickData : dict
            Data from latest histogram graph click event.
        x : str
            Name of the x-axis dataset-pipeline.
        y : str
            Name of the y-axis dataset-pipeline.

        Returns
        ----------
        dash._callback.Noupdate or dash_bootstrap_components._components.Card.Card
            No dash update if clickData is None otherwise, styled and structured
            metadata to be displayed in scatter-metadata-div.
        """
        return scatter_click_func(clickData, x, y, df)

    if local:
        app.run_server()
    else:
        return app.server
