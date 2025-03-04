import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
from open_f1_data import OpenF1LiveData  # Import OpenF1 class
import pandas as pd
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
    dcc.Graph(id="replay-speedmap", config={'displayModeBar': False}),

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
    dbc.Row([
    dbc.Col(dcc.Checklist(
        id="driver-checklist",
        options=[],  # This will be populated dynamically based on available drivers
        value=[],    # Initially no drivers selected
        inline=True, 
        style={"color": "#ffffff"},
        labelStyle={'display': 'inline-block', 'margin-right': '10px'}
    ), width=12)
]),

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

# Callback: Populate Driver Checklist based on selected session
@dash.callback(
    Output("driver-checklist", "options"),
    [Input("replay-session-dropdown", "value"),
     Input("replay-event-dropdown", "value"),
     Input("replay-year-dropdown", "value")]
)
def update_driver_checklist(event_name, session_name, selected_year):
    if not session_name:
        return []
    
    session_id = openf1.get_session_id(event_name, selected_year, session_name)

    # Fetch lap data to get all available drivers in the session
    lap_data = openf1.get_lap_data(session_id)

    if lap_data.empty:
        return []

    # Extract unique driver numbers
    driver_numbers = lap_data['driver_number'].unique()

    # Create checklist options for each driver number
    return [{'label': f'Driver {driver}', 'value': driver} for driver in driver_numbers]

# Callback: Update Slider Max, Marks, Value and Handle Play/Pause
@dash.callback(
    [Output("replay-time-slider", "max"),
     Output("replay-time-slider", "marks"),
     Output("replay-time-slider", "value")],
    [Input("replay-event-dropdown", "value"),
     Input("replay-session-dropdown", "value"),
     Input("replay-year-dropdown", "value"),
     Input('replay-interval', 'n_intervals')],
    [State("replay-time-slider", "value"),
     State("replay-play-button", "n_clicks")]
)
def update_slider(event_name, session_name, selected_year, n_intervals, current_value, play_button_clicks):
    # If no session is selected, return default values
    if not session_name:
        return 0, {}, 0

    session_id = openf1.get_session_id(event_name, selected_year, session_name)

    # Fetch lap data: Get lap durations per driver
    lap_data = openf1.get_lap_data(session_id)

    if lap_data.empty:
        return 0, {}, 0

    # Find the driver who took the longest total race time
    driver_total_time = lap_data.groupby("driver_number")["lap_duration"].sum()
    slowest_driver = driver_total_time.idxmax()  # Driver with the highest total time

    # Get only this driver's lap durations
    slowest_driver_laps = lap_data[lap_data["driver_number"] == slowest_driver].sort_values("lap_number")

    # Compute cumulative race time for this driver
    cumulative_time = slowest_driver_laps["lap_duration"].fillna(0).astype(float).cumsum()

    # Max value for the slider is this driver's total race time
    total_time = cumulative_time.iloc[-1]  # Last cumulative time is the total race duration

    # Generate marks at each lap using cumulative race time
    marks = {int(time): f"Lap {lap}" for lap, time in zip(slowest_driver_laps["lap_number"], cumulative_time)}

    # Handle Play/Pause functionality
    if play_button_clicks % 2 == 1:  # Play is active
        # Increment the slider value by 10 every 10 seconds
        if current_value + 5 <= total_time:
            new_value = current_value + 5
        else:
            new_value = total_time  # Stop at max value if reached
    else:
        new_value = current_value  # Keep the current value if paused

    return total_time, marks, new_value
# Callback: Update Track Map, Acceleration Chart, and Positions Table based on time slider
@dash.callback(
    [Output("replay-speedmap", "figure"),
     Output("replay-acceleration-chart", "figure")],
    [Input("replay-event-dropdown", "value"),
     Input("replay-session-dropdown", "value"),
     Input("replay-year-dropdown", "value"),
     Input("replay-time-slider", "value"),
     Input("replay-interval", "n_intervals"),
     Input("driver-checklist", "value")],  # Add the driver checklist input
    [State("replay-play-button", "n_clicks")]
)
def update_replay_page(event_name, session_name, selected_year, slider_value, n_intervals, selected_drivers, n_clicks):
    print(slider_value)
    if not session_name:
        #print("No session selected")
        return px.scatter(title="No Session Selected", template="plotly_dark"), \
               px.line(title="No Data Available", template="plotly_dark"), \
               dbc.Table([])

    session_id = openf1.get_session_id(event_name, selected_year, session_name)

    # Fetch lap data: Get lap start time and lap durations
    lap_data = openf1.get_lap_data(session_id)
    car_data=openf1.get_data_in_time_range(slider_value)
    # Sort data by trip and time

    car_data['date'] = pd.to_datetime(car_data['date'])
    car_data = car_data.sort_values(by=[ 'driver_number','date'])

    # Compute acceleration separately for each trip
    car_data['time_diff'] = car_data.groupby("driver_number")['date'].diff().dt.total_seconds()
    car_data['speed_diff'] = car_data.groupby("driver_number")['speed'].diff()
    car_data['acceleration'] = car_data['speed_diff'] / car_data['time_diff']
    span = 20  # Number of periods over which to apply the smoothing
    car_data['ema_acceleration'] = car_data['acceleration'].ewm(span=span, adjust=False).mean()
    
    if selected_drivers:
        car_data = car_data[car_data['driver_number'].isin(selected_drivers)]
    # Select relevant columns
    speed_df = car_data[["driver_number", 'date', 'speed', 'acceleration','ema_acceleration']]
    print(speed_df['ema_acceleration'])
    # Create Track Map
    track_fig = px.line(
        speed_df, x="date", y="speed", color="driver_number",
        hover_data=["driver_number"], title="Car Positions & Speed at Time",
        template="plotly_dark"
    ) if not speed_df.empty else px.scatter(title="No Data Available", template="plotly_dark")
    
    # Create Acceleration Chart
    accel_fig = px.line(
        speed_df, x="date", y="ema_acceleration", color="driver_number",
        title="Acceleration at Time", template="plotly_dark"
    ) if not speed_df.empty else px.line(title="No Data Available", template="plotly_dark")


    
    return track_fig, accel_fig


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
