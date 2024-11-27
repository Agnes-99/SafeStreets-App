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

    # Example data for the dashboard
    data = {
        'Crime Type': ['Burglary', 'Assault', 'Theft', 'Vandalism', 'Robbery'],
        'Date': ['2024-01-01', '2024-01-02', '2024-01-03', '2024-01-04', '2024-01-05'],
        'Latitude': [40.7128, 34.0522, 51.5074, 48.8566, 41.8781],
        'Longitude': [-74.0060, -118.2437, -0.1278, 2.3522, -87.6298],
        'Description': [
            'Breaking and entering',
            'Physical assault',
            'Shoplifting',
            'Graffiti on wall',
            'Armed robbery'
        ]
    }

    df = pd.DataFrame(data)
    df['Date'] = pd.to_datetime(df['Date'])

    # Create a simple map
    map_fig = go.Figure(go.Scattermapbox(
        lat=df['Latitude'],
        lon=df['Longitude'],
        mode='markers',
        marker=dict(size=14, color='red'),
    ))

    map_fig.update_layout(
        mapbox_style="carto-positron",
        mapbox_zoom=4,
        mapbox_center={"lat": 39.8283, "lon": -98.5795},
        title="Crime Locations"
    )

    dash_app.layout = html.Div([
        dbc.Row([dbc.Col(html.H1("Crime Reporting Dashboard", className="text-center"), width=12)]),
        dbc.Row([
            dbc.Col([dcc.Graph(id="crime-map", figure=map_fig)], width=12),
        ])
    ])
    
    return dash_app
