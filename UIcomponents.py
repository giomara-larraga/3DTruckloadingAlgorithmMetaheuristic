import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc

navbar = dbc.NavbarSimple(
    brand="3D Truck Load",
    brand_href="#",
    color="primary",
    dark=True,
)

upload = dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px 0'
        },
        multiple=False
    )

SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "24rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "25rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H5("3D Truck Load", className="display-8"),
        html.Hr(),
        html.P(
            "Please choose an Excel file containing the data for the container and the list of items. Next, specify the specific sheets within the file where this information can be found."
        ),
        upload,
        html.Div(id='file-name', style={'margin': '10px 0'}),
        dbc.Row([
            dbc.Col([
                html.P("Container: "),
            ], width=4),
            dbc.Col([
                dcc.Dropdown(id='sheet-dropdown1', placeholder='Select Page', className="form-control"),
            ], width=8),
        ], align="center", style={'margin': '10px 0'}),
        dbc.Row([
            dbc.Col([
                html.P("Items: "),
            ], width=4),
            dbc.Col([
                dcc.Dropdown(id='sheet-dropdown2', placeholder='Select Page', className="form-control"),
            ], width=8),
        ], align="center", style={'margin': '10px 0'}),
        dcc.Store(id='options-store', data=[]),  # Store for options
        dcc.Store(id='container-store', data=[]),  # Store for container DataFrame
        dcc.Store(id='items-store', data=[]),  # Store for items DataFrame
        html.Div([
                dbc.Row([
                    dbc.Col(html.Button('Heuristic', id='heuristic-btn'), width="auto"),
                    dbc.Col(html.Button('Exact method', id='exact-method-btn'), width=True),
                ], align="center", justify="between"),  # Align columns to the left and right edges of the container
            ], style={'margin': '10px 0'}),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='output-data-upload'),
    html.Div(id='output-div')],
    style=CONTENT_STYLE, id="page-content")