import dash
from dash import html
import requests
import flask
import traceback

server = flask.Flask('app')

try:
    response = requests.get("http://datastore:8050/api")
except Exception as e:
    traceback.print_exc()

print("data from datastore", response.json())

app = dash.Dash('app', server=server)


app.layout = html.Div([
    html.H1('Hello World'),
])

if __name__ == '__main__':
    app.run_server()