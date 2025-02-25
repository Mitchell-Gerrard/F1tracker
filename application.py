import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
from open_f1_data import OpenF1LiveData  # Import the class from the separate file

# Initialize OpenF1 Data Class (No session pre-selected)
openf1 = OpenF1LiveData()

# Initialize Dash app with Bootstrap (Darkly theme)
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# Dark Mode Styling
DARK_STYLE = {
    "backgroundColor": "#1e1e1e",  # Dark background
    "color": "#ffffff"  # White text
}

# Custom Dropdown Styles for Dark Mode
DARK_DROPDOWN_STYLE = {
    "color": "#ffffff",  # White text
    "backgroundColor": "#333333",  # Dark background for the dropdown
    "borderColor": "#444444",  # Dark border for the dropdown
    "boxShadow": "none",  # Remove box shadow
}

# App Layout with Dark Mode
app.layout = dbc.Container(
    [
        html.H1("F1 Data Viewer", style={"textAlign": "center", "color": "#ffffff"}),

        # Year selection dropdown


        # Dropdowns for selecting data type (Live vs Historical)
        dbc.Row([
            dbc.Col(dcc.Dropdown(
                id="data-type",
                options=[
                    {'label': 'Live Data', 'value': 'live'},
                    {'label': 'Historical Data', 'value': 'historical'}
                ],
                value='historical', clearable=False
            ), width=6),
        dbc.Row([
             dbc.Col(dcc.Dropdown(
                id="year-dropdown",
                options=[{'label': str(year), 'value': year} for year in range(2020, 2025)],
                value=2024, clearable=False
            ), width=6),
        ], className="mb-3"),

            dbc.Col(dcc.Dropdown(
                id="event-dropdown",
                placeholder="Select Event",
                clearable=False
            ), width=6),
        ], className="mb-3"),

        # Dropdown for selecting session type
        dbc.Row([
            dbc.Col(dcc.Dropdown(
                id="session-dropdown",
                placeholder="Select Session",
                clearable=False
            ), width=6),

            dbc.Col(dcc.Dropdown(
                id="lap-dropdown",
                placeholder="Select Lap",
                clearable=False
            ), width=6)
        ], className="mb-3"),

        # Dropdown for selecting data category
        dcc.Dropdown(
            id="data-category",
            options=[
                {'label': 'Lap Time', 'value': 'lap_duration'},
                {'label': 'Speed', 'value': 'st_speed'}
            ],
            value='lap_duration', clearable=False
        ),

        # Graph for lap data
        dcc.Graph(id="lap-graph", config={'displayModeBar': False}),

        # Interval Component for Live Updates
        dcc.Interval(id='interval-component', interval=5000, n_intervals=0)
    ],
    fluid=True, style=DARK_STYLE  # Apply Dark Mode Styling
)

# Callback to populate event dropdown
@app.callback(
    Output("event-dropdown", "options"),
    Input("data-type", "value"),
    Input("year-dropdown", "value")
)
def update_event_dropdown(data_type, selected_year):
    print(data_type, selected_year)
    if data_type == "live":
        return [{'label': 'Live Session', 'value': 'live'}]
    
    events = openf1.get_available_events(year=selected_year)
    print(events)
    return [{'label': event, 'value': event} for event in events]

# Callback to populate session dropdown based on selected event and year
@app.callback(
    Output("session-dropdown", "options"),
    [Input("event-dropdown", "value"),
     Input("year-dropdown", "value")]
)
def update_session_dropdown(event_name, selected_year):

    if not event_name:
        return []
    
    sessions = openf1.get_available_sessions(event_name, selected_year)
    
    return [{'label': session, 'value': session} for session in sessions]


# Callback to populate lap dropdown based on selected session
@app.callback(
    Output("lap-dropdown", "options"),
    [Input("event-dropdown", "value"),
     Input("data-category", "value"),
     Input("data-type", "value"),
     Input("session-dropdown", "value"),
     Input("year-dropdown", "value"),
     Input("interval-component", "n_intervals")]
)
def update_lap_dropdown(event_name,data_category, data_type, session_name, selected_year, n_intervals):
   
    if not session_name:
        return []
    else:
         
         session_id = openf1.get_session_id(event_name, selected_year, session_name)
        
    df = openf1.get_lap_data() if data_type == 'historical' else openf1.get_live_lap_data()

    if df is None or df.empty:
        
        return []
    return [{'label': f"Lap {lap}", 'value': lap} for lap in sorted(df['lap_number'].unique())]

# Callback to update the graph
@app.callback(
    Output("lap-graph", "figure"),
    [Input("lap-dropdown", "value"),
     Input("data-category", "value"),
     Input("data-type", "value"),
     Input("session-dropdown", "value"),
     Input("year-dropdown", "value"),
     Input("interval-component", "n_intervals")]
)

def update_lap_graph(selected_lap, data_category, data_type, session_name, selected_year, n_intervals):
    print(selected_lap, data_category, data_type, session_name, selected_year, n_intervals)
    if not session_name:
        return px.line(title="No Session Selected", template="plotly_dark")

    df = openf1.get_lap_data() if data_type == 'historical' else openf1.get_live_lap_data()

    if df is None or df.empty or selected_lap is None:
        return px.line(title="No Data Available", template="plotly_dark")

    df_lap = df[df['lap_number'] == selected_lap]

    if data_category not in df_lap.columns:
        return px.line(title="Data Not Available", template="plotly_dark")

    fig = px.scatter(
        df_lap, x="lap_duration", y=data_category, color="driver_number",
        title=f"{data_category.capitalize()} for Lap {selected_lap}",
        template="plotly_dark"
    )

    fig.update_layout(
        margin=dict(l=20, r=20, t=30, b=20),
        uirevision='constant',
        plot_bgcolor="#1e1e1e",
        paper_bgcolor="#1e1e1e",
        font=dict(color="white")
    )
    return fig

if __name__ == '__main__':

    app.run_server(debug=True)
