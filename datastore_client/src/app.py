import dash
from dash import html, dash_table as dt
import requests
import flask
import traceback

import requests
import json
import pandas as pd

server = flask.Flask('app')

# ---------------------------------
#   Get Data From datastore
# ---------------------------------
try:
    response = requests.get("http://datastore:8050/subjects")
    subjects = response.json()
    print(subjects.keys())
except Exception as e:
    subjects = {'status': 'no response'}
    traceback.print_exc()

weekly = pd.DataFrame.from_dict(subjects['weekly'], orient='index').reset_index()
#
# print("data from datastore:", datafeed)

# ---------------------------------
#   Page components
# ---------------------------------

df = pd.read_csv('https://git.io/Juf1t')
datafeeds_div = html.Div([
    html.Div([
        json.dumps(weekly.to_dict('records'))
        ]),
    dt.DataTable(
        id='tbl_weekly', data=weekly.to_dict('records'),
        columns=[{"name": i, "id": i} for i in weekly.columns],
    ),
    dt.DataTable(
        id='tbl', data=df.to_dict('records'),
        columns=[{"name": i, "id": i} for i in df.columns],
    )
])

# ---------------------------------
#   build app
# ---------------------------------

app = dash.Dash('app', server=server)


app.layout = html.Div([
    html.H1('Monday. Blurgh'),
    datafeeds_div
])

if __name__ == '__main__':
    app.run_server()
