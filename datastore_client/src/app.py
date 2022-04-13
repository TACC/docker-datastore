
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
#   Get Data From datastore
# ---------------------------------

def get_api_data():
    try:
        api_address = "http://datastore:8050/api/subjects"
        response = requests.get(api_address)
        api_json = response.json()
        return api_json
    except Exception as e:
        api_json = {'status': 'no response'}
        # traceback.print_exc()

#
# print("data from datastore:", datafeed)

# ---------------------------------
#   Page components
# ---------------------------------
def serve_layout():

    api_data = get_api_data()

    layout = html.Div([
        html.H1('A2CPS Data from API'),
        html.Div(id='div_content', children=json.dumps(api_data))
    ])
    return layout

# ---------------------------------
#   build app
# ---------------------------------

app = Dash('app', server=server)

app.layout = serve_layout

if __name__ == '__main__':
    app.run_server()


# ---------------------------------
#   Callbacks
# ---------------------------------
