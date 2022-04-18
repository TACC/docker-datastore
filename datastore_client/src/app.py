
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

def get_api_data(api_address):
    api_json = {}
    try:
        try:
            response = requests.get(api_address)
        except:
            return('error: {}'.format(e))
        request_status = response.status_code
        if request_status == 200:
            api_json = response.json()
            return api_json
        else:
            return request_status
    except Exception as e:
        traceback.print_exc()
        api_json['json'] = 'error: {}'.format(e)
        return api_json

#
# print("data from datastore:", datafeed)

# ---------------------------------
#   Page components
# ---------------------------------
def serve_layout():

    layout = html.Div([
        html.H1('A2CPS Data from API'),
        dcc.Dropdown(
            id='dropdown-api',
           options=[
               {'label': 'Subjects', 'value': 'subjects'},
               {'label': 'Imaging', 'value': 'imaging'},
               {'label': 'Blood Draws', 'value': 'blood'},
           ],
           # value='imaging'
        ),
        dcc.Loading(
            id="loading-content",
            type="default",
            children=html.Div(id='div_content')
        ),

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
@app.callback(
    Output('div_content', 'children'),
    Input('dropdown-api', 'value')
)
def update_content(api):
    api_address = "http://datastore:8050/api/" + api
    div_json = get_api_data(api_address)

    return json.dumps(div_json)
