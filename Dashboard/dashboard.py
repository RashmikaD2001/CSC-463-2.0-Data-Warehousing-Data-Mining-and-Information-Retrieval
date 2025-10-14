import dash
import dash_bootstrap_components as dbc
from dash import dcc, Input, Output, html
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os

# Loading data
def load_data():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, '../Data/cleaned_data.csv')
    data_path = os.path.normpath(data_path)
    print(f"Looking for file at: {data_path}")
    data = pd.read_csv(data_path)
    return data

data = load_data()

quantitative_columns = ['age', 'departure_delay_minutes', 'arrival_delay_minutes', 'distance']
qualitative_cols = [col for col in data.columns if col not in quantitative_columns]

num_records = len(data)
satisfied_customers = (len(data[data['satisfaction'] == 'satisfied'])/num_records)*100

mode_age_grp = data['age_bin'].mode()[0]
mode_class = data['class'].mode()[0]
mode_travel_type = data['travel_type'].mode()[0]
mode_customers = data['customer_type'].mode()[0]

mode_age_grp_val = len(data[(data['age_bin'] == mode_age_grp)])
mode_class_val = len(data[data['class'] == mode_class])
mode_travel_type_val = len(data[data['travel_type'] == mode_travel_type])
mode_customers_val = len(data[data['customer_type'] == mode_customers])

