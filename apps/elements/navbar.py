import dash_bootstrap_components as dbc
import dash_html_components as html

from app import dapp


def banner():
    banner = dbc.Nav([
        html.Div(html.Img(src=dapp.get_asset_url("beta_logo.png"), style={'height': '1.5rem'}),
                 className='ml-2 mr-4 py-1'),
        html.Div(['Robo Rep - Let Your Reps Know What You Think'], className='p-2'),
    ], className='banner p-2')
    return banner


def navbar():
    navbar = dbc.Nav([
        dbc.NavItem(dbc.NavLink("Find Your Representatives", active=True, href="/Home", className='px-2'))
    ])
    return navbar
