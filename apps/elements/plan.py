import dash_bootstrap_components as dbc
from dash import dcc
import dash_html_components as html

from app import dapp


class Grid:
    def __init__(self, rows=1, cols=1, specs=None, row_kwargs=None, div_class_name=None):
        self.rows = rows
        self.cols = cols
        self.div_class_name = div_class_name
        self.specs = specs
        self.row_kwargs = row_kwargs
        self.generated_grid = None

    @property
    def specs(self):
        return self.__specs

    @specs.setter
    def specs(self, specs):
        if specs is None:
            self.__specs = [[{} for c in range(self.cols)] for r in range(self.rows)]
        elif not (
                isinstance(specs, (list, tuple))
                and specs
                and all(isinstance(row, (list, tuple)) for row in specs)
                and len(specs) == self.rows
                and all(len(row) == self.cols for row in specs)
                and all(all(v is None or isinstance(v, dict) for v in row) for row in specs)
        ):
            raise ValueError(
                """
                The 'specs' argument to generate a grid must be a 2D list of dictionaries with
                dimensions ({rows} x {cols}).
                Received value of type {typ}: {val}
                """.format(rows=self.rows, cols=self.cols, typ=type(specs), val=repr(specs))
            )
        else:
            self.__specs = specs

    @property
    def row_kwargs(self):
        return self.__row_kwargs

    @row_kwargs.setter
    def row_kwargs(self, row_kwargs):
        if not isinstance(row_kwargs, (type(None), list, tuple)):
            raise ValueError(
                """
                The 'row_kwargs' argument must be of type list or tuple. Received: {typ}
                """.format(typ=type(row_kwargs))
            )

        if row_kwargs is None:
            self.__row_kwargs = [{} for r in range(self.rows)]
        elif len(row_kwargs) == self.rows and all(isinstance(row, dict) for row in row_kwargs):
            self.__row_kwargs = row_kwargs
        else:
            raise ValueError(
                """
                The 'row_kwargs' argument must be a list or tuple of dictionaries of length {rows}.
                """.format(rows=self.rows)
            )

    @property
    def generated_grid(self):
        return self.__generated_grid

    @generated_grid.setter
    def generated_grid(self, generated_grid):
        grid_list = []
        for r in range(self.rows):
            rkwargs = self.row_kwargs[r]
            row_children = []
            for c in range(self.cols):
                kwargs = self.specs[r][c]
                if kwargs is not None:
                    row_children.append(dbc.Col([], **kwargs))
            grid_list.append(dbc.Row(row_children, **rkwargs))
        if self.div_class_name:
            self.__generated_grid = html.Div(grid_list, className=self.div_class_name)
        else:
            self.__generated_grid = html.Div(grid_list)

    def add_element(self, element, row, col):
        try:
            self.__generated_grid.children[row-1].children[col-1].children.append(element)
        except IndexError:
            raise ValueError(
                'Cannot add element. The index ({row}, {col}) does not exist in the grid'.format(row=row, col=col)
            )
        return

    def replace_element(self, element, row, col):
        try:
            self.__generated_grid.children[row-1].children[col-1].children[0] = element
        except IndexError:
            raise ValueError(
                'Cannot add element. The index ({row}, {col}) does not exist in the grid'.format(row=row, col=col)
            )
        return


def generate_dropdown_form(label_kwargs=None, dropdown_kwargs=None, is_row=False, widths=(None, None)):
    form_group = dbc.FormGroup([
        dbc.Col(dbc.Label(**label_kwargs), width=widths[0]),
        dbc.Col(dcc.Dropdown(**dropdown_kwargs), width=widths[1])
    ], row=is_row)
    return form_group


def generate_input_form(label_kwargs=None, input_kwargs=None, is_row=False, widths=(None, None), result_message_id=None):

    if result_message_id:
        success_info = html.Div([
            html.Div(html.Img(src=dapp.get_asset_url("check.svg"), style={'height': '1.5rem'}), className='align-self-center px-2'),
            html.Div(id=f'{result_message_id}-success-message', className='align-self-center px-2')
        ], id=f'{result_message_id}-success-container', className='d-none', style={'height': '3rem'})

        failure_info = html.Div([
            html.Div(id=f'{result_message_id}-error-message', className='align-self-center px-2')
        ], id=f'{result_message_id}-error-container', className='d-none', style={'color': '#F41E60', 'height': '3rem'})

        input_list = [
            dbc.Input(**input_kwargs),
            success_info,
            failure_info
        ]
    else:
        input_list = [dbc.Input(**input_kwargs)]

    if is_row:
        label_margin = '0rem'
    else:
        label_margin = None

    form_group = dbc.FormGroup([
        dbc.Col(dbc.Label(style={'margin-bottom': label_margin}, **label_kwargs), width=widths[0]),
        dbc.Col(dcc.Loading(input_list, type='circle'), width=widths[1])
    ], row=is_row, className='align-items-center')
    return form_group