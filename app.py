import dash
from dash import dcc, html, Input, Output, State
import pandas as pd
import base64
import io
from dash.exceptions import PreventUpdate
from dash.dependencies import ClientsideFunction
import dash_bootstrap_components as dbc
from UIcomponents import sidebar,content

# Initialize the Dash app with external CSS styles
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout of the app
app.layout = html.Div([
    dcc.Location(id="url"),
    sidebar,
    content,
])

# Define the callback to update options in the Store
@app.callback(Output('options-store', 'data'),
              [Input('upload-data', 'contents')])
def update_options(contents):
    if contents is None:
        raise PreventUpdate
    
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    
    try:
        xl = pd.ExcelFile(io.BytesIO(decoded))
        sheet_names = xl.sheet_names
        options = [{'label': sheet, 'value': sheet} for sheet in sheet_names]
        return options
    except Exception as e:
        print(f"Error updating options: {e}")
        return []

# Define the callback to update dropdown options
@app.callback([Output('sheet-dropdown1', 'options'),
               Output('sheet-dropdown2', 'options')],
              [Input('options-store', 'data')])
def update_dropdown_options(options_data):
    return [options_data, options_data]

# Define the callback to read uploaded file and display data
@app.callback([Output('output-data-upload', 'children'),
               Output('container-store', 'data'),
               Output('items-store', 'data')],
              [Input('options-store', 'data'),
               Input('sheet-dropdown1', 'value'),
               Input('sheet-dropdown2', 'value')],
              [State('upload-data', 'filename'),
               State('upload-data', 'contents')])
def update_and_display_table(options, sheet_name1, sheet_name2, filename, contents):
    if options is None:
        raise PreventUpdate
    
    try:
        if sheet_name1 and sheet_name2 and contents:
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)
            container = pd.read_excel(io.BytesIO(decoded), sheet_name=sheet_name1)
            items = pd.read_excel(io.BytesIO(decoded), sheet_name=sheet_name2)

            table1 = dbc.Table.from_dataframe(container, striped=True, bordered=True, hover=True)
            table2 = dbc.Table.from_dataframe(items, striped=True, bordered=True, hover=True)
            
            return [table1, table2], container.to_json(), items.to_json()
        else:
            return html.Div("Please select two pages."), '[]', '[]'
    except Exception as e:
        return html.Div([
            f'Error: {str(e)}'
        ]), '[]', '[]'


# Define the callback to display file name
@app.callback(Output('file-name', 'children'),
              [Input('upload-data', 'filename')])
def display_filename(filename):
    if filename:
        return html.Div(f'Selected file: {filename}')
    else:
        return html.Div()


@app.callback(Output('output-div', 'children'),
              [Input('heuristic-btn', 'n_clicks'),
               Input('exact-method-btn', 'n_clicks')])
def navigate_to_page(n_clicks_heuristic, n_clicks_exact_method):
    ctx = dash.callback_context
    if not ctx.triggered:
        return

    triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
    if triggered_id == 'heuristic-btn':
        return dcc.Location(pathname='/page1')
    elif triggered_id == 'exact-method-btn':
        return dcc.Location(pathname='/page2')

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