# Creating web app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Custom CSS styles
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            :root {
                --primary-color: #0066cc;
                --secondary-color: #00a8e8;
                --accent-color: #ff6b6b;
                --dark-bg: #0f1419;
                --card-bg: #1a1f2e;
                --text-light: #e0e0e0;
            }
            
            body {
                background: linear-gradient(135deg, #0f1419 0%, #1a1f2e 100%);
                color: var(--text-light);
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            
            .dashboard-title {
                background: linear-gradient(135deg, #0066cc 0%, #00a8e8 100%);
                color: white;
                padding: 30px;
                border-radius: 15px;
                font-size: 2.5rem;
                font-weight: 700;
                text-shadow: 0 2px 10px rgba(0,0,0,0.3);
                margin-bottom: 30px !important;
                box-shadow: 0 10px 30px rgba(0, 102, 204, 0.3);
                text-align: center;
            }
            
            .stat-card {
                background: linear-gradient(135deg, #1a1f2e 0%, #252d3d 100%);
                border: 1px solid rgba(0, 168, 232, 0.3);
                border-radius: 12px;
                padding: 20px;
                text-align: center;
                margin-bottom: 15px;
                transition: all 0.3s ease;
                box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            }
            
            .stat-card:hover {
                transform: translateY(-5px);
                border-color: #00a8e8;
                box-shadow: 0 15px 30px rgba(0, 168, 232, 0.2);
            }
            
            .stat-value {
                font-size: 1.8rem;
                font-weight: 700;
                color: #00a8e8;
                margin-bottom: 5px;
            }
            
            .stat-label {
                font-size: 0.95rem;
                color: #b0b0b0;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            
            .card {
                background: linear-gradient(135deg, #1a1f2e 0%, #252d3d 100%) !important;
                border: 1px solid rgba(0, 168, 232, 0.2) !important;
                border-radius: 15px !important;
                box-shadow: 0 10px 30px rgba(0,0,0,0.4) !important;
                transition: all 0.3s ease;
                margin-bottom: 25px;
            }
            
            .card:hover {
                transform: translateY(-5px);
                border-color: rgba(0, 168, 232, 0.5) !important;
                box-shadow: 0 15px 40px rgba(0, 168, 232, 0.15) !important;
            }
            
            .card-body {
                padding: 25px !important;
            }
            
            .card-title {
                color: #00a8e8 !important;
                font-weight: 700 !important;
                font-size: 1.3rem !important;
                margin-bottom: 20px !important;
            }
            
            .dropdown-label {
                color: #ffffff;
                font-size: 0.9rem;
                margin-bottom: 8px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            
            .Select-control {
                background-color: #0f1419 !important;
                border: 1px solid rgba(0, 168, 232, 0.3) !important;
                border-radius: 8px !important;
            }
            
            .Select-menu-outer {
                background-color: #1a1f2e !important;
                border: 1px solid rgba(0, 168, 232, 0.3) !important;
            }
            
            .Select-option {
                background-color: #1a1f2e !important;
                color: #e0e0e0 !important;
            }
            
            .Select-option.is-focused {
                background-color: #00a8e8 !important;
                color: white !important;
            }
            
            .Select-placeholder {
                color: #ffffff !important;
            }
            
            .Select-input input::placeholder {
                color: #ffffff !important;
            }
            
            .rc-slider {
                margin: 20px 0 !important;
            }
            
            .rc-slider-track {
                background: linear-gradient(to right, #0066cc, #00a8e8) !important;
            }
            
            .rc-slider-handle {
                background: #00a8e8 !important;
                border: 2px solid #0066cc !important;
            }
            
            footer {
                background: rgba(15, 20, 25, 0.8);
                border-top: 1px solid rgba(0, 168, 232, 0.2);
                margin-top: 50px;
                padding: 30px 0;
            }
            
            footer p {
                color: #808080;
                font-size: 0.9rem;
                margin: 0;
            }
            
            .plotly-graph-div {
                background: transparent !important;
            }
            
            h1, h2, h3, h4 {
                color: var(--text-light);
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# App layout
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.H1("✈️ Airline Passenger Satisfaction Dashboard", 
                   className="dashboard-title"),
            width=12
        )
    ]),

    dbc.Row([
        dbc.Col(
            html.Div([
                html.Div(f"{num_records:,}", className="stat-value"),
                html.Div("Total Customer Records", className="stat-label")
            ], className="stat-card"),
            width=12, md=6, lg=3
        ),
        dbc.Col(
            html.Div([
                html.Div(f"{satisfied_customers:.1f}%", className="stat-value"),
                html.Div("Satisfied Customers", className="stat-label")
            ], className="stat-card"),
            width=12, md=6, lg=3
        ),
        dbc.Col(
            html.Div([
                html.Div(f"{mode_age_grp_val:,}", className="stat-value"),
                html.Div(f"Majority: {mode_age_grp}", className="stat-label")
            ], className="stat-card"),
            width=12, md=6, lg=3
        ),
        dbc.Col(
            html.Div([
                html.Div(f"{mode_class}", className="stat-value"),
                html.Div("Most Popular Class", className="stat-label")
            ], className="stat-card"),
            width=12, md=6, lg=3
        ),
    ], className="mb-4"),

    dbc.Row([
        dbc.Col(
            dbc.Card([
                dbc.CardBody([
                    html.H4("Customer Demographics", className="card-title"),
                    html.Div("Select a demographic feature to explore:", className="dropdown-label"),
                    dcc.Dropdown(
                        id="customer-features",
                        options=[
                            {'label': '😊 Satisfaction', 'value': 'satisfaction'},
                            {'label': '📅 Age Group', 'value': 'age_bin'},
                            {'label': '💼 Class', 'value': 'class'},
                            {'label': '👤 Customer Type', 'value': 'customer_type'},
                            {'label': '👥 Gender', 'value': 'gender'},
                            {'label': '✈️ Travel Type', 'value': 'travel_type'}
                        ],
                        value='satisfaction',
                        placeholder="Select a feature",
                        style={'color': '#ffffff'}
                    ),
                    dcc.Graph(id="customer-dist")
                ])
            ]),
            width=12
        ),
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Quantitative Feature Distribution", className="card-title"),
                    html.Div("Select a metric to analyze:", className="dropdown-label"),
                    dcc.Dropdown(
                        id="quantitative-feature",
                        options=[{'label': col.title().replace("_", " "), 'value': col} for col in quantitative_columns],
                        value='age',
                        placeholder="Select a feature",
                        style={'color': '#ffffff'}
                    ),
                    html.Br(),
                    html.Div("Filter data by selecting a maximum value:", className="dropdown-label"),
                    dcc.Slider(
                        id="quantitative-slider",
                        step=1,
                        tooltip={"placement": "bottom", "always_visible": True}
                    ),
                    html.Br(),
                    dcc.Graph(id="quantitative-distribution")
                ])
            ])
        ], width=12)
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Relationship Between Metrics", className="card-title"),
                    dbc.Row([
                        dbc.Col([
                            html.Div("X-Axis Feature:", className="dropdown-label"),
                            dcc.Dropdown(
                                id="x-feature",
                                options=[{'label': col.title().replace("_", " "), 'value': col} for col in quantitative_columns],
                                value='age',
                                style={'color': '#ffffff'}
                            ),
                        ], md=6),
                        dbc.Col([
                            html.Div("Y-Axis Feature:", className="dropdown-label"),
                            dcc.Dropdown(
                                id="y-feature",
                                options=[{'label': col.title().replace("_", " "), 'value': col} for col in quantitative_columns],
                                value='distance',
                                style={'color': '#ffffff'}
                            ),
                        ], md=6),
                    ]),
                    html.Br(),
                    dcc.Graph(id="scatter-relationship")
                ])
            ])
        ], width=12)
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H4("Feature Comparison", className="card-title"),
                    dbc.Row([
                        dbc.Col([
                            html.Div("First Feature:", className="dropdown-label"),
                            dcc.Dropdown(
                                id="qualitative-x",
                                options=[{'label': col.title().replace("_", " "), 'value': col} for col in qualitative_cols],
                                value='gender',
                                style={'color': '#ffffff'}
                            ),
                        ], md=6),
                        dbc.Col([
                            html.Div("Second Feature:", className="dropdown-label"),
                            dcc.Dropdown(
                                id="qualitative-hue",
                                options=[{'label': col.title().replace("_", " "), 'value': col} for col in qualitative_cols],
                                value='satisfaction',
                                style={'color': '#ffffff'}
                            ),
                        ], md=6),
                    ]),
                    html.Br(),
                    dcc.Graph(id="qualitative-relationship")
                ])
            ])
        ], width=12)
    ]),

    dbc.Row([
        dbc.Col(
            html.Footer(
                html.P(
                    "Airline Dashboard | Built with Dash & Plotly By Rashmika Dushmantha",
                    style={"textAlign": "center", "margin": 0}
                )
            ),
            width=12
        )
    ])

], fluid=True, style={'backgroundColor': '#0f1419', 'paddingTop': '20px', 'paddingBottom': '20px'})


