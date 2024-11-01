import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import random

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "Multi-Page Graph App with Dynamic Updates"

# Sample Data Generator
def generate_data():
    return pd.DataFrame({
        'x': range(10),
        'y': [random.randint(0, 100) for _ in range(10)],
        'z': [random.randint(0, 100) for _ in range(10)]
    })

# Layout for a page with graphs
def page_layout(page_num, dropdowns=False):
    return html.Div([
        html.H1(f"Page {page_num}"),
        
        # Dropdowns if required (Pages 1 and 4)
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id=f"dropdown-{page_num}-{i}",
                    options=[{'label': f"Option {j}", 'value': j} for j in range(1, 5)],
                    value=1,
                    clearable=False
                ) for i in range(4)
            ], style={'display': 'flex', 'gap': '10px'}) if dropdowns else None
        ], style={'margin-bottom': '20px'}),
        
        # Graphs
        html.Div([
            dcc.Graph(id=f"graph-{page_num}-{i}", config={'displayModeBar': False}) for i in range(3)
        ], style={'display': 'flex', 'gap': '20px'}),
        
        # Interval for automatic updating (Pages 2 and 3)
        dcc.Interval(
            id=f'interval-{page_num}',
            interval=5*1000,  # Update every 5 seconds
            n_intervals=0
        ) if page_num in [2, 3] else None
    ])

# Create the app layout with links to different pages
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link(f'Go to Page {i+1}', href=f'/page-{i+1}', style={'margin-right': '10px'}) for i in range(4)
    ], style={'margin': '20px'}),

    html.Div(id='page-content')
])

# Update the page content based on the URL
@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_layout(1, dropdowns=True)
    elif pathname == '/page-2':
        return page_layout(2)
    elif pathname == '/page-3':
        return page_layout(3)
    elif pathname == '/page-4':
        return page_layout(4, dropdowns=True)
    else:
        return html.H1("Welcome! Please select a page above.")

# Generate data and update graphs for pages with dropdowns (Pages 1 and 4)
@app.callback(
    [Output(f"graph-1-{i}", "figure") for i in range(3)] +
    [Output(f"graph-4-{i}", "figure") for i in range(3)],
    [Input(f"dropdown-1-{i}", "value") for i in range(4)] +
    [Input(f"dropdown-4-{i}", "value") for i in range(4)]
)
def update_graphs_with_dropdowns(*dropdown_values):
    data = generate_data()
    graphs = []
    
    # Example graph updates based on dropdown selections
    for i in range(3):
        fig = px.line(data, x='x', y='y', title=f"Graph {i+1}")
        fig.update_layout(margin=dict(l=20, r=20, t=30, b=20), uirevision='constant')
        graphs.append(fig)
    
    return graphs * 2  # Duplicate for pages 1 and 4

# Update graphs on Pages 2 and 3 using Interval
@app.callback(
    [Output(f"graph-2-{i}", "figure") for i in range(3)] +
    [Output(f"graph-3-{i}", "figure") for i in range(3)],
    [Input('interval-2', 'n_intervals'), Input('interval-3', 'n_intervals')]
)
def update_graphs_with_interval(n_intervals_2, n_intervals_3):
    data = generate_data()
    graphs = []

    # Create new figures with updated data
    for i in range(3):
        fig = px.scatter(data, x='x', y='z', title=f"Live Graph {i+1}")
        fig.update_layout(margin=dict(l=20, r=20, t=30, b=20), uirevision='constant')
        graphs.append(fig)

    return graphs * 2  # Duplicate for pages 2 and 3

if __name__ == '__main__':
    app.run_server(debug=True)
