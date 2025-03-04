import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
import pandas as pd
# Initialize Dash app with multi-page support
app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.DARKLY])
server = app.server  # Required for deployment

# App Layout with Navigation
app.layout = dbc.Container(
    [
        html.H1("🏎️ F1 Data Viewer", style={"textAlign": "center", "color": "#ffffff"}),

        # Navigation Links

        
        dash.page_container  # Loads the selected page dynamically
    ],
    fluid=True
)

if __name__ == "__main__":
    app.run_server(debug=True)

