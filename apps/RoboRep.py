import dash
import dash_daq as daq
import dash_player
from dash import dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

import time
import pandas
import requests
from bs4 import BeautifulSoup

from app import dapp
from apps.elements.navbar import navbar, banner
from apps.elements.plan import Grid

from routines import HTMLDash


pandas.options.display.float_format = '{:,.10f}'.format
pandas.set_option("display.max_columns", 20)
pandas.set_option('expand_frame_repr', False)



##################
# Dashboard Layout
##################


# Page Grid object generation
page_grid = Grid(rows=3,
                 cols=4,
                 specs=[
                     [{'width': 3}, {'width': 3}, {'width': 3}, {'width': 3}],
                     [{'width': 3}, {'width': 9}, None, None],
                     [{'width': 3}, {'width': 3}, {'width': 3}, {'width': 3}],
                 ],
                 row_kwargs=[{'className': 'p-2'}, {'className': 'p-2'}, {'className': 'p-2'}],
                 div_class_name='page-grid')

# region Row for nav and continue button
nav_row = html.Div([
    navbar()
], className='d-flex flex-row justify-content-between align-items-center')
# endregion

page_grid.add_element(nav_row, 1, 1)

rep_div = html.Div(id='rep-div')
page_grid.add_element(rep_div, 2, 2)


form = dbc.Form(
    dbc.Row(
        [
            dbc.Label("", width="auto"),
            dbc.Col(
                dbc.Input(type="text", placeholder="Enter Zip Code", id='zip-input'),
                className="input"
            ),
            dbc.Col(dbc.Button("Submit", color="primary", n_clicks=0, id="submit-button"), width="auto"),
            html.Div(id='rep-div'),
        ],
        className="g-2",
    )
)
@dapp.callback(Output('rep-div', 'children'),
               [Input('submit-button', 'n_clicks'), Input('zip-input', 'value')],
               )
def on_button_click(n, value):
    if value is None:
        return
    if len(value) < 5 < len(value):
        return html.P('Invalid Zip')

    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if 'submit-button' in changed_id:
        url = f'https://ziplook.house.gov/htbin/findrep_house?ZIP={value}'
        response = requests.get(url)
        html_content = response.text
        soup = BeautifulSoup(html_content, "html.parser")
        rep_div = soup.find_all("div", {"class": "repdistrict"})
        html_string = str(rep_div[0]) \
            .replace('name', 'id') \
            .replace('border', 'width')
        dash_div = HTMLDash.html_to_dash(html_string)
        return dash_div
    else:
        return html.P('')

page_grid.add_element(form, 2, 1)

# We generate the layout with the grid
layout = html.Div([
    banner(),
    page_grid.generated_grid,
    dcc.Interval(
        id='interval-component',
        # interval=6*1000, # in milliseconds
        n_intervals=0
    )
], id='main-layout')


# @dapp.callback(Output("main-layout", "children"), [Input("interval-component", "n_intervals")])
# def update(n_intervals):
#    print('refreshed')
#    page_grid.replace_element(form, 2, 1)
#    return [
#        banner(),
#        page_grid.generated_grid,
#        dcc.Interval(
#            id='interval-component',
#            interval=6*1000, # in milliseconds
#            n_intervals=0
#        )
#    ]


################################
# Interaction Between Components
################################
