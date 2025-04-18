import dash
import dash_daq as daq
import dash_player
from dash import dcc, clientside_callback
import dash_html_components as html
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output, State

import requests
from bs4 import BeautifulSoup

from app import dapp
from apps.elements.navbar import navbar, banner
from apps.elements.plan import Grid

from routines import HTMLDash
from apps.data.state_names import name_to_abbreviation


def strip_html(div):
    html_string = str(div[0])

    html_string = html_string \
        .replace('name', 'id') \
        .replace('border', 'width') \
        .replace('style type', 'style')
    return HTMLDash.html_to_dash(html_string)


def get_house_rep(value):
    url = f'https://ziplook.house.gov/htbin/findrep_house?ZIP={value}'
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    rep_div = soup.find_all("div", {"class": "repdistrict"})

    return strip_html(rep_div)


def get_senate_reps(state):
    state_abbrv = name_to_abbreviation[state]
    url = f'https://www.senate.gov/states/{state_abbrv}/intro.htm'
    response = requests.get(url)
    html_content = response.text
    soup = BeautifulSoup(html_content, "html.parser")
    div_column = soup.find_all('div', {'class': 'state-column'})

    return HTMLDash.html_to_dash(str(div_column[0])), HTMLDash.html_to_dash(str(div_column[1]))


##################
# Dashboard Layout
##################


# Page Grid object generation
page_grid = Grid(rows=3, cols=4, specs=[
    [{'width': 3}, {'width': 3}, {'width': 3}, {'width': 3}],
    [{'width': 5}, {'width': 2}, {'width': 2}, {'width': 3}],
    [{'width': 4}, {'width': 4}, {'width': 4}, None],
], row_kwargs=[{'className': 'p-2'}, {'className': 'p-2'}, {'className': 'p-2'}], div_class_name='page-grid')

# region Row for nav and continue button
nav_row = html.Div([
    navbar()
], className='d-flex flex-row justify-content-between align-items-center')
# endregion

page_grid.add_element(nav_row, 1, 1)
color_mode_switch =  html.Span(
    [
        dbc.Label(className="fa fa-moon", html_for="switch"),
        dbc.Switch( id="switch", value=True, className="d-inline-block ms-1", persistence=True),
        dbc.Label(className="fa fa-sun", html_for="switch"),
    ]
)
page_grid.add_element(color_mode_switch, 1, 4)

# rep_div = html.Div([html.Card([], id='rep-card')], id='rep-div')
# page_grid.add_element(rep_div, 2, 2)

house_div = html.Div([], id='house-div')
page_grid.add_element(house_div, 3, 1)

senate_div_1 = html.Div([], id='senate-div-1')
page_grid.add_element(senate_div_1, 3, 2)

senate_div_2 = html.Div([], id='senate-div-2')
page_grid.add_element(senate_div_2, 3, 3)


form = dbc.Form(
    dbc.Row(
        [
            dbc.Label("", width="auto"),
            dbc.Col(
                dbc.Input(type="search", placeholder="Enter Zip Code", id='zip-input'),
                className="input"
            ),
            dbc.Col(dbc.Button("Submit", color="primary", n_clicks=0, id="submit-button"), width="auto"),
            html.Span(id='out-span'),
        ],
        className="g-2",
    )
)

page_grid.add_element(form, 2, 1)

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



@dapp.callback([Output('house-div', 'children'), Output('senate-div-1', 'children'), Output('senate-div-2', 'children')],
               [Input('submit-button', 'n_clicks'), Input('zip-input', 'value')],

               )
def on_submit_click(n, value):
    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
    if value and 'submit-button' in changed_id:
        if len(value) == 5:
            house_div = get_house_rep(value)
            state = house_div.children[3].children[6].split('of ')[-1].split('.')[0]
            senate_1, senate_2 = get_senate_reps(state)

        return house_div, senate_1, senate_2
    else:
        return [], [], []

clientside_callback(
    """
    (switchOn) => {
       document.documentElement.setAttribute('data-bs-theme', switchOn ? 'light' : 'dark');  
       return window.dash_clientside.no_update
    }
    """,
    Output("color-mode-switch", "id"),
    Input("color-mode-switch", "value"),
)


# @dapp.callback(Output("main-layout", "children"), [Input("submit-button", "n_clicks"), Input('main-layout', 'children')])
# def update(n_clicks, children):
#    # print('refreshed')
#    # page_grid.replace_element(form, 2, 1)
#    print([p['prop_id'] for p in dash.callback_context.triggered])
#    changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]
#    if 'submit-button' in changed_id:
#        return [
#            banner(),
#            page_grid.generated_grid,
#        ]
#    else:
#        return children


################################
# Interaction Between Components
################################
