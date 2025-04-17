import json
import os

from dash import dcc
import dash_html_components as html
from dash.dependencies import Input, Output

from app import dapp
from apps import RoboRep
from apps import AdminPage

dapp.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


# UI Page content routes
@dapp.callback(Output('page-content', 'children'),
               [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return RoboRep.layout
    elif pathname == '/Home':
        return RoboRep.layout
    elif pathname == '/Admin':
        return AdminPage.layout
    else:
        return '404: Page not found'


# Traditional API routes
@dapp.server.route("/ping")
def ping():
    return "{status: ok}"


@dapp.server.route("/version")
def version():
    with open('version.json') as json_file:
        data = json.load(json_file)
    return data


# start Flask server
if __name__ == '__main__':
    if os.environ.get('ENVIRONMENT') == 'dev':
        debug = True
    else:
        debug = False

    dapp.run(
        debug=True,
        host='0.0.0.0',
        port=8050
    )
