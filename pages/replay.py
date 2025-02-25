import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
from open_f1_data import OpenF1LiveData  # Import OpenF1 class

# Initialize OpenF1 Data
openf1 = OpenF1LiveData()

# Register Replay Page
dash.register_page(__name__, path="/replay", name="Race Replay")

# Dark Mode Styling
DARK_STYLE = {"backgroundColor": "#1e1e1e", "color": "#ffffff"}

# Layout
layout = dbc.Container([
    html.H1("Race Replay", style={"textAlign": "center", "color": "#ffffff"}),

    # Dropdowns (Same structure as home page)
    dbc.Row([
        dbc.Col(dcc.Dropdown(
            id="replay-data-type",
            options=[{'label': 'Historical Data', 'value': 'historical'}],
            value='historical', clearable=False
        ), width=6),

        dbc.Col(dcc.Dropdown(
            id="replay-year-dropdown",
            options=[{'label': str(year), 'value': year} for year in range(2020, 2025)],
            value=2024, clearable=False
        ), width=6),
    ], className="mb-3"),

    dbc.Row([
        dbc.Col(dcc.Dropdown(
            id="replay-event-dropdown",
            placeholder="Select Event",
            clearable=False
        ), width=6),

        dbc.Col(dcc.Dropdown(
            id="replay-session-dropdown",
            placeholder="Select Session",
            clearable=False
        ), width=6),
    ], className="mb-3"),

    # Track Map (Latest Speed & Positions)
    dcc.Graph(id="replay-trackmap", config={'displayModeBar': False}),

    # Acceleration Chart (Last 1 min)
    dcc.Graph(id="replay-acceleration-chart", config={'displayModeBar': False}),

    # Positions Table
    dbc.Table(id="replay-position-table", bordered=True, dark=True, striped=True, hover=True),

    # Slider and Play Button for controlling race time
    dbc.Row([
        dbc.Col(dcc.Slider(
            id="replay-time-slider",
            min=0,
            max=100,  # Default max, will be dynamically updated
            step=1,
            value=0,  # Start value
            marks={i: str(i) for i in range(0, 101, 10)},  # Example marks
            tooltip={"placement": "bottom", "always_visible": True},
        ), width=10),

        dbc.Col(dbc.Button(
            "Play",
            id="replay-play-button",
            color="primary",
            n_clicks=0
        ), width=2),
    ], className="mb-3"),

    # Interval Component for Live Updates
    dcc.Interval(id='replay-interval', interval=5000, n_intervals=0)
], fluid=True, style=DARK_STYLE)


# Callback: Populate Event Dropdown
@dash.callback(
    Output("replay-event-dropdown", "options"),
    [Input("replay-year-dropdown", "value")]
)
def update_event_dropdown(selected_year):
    events = openf1.get_available_events(year=selected_year)
    return [{'label': event, 'value': event} for event in events] if events else []


# Callback: Populate Session Dropdown based on selected Event and Year
@dash.callback(
    Output("replay-session-dropdown", "options"),
    [Input("replay-event-dropdown", "value"),
     Input("replay-year-dropdown", "value")]
)
def update_session_dropdown(event_name, selected_year):
    if not event_name:
        return []
    
    sessions = openf1.get_available_sessions(event_name, selected_year)
    return [{'label': session, 'value': session} for session in sessions] if sessions else []


# Callback: Update Slider based on the selected session and lap data
@dash.callback(
    [Output("replay-time-slider", "max"),
     Output("replay-time-slider", "marks"),
     Output("replay-time-slider", "value")],
    [Input("replay-event-dropdown", "value"),
     Input("replay-session-dropdown", "value"),
     Input("replay-year-dropdown", "value"),
     Input("replay-interval", "n_intervals")]
)
def update_slider(event_name, session_name, selected_year, n_intervals):
    if not session_name:
        return 0, {}, 0

    session_id = openf1.get_session_id(event_name, selected_year, session_name)

    # Fetch lap data: Get lap start time and lap durations
    lap_data = openf1.get_lap_data()
    print(lap_data,'yo')
    
    print('ya')
    # Set the slider max value to the number of laps
    num_laps = lap_data["lap_number"].max()
    print(num_laps)
    # Generate the marks for each lap with the cumulative time
    marks = {
        i: str(round(sum(lap_data["lap_duration"][:i]), 2))  # Cumulative time for each lap
        for i in range(1, num_laps + 1)
    }

    # Set the initial value to the first lap
    initial_value = 1

    return num_laps, marks, initial_value


# Callback: Update Track Map, Acceleration Chart, and Positions Table based on time slider
@dash.callback(
    [Output("replay-trackmap", "figure"),
     Output("replay-acceleration-chart", "figure"),
     Output("replay-position-table", "children")],
    [Input("replay-event-dropdown", "value"),
     Input("replay-session-dropdown", "value"),
     Input("replay-year-dropdown", "value"),
     Input("replay-time-slider", "value"),
     Input("replay-interval", "n_intervals")],
    [State("replay-play-button", "n_clicks")]
)
def update_replay_page(event_name, session_name, selected_year, slider_value, n_intervals, n_clicks):
    if not session_name:
        return px.scatter(title="No Session Selected", template="plotly_dark"), \
               px.line(title="No Data Available", template="plotly_dark"), \
               dbc.Table([])

    session_id = openf1.get_session_id(event_name, selected_year, session_name)

    # Fetch lap data: Get lap start time and lap durations
    lap_data = openf1.get_lap_data(session_id)
    
    if not lap_data:
        return px.scatter(title="No Data Available", template="plotly_dark"), \
               px.line(title="No Data Available", template="plotly_dark"), \
               dbc.Table([])

    # Fetch data based on the total time computed from the slider
    total_time = sum(lap_data["lap_duration"][:slider_value])
    track_df = openf1.get_race_data_at_time(session_id, total_time)
    accel_df = openf1.get_race_data_at_time(session_id, total_time)
    pos_df = openf1.get_positions_at_time(session_id, total_time)

    # Create Track Map
    track_fig = px.scatter(
        track_df, x="x_position", y="y_position", color="speed",
        hover_data=["driver_number"], title="Car Positions & Speed at Time",
        template="plotly_dark", color_continuous_scale="reds"
    ) if not track_df.empty else px.scatter(title="No Data Available", template="plotly_dark")

    # Create Acceleration Chart
    accel_fig = px.line(
        accel_df, x="timestamp", y="acceleration", color="driver_number",
        title="Acceleration at Time", template="plotly_dark"
    ) if not accel_df.empty else px.line(title="No Data Available", template="plotly_dark")

    # Create Positions Table
    table = dbc.Table([
        html.Thead(html.Tr([html.Th("Position"), html.Th("Driver"), html.Th("Interval")])),
        html.Tbody([
            html.Tr([html.Td(row["position"]), html.Td(row["driver_number"]), html.Td(row["interval"])])
            for _, row in pos_df.iterrows()
        ])
    ], bordered=True, dark=True, striped=True, hover=True) if not pos_df.empty else dbc.Table([])

    return track_fig, accel_fig, table


# Callback: Play Button toggle (Play/Pause functionality)
@dash.callback(
    Output('replay-play-button', 'children'),
    [Input('replay-play-button', 'n_clicks')],
    prevent_initial_call=True
)
def toggle_play_button(n_clicks):
    if n_clicks % 2 == 0:
        return "Play"
    else:
        return "Pause"
