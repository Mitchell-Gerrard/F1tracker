 html.H1("🏎️ Race Replay", style={"textAlign": "center", "color": "#ffffff"}),

        # Navigation Links
        dbc.Row([
            dbc.Col(dcc.Link("🏠 Home", href="/", style={"margin-right": "15px", "color": "white"})),
            dbc.Col(dcc.Link("📊 Historical Data", href="/replay", style={"margin-right": "15px", "color": "white"})),
            dbc.Col(dcc.Link("📡 Live Data", href="/live", style={"color": "white"})),
        ], className="mb-3"),