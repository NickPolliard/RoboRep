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


pandas.options.display.float_format = '{:,.10f}'.format
pandas.set_option("display.max_columns", 20)
pandas.set_option('expand_frame_repr', False)



##################
# Dashboard Layout
##################


# Page Grid object generation
page_grid = Grid(rows=2,cols=4, specs=[[{'width': 3}, {'width': 3}, {'width': 3}, {'width': 3}], [{'width': 3}, {'width': 3}, {'width': 3}, {'width': 3}]],
                 row_kwargs=[{'className': 'p-2'}, {'className': 'p-2'}],
                 div_class_name='page-grid')

# region Row for nav and continue button
nav_row = html.Div([
    navbar()
], className='d-flex flex-row justify-content-between align-items-center')
# endregion

page_grid.add_element(nav_row, 1, 1)


zip_input = html.Div(
    [
        html.P('Enter Your Zip Code'),
        dbc.Input(id="input", placeholder="12345", type="text"),
        html.Br(),
        html.P(id="output"),
    ]
)

@dapp.callback(Output("output", "children"), [Input("input", "value")])
def output_text(value):
    url = f'https://ziplook.house.gov/htbin/findrep_house?ZIP={value}'
    return url

page_grid.add_element(zip_input, 2, 1)

# We generate the layout with the grid
layout = html.Div([
    banner(),
    page_grid.generated_grid,
    dcc.Interval(
        id='interval-component',
        interval=600*1000, # in milliseconds
        n_intervals=0
    )
], id='main-layout')


#@dapp.callback(Output("main-layout", "children"), [Input("interval-component", "n_intervals")])
#def update(n_intervals):
#    print('refreshed')
#    status_grid = status.generate_status()
#    page_grid.replace_element(status_grid.generated_grid, 2, 1)
#    etl_check_data = etl_check.etl_tracking()
#    etl_check_data['LastCompletedDate'] = pandas.to_datetime(etl_check_data['LastCompletedDate'], format="%Y-%m-%d %H:%M:%S")
#    etl_track_row = etl_track_div(etl_check_data)
#    page_grid.replace_element(etl_track_row, 3, 2)
#    return [
#        banner(),
#        page_grid.generated_grid,
#        dcc.Interval(
#            id='interval-component',
#            interval=600*1000, # in milliseconds
#            n_intervals=0
#        )
#    ]


################################
# Interaction Between Components
################################