# Callbacks
@app.callback(
    Output('customer-dist', 'figure'),
    Input('customer-features', 'value')
)
def customer_dist_graphs(selected_feature):
    if not selected_feature:
        return px.scatter()
    
    counts = data[selected_feature].value_counts().reset_index()
    counts.columns = [selected_feature, "count"]

    fig = px.pie(
        counts, 
        names=selected_feature, 
        values="count", 
        title=f"Distribution of {selected_feature.title().replace('_', ' ')}"
    )
    
    fig.update_traces(marker=dict(line=dict(color='#0f1419', width=2)))
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e0e0e0', family='Segoe UI'),
        title_font_size=18
    )
    return fig


@app.callback(
    Output('quantitative-slider', 'min'),
    Output('quantitative-slider', 'max'),
    Output('quantitative-slider', 'value'),
    Output('quantitative-slider', 'marks'),
    Input('quantitative-feature', 'value')
)
def update_slider(selected_feature):
    if not selected_feature:
        return 0, 100, 50, {0: "0", 100: "100"}

    col_data = data[selected_feature].dropna()
    min_val = int(col_data.min())
    max_val = int(col_data.max())
    median_val = int(col_data.median())

    marks = {int(v): str(int(v)) for v in col_data.quantile([0, 0.25, 0.5, 0.75, 1]).values}

    return min_val, max_val, median_val, marks


@app.callback(
    Output('quantitative-distribution', 'figure'),
    Input('quantitative-feature', 'value'),
    Input('quantitative-slider', 'value')
)
def update_histogram(selected_feature, slider_value):
    if not selected_feature:
        return px.histogram(title="Select a feature to display")

    filtered_df = data[data[selected_feature] <= slider_value]

    fig = px.histogram(
        filtered_df,
        x=selected_feature,
        nbins=30,
        title=f"{selected_feature.title().replace('_', ' ')} Distribution",
        labels={selected_feature: selected_feature.title().replace("_", " ")},
        color_discrete_sequence=['#00a8e8']
    )
    
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e0e0e0', family='Segoe UI'),
        hovermode='x unified'
    )
    
    fig.update_traces(marker_line=dict(color='#0066cc', width=1))
    return fig


@app.callback(
    Output('scatter-relationship', 'figure'),
    Input('x-feature', 'value'),
    Input('y-feature', 'value')
)
def update_relationship(x_feature, y_feature):
    if not x_feature or not y_feature:
        return px.scatter(title="Select X and Y features to display relationship")

    fig = px.scatter(
        data,
        x=x_feature,
        y=y_feature,
        opacity=0.6,
        title=f"{x_feature.title().replace('_',' ')} vs {y_feature.title().replace('_',' ')}",
        labels={x_feature: x_feature.title().replace("_", " "),
                y_feature: y_feature.title().replace("_", " ")},
        color_discrete_sequence=['#00a8e8']
    )

    fig.update_traces(marker=dict(size=8, line=dict(color='#0066cc', width=1)))
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#e0e0e0', family='Segoe UI'),
        hovermode='closest'
    )
    return fig


@app.callback(
    Output('qualitative-relationship', 'figure'),
    Input('qualitative-x', 'value'),
    Input('qualitative-hue', 'value')
)
def update_qualitative_graph(x_feature, hue_feature):
    if not x_feature or not hue_feature:
        return px.bar(title="Select two qualitative features to display")

    try:
        # Create a simple bar chart first
        fig = px.bar(
            data,
            x=x_feature,
            color=hue_feature,
            barmode='group',
            title=f"{x_feature.title().replace('_', ' ')} by {hue_feature.title().replace('_', ' ')}"
        )

        # Then customize the layout
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#e0e0e0', family='Segoe UI'),
            xaxis_title=x_feature.title().replace("_", " "),
            yaxis_title="Count",
            legend_title=hue_feature.title().replace("_", " "),
            bargap=0.2,
            hovermode='x unified',
            showlegend=True
        )
        
        # Update traces separately
        fig.update_traces(marker_line=dict(color='rgba(255,255,255,0.2)', width=0.5))
        
        return fig
    
    except Exception as e:
        print(f"Error in update_qualitative_graph: {e}")
        # Return a simple empty figure as fallback
        return go.Figure().add_annotation(
            text=f"Unable to display chart",
            showarrow=False,
            font=dict(color='#e0e0e0', size=14)
        )


if __name__ == "__main__":
    app.run(debug=True)