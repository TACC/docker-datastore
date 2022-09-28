
import requests
import flask
import traceback

import requests
import json
import pandas as pd

# Dash Framework
import dash_bootstrap_components as dbc
from dash import Dash, callback, clientside_callback, html, dcc, dash_table as dt, Input, Output, State, MATCH, ALL
from dash.exceptions import PreventUpdate


server = flask.Flask('app')


# ---------------------------------
#   Page components
# ---------------------------------
def serve_layout():

    layout = html.Div([
        dcc.Store(id='store_data'),
        html.H1('Build an App Here'),

    ])
    return layout

# ---------------------------------
#   build app
# ---------------------------------
external_stylesheets_list = [dbc.themes.SANDSTONE, 'https://codepen.io/chriddyp/pen/bWLwgP.css'] #  set any external stylesheets

app = Dash('app', server=server,
                external_stylesheets=external_stylesheets_list,
                suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport', 'content': 'width=device-width, initial-scale=1'}])

app.layout = serve_layout

if __name__ == '__main__':
    app.run_server()


# ---------------------------------
#   Callbacks
# ---------------------------------
