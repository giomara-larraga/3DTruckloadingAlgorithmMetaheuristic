import numpy as np
import pandas as pd
import json
import io
import base64
import os
import dash_bootstrap_components as dbc
import dash
from dash import dcc, html, Input, Output, State
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output
from random import randint
from UIcomponents import sidebar, content
from container_loading_metaheuristic import container_loading

CONTENT_STYLE = {
    "margin-left": "10rem",
    "margin-right": "10rem",
    "padding": "2rem 2rem",
}

# Initialize the Dash app
app = dash.Dash(
    __name__, external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP]
)

server = app.server
# Define the layout of the app
app.layout = html.Div(
    [
        sidebar,
        content,
    ]
)


# Define the callback to update options in the Store
@app.callback(Output("options-store", "data"), [Input("upload-data", "contents")])
def update_options(contents):
    if contents is None:
        raise PreventUpdate

    content_type, content_string = contents.split(",")
    decoded = base64.b64decode(content_string)

    try:
        xl = pd.ExcelFile(io.BytesIO(decoded))
        sheet_names = xl.sheet_names
        options = [{"label": sheet, "value": sheet} for sheet in sheet_names]
        return options
    except Exception as e:
        print(f"Error updating options: {e}")
        return []


# Define the callback to update dropdown options
@app.callback(
    [Output("sheet-dropdown1", "options"), Output("sheet-dropdown2", "options")],
    [Input("options-store", "data")],
)
def update_dropdown_options(options_data):
    return [options_data, options_data]


# Define the callback to read uploaded file and display data
@app.callback(
    [
        Output("output-data-upload", "children"),
        Output("container-store", "data"),
        Output("items-store", "data"),
        Output("is-valid-entry", "data"),
    ],
    [
        Input("options-store", "data"),
        Input("sheet-dropdown1", "value"),
        Input("sheet-dropdown2", "value"),
    ],
    [State("upload-data", "filename"), State("upload-data", "contents")],
)
def update_and_display_table(options, sheet_name1, sheet_name2, filename, contents):
    if options is None:
        raise PreventUpdate

    try:
        if sheet_name1 and sheet_name2 and contents:
            content_type, content_string = contents.split(",")
            decoded = base64.b64decode(content_string)
            container = pd.read_excel(io.BytesIO(decoded), sheet_name=sheet_name1)
            items = pd.read_excel(io.BytesIO(decoded), sheet_name=sheet_name2)

            table1 = html.Div(
                [
                    html.H5("Container Information"),
                    dbc.Table.from_dataframe(
                        container, striped=True, bordered=True, hover=True
                    ),
                ]
            )

            table2 = html.Div(
                [
                    html.H5("List of Items"),
                    dbc.Table.from_dataframe(
                        items, striped=True, bordered=True, hover=True
                    ),
                ]
            )
            required_columns = ["Item_ID", "Length", "Width", "Height", "Weight"]
            required_columns_2 = [
                "Item_ID",
                "Quantity",
                "Length",
                "Width",
                "Height",
                "Weight",
                "Type",
                "Stackable",
            ]

            is_valid_entry = all(
                col in container.columns for col in required_columns
            ) and all(col in items.columns for col in required_columns_2)

            if not is_valid_entry:
                error_message = (
                    "The Container page must have the following columns: Item_ID, Length, Width, Height, Weight; "
                    "and the Items page must have the following columns: Item_ID, Quantity, Length, Width, Height, Weight, Type, Stackable."
                )
                return (
                    dbc.Alert(
                        [error_message],
                        color="danger",
                        className="d-flex align-items-center",
                    ),
                    "[]",
                    "[]",
                    is_valid_entry,
                )
            return (
                [table1, table2],
                container.to_json(),
                items.to_json(),
                is_valid_entry,
            )
        else:
            return html.Div(""), "[]", "[]", False
    except Exception as e:
        return html.Div([f"Error: {str(e)}"]), "[]", "[]", False


# Define the callback to display file name
@app.callback(Output("file-name", "children"), [Input("upload-data", "filename")])
def display_filename(filename):
    if filename:
        return html.Div(f"Selected file: {filename}")
    else:
        return html.Div()


@app.callback(
    [
        Output("output-data-upload-results", "children"),
        Output("output-data-upload", "style"),
    ],
    State("container-store", "data"),
    State("items-store", "data"),
    [Input("compute-button", "n_clicks"), Input("is-valid-entry", "data")],
)
def update_output(container, items, n_clicks, isValid):
    ctx = dash.callback_context
    if not ctx.triggered:
        raise PreventUpdate
    elif ctx.triggered[0]["prop_id"].split(".")[0] == "compute-button":
        if n_clicks is None or not (isValid):
            return " ", {"display": "block"}
        else:
            # Perform computation or handle click event here
            json_data = container_loading(container, items)
            return html.Pre(json_data, style={"display": "inline-block", "wordWrap": "break-word","overflowWrap": "break-word","text-wrap":"pretty","maxWidth": "100%"}), {"display": "none"}
    else:
        return dash.no_update, {"display": "block" }  # Hide the div

# Run the app
if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=False)
