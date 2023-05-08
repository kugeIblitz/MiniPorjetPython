import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
import sqlite3
from dash.dependencies import Input, Output, State

#-------------------------------------------------Connecting to the database------------------------------------------------------------
#? Creating a database and saving the data in it
conn = sqlite3.connect('jumiaSmartPhones.db')
c = conn.cursor()

#------------------------------------------------------
query = 'SELECT brandName FROM brand'
cursor = conn.execute(query)
#? Retrieve brand names from SQLite database
brand_names = [row[0] for row in cursor.fetchall()]

#-------------------------------------------------Dash interface----------------------------------------------------

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LUX])

# Define the layout of the app
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1('Smartphones Filter', className='display-3 mb-4'),
            html.Label('Select brand: ', className='form-label'),
             dcc.Dropdown(
                    id='brand-dropdown',
                    
                    options=[{'label': name, 'value': name} for name in brand_names],
                    value="Any",
                    className='form-select'
                ),
            html.Label('Max price: ', className='form-label'),
            dcc.Input(
                id='price-input',
                type='number',
                min=0,
                max=99999,
                value=None,
                className='form-control'
            ),
            html.Button('Filter', id='filter-button', className='btn btn-primary mt-3'),
            html.Hr(className='my-4'),
            html.Div(id='filtered-smartphones')
        ])
    ])
], fluid=True)

@app.callback(
    Output('filtered-smartphones', 'children'),
    [Input('filter-button', 'n_clicks')],
    [State('price-input', 'value'), State('brand-dropdown', 'value')]
)
def update_filtered_smartphones(n_clicks, price, brand):
    if n_clicks:
        conn = sqlite3.connect('jumiaSmartPhones.db')
        if price:
            query = 'SELECT nom,imgURL,price FROM SmartPhone WHERE price <= ? AND brand = ?'
            cursor = conn.execute(query, (price, brand))
        else:
            query = 'SELECT nom,imgURL,price FROM SmartPhone WHERE brand = ?'
            cursor = conn.execute(query, (brand,))
        data = cursor.fetchall()
        paragraphs = []
        if data:
            for d in data:
                paragraph_text = d[0]
                img_url = d[1]
                price = d[2]
                paragraph = html.P([
                    html.Img(src=img_url),
                    paragraph_text," ",
                    price,"DT"
                ], className='lead')
                paragraphs.append(paragraph)
            return html.Div(paragraphs)
        else:
            return html.P('No smartphones found for the selected criteria', className='lead text-muted')
    else:
        conn = sqlite3.connect('jumiaSmartPhones.db')
        query = 'SELECT nom,imgURL,price FROM SmartPhone'
        cursor = conn.execute(query)
        data = cursor.fetchall()
        paragraphs = []
        if data:
            for d in data:
                paragraph_text = d[0]
                img_url = d[1]
                price = d[2]
                paragraph = html.P([
                    html.Img(src=img_url),
                    paragraph_text," ",
                    price,"DT"
                ], className='lead')
                paragraphs.append(paragraph)
            return html.Div(paragraphs)

if __name__ == '__main__':
    app.run_server(debug=True)
