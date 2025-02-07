import dash_core_components as dcc
import dash_html_components as html

import pandas

from app import dapp
from apps.elements.admin_navbar import navbar, banner
from apps.elements.plan import Grid


pandas.options.display.float_format = '{:,.10f}'.format
pandas.set_option("display.max_columns", 20)
pandas.set_option('expand_frame_repr', False)


##################
# Dashboard Layout
##################



# Page Grid object generation
page_grid = Grid(rows=4,cols=4, specs=[[{'width': 10}, {'width': 2}, None, None], [{'width': 12}, None, None, None],
                                       [{'width': 0}, {'width': 12}, {'width': 0}, {'width': 0}], [{}, None, None, None]],
                 row_kwargs=[{'className': 'p-2'}, {'className': 'p-2'}, {'className': 'pt-5', 'align': 'center'}, {'className': 'p-2'}],
                 div_class_name='page-grid')

# region Row for nav and continue button
nav_row = html.Div([
    navbar()
], className='d-flex flex-row justify-content-between align-items-center')
# endregion


page_grid.add_element(nav_row, 1, 1)


# We generate the layout with the grid
layout = html.Div([
    banner(),
    page_grid.generated_grid,
    dcc.Interval(
        id='interval-component',
        interval=600*1000, # in milliseconds
        n_intervals=0
    )
])
