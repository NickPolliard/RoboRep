import dash
import dash_daq as daq
import dash_player
import dash_core_components as dcc
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
page_grid = Grid(rows=2,cols=4, specs=[[{'width': 10}, {'width': 2}, None, None], [{'width': 12}, None, None, None]],
                 row_kwargs=[{'className': 'p-2'}, {'className': 'p-2'}],
                 div_class_name='page-grid')

# region Row for nav and continue button
nav_row = html.Div([
    navbar()
], className='d-flex flex-row justify-content-between align-items-center')
# endregion



#status_grid = status.generate_status()
#old_etl_status = status.old_etl_status()
page_grid.add_element(nav_row, 1, 1)
#page_grid.add_element(old_etl_status, 1, 2)
#page_grid.add_element(status_grid.generated_grid, 2, 1)

#page_grid.add_element(etl_track_row, 3, 2)



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
