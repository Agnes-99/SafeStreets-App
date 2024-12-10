import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd

def create_dashboard(server):
    dash_app = dash.Dash(__name__, 
        server=server, 
        url_base_pathname='/dashboard/', 
        external_stylesheets=[dbc.themes.BOOTSTRAP])

   **⚠️ This dashboard is currently under development. Updates are coming soon!**

    return dash_app
