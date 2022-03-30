
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
# try:
#     response = requests.get("http://datastore:8050/subjects")
#     subjects = response.json()
#     print(subjects.keys())
# except Exception as e:
#     subjects = {'status': 'no response'}
#     traceback.print_exc()
def get_api(api):
    try:
        api_address = "http://datastore:8050/" + api
        response = requests.get(api_address)
        request_status = response.status_code
        api_json = response.json()
        return api_json, request_status
    except Exception as e:
        api_json = {'status': 'no response'}
        # traceback.print_exc()

#
# print("data from datastore:", datafeed)

# ---------------------------------
#   Page components
# ---------------------------------


# ---------------------------------
#   build app
# ---------------------------------

app = Dash('app', server=server)


app.layout = html.Div([
    html.H1('A2CPS Data Tables'),
    dcc.Dropdown(
        id='dropdown-datafeeds',
           options=[
               # {'label': 'API', 'value': 'api'},
               # {'label': 'Subjects', 'value': 'subjects'},
               {'label': 'Imaging: overall', 'value': 'imaging'},
               {'label': 'Imaging: scan quality', 'value': 'qc'},

               # {'label': 'Adverse Effects', 'value': 'adverse_effects'}
           ],
       value='imaging'
    ),
    html.Div(id='div_content'),

])

if __name__ == '__main__':
    app.run_server()


# ---------------------------------
#   Callbacks
# ---------------------------------

@app.callback(
    Output('div_content', 'children'),
    Input('dropdown-datafeeds', 'value')
)
def update_dic_content(api):
    api_dict, request_status = get_api(api)
    api_df = pd.DataFrame(api_dict)
    cols_list = list(api_df.columns)
    # api_df = pd.DataFrame(api_dict)
    div_content = html.Div([
        html.P(api),
        html.P(['Request Status: ', request_status]),
        # html.Div([
        #     html.P(json.dumps(c)) for c in api_dict
        #     ])
        # html.Div(type(api_dict))
        # html.P(str(len(api_dict['data']))),
        # html.Div(json.dumps(api_dict['data'][0])),
        #
        dt.DataTable(
            id='tbl', data=api_dict,
            columns=[{"name": i, "id": i} for i in cols_list],
        ),
        # html.Div([
        #     json.dumps(get_api(api))
        # ])
    ])
    return div_content
