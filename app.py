import dash
import dash_bootstrap_components as dbc

################
# Authentication
################

#################
# Dashboard Setup
#################

# Set up Dashboard and create layout
external_stylesheets = [dbc.themes.BOOTSTRAP]

dapp = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = dapp.server

dapp.config.suppress_callback_exceptions = True
