import dash
from dash import html, dcc
# from dash.dependencies import Input, Output, State,
from dash import dcc, html, callback, Output, Input, State
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import dash_table
import csv
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, select,update,insert
# from data.database import load_data_from_db
# selected_groups_str = ' '
# df=pd.read_csv('data/contacts.csv')
# Database configuration
DATABASE_URI = "mysql+pymysql://root:@localhost/phonebook"
engine = create_engine(DATABASE_URI)
metadata = MetaData()

# Reflect the existing table
rsucontacts_table = Table('rsucontacts', metadata, autoload_with=engine)

# Load the initial DataFrame from the database
def load_data_from_db():
    with engine.connect() as connection:
        query = "SELECT * FROM rsucontacts"
        df = pd.read_sql(query, connection)
    return df




df=load_data_from_db()
# groups=df['Group']
#df2=pd.read_csv('data/OOSC Conference participants.csv')
#org=df2['Type'].unique()
#dept=df2['Department'].unique()
#org=org.tolist()
dash.register_page(__name__, name='LSU Data Entry Update', external_stylesheets=[dbc.themes.BOOTSTRAP])
layout = html.Div([

    html.H5('Kindly update the tranfer-posting in your region'),


    html.P('Select one row then Edit RSU Contact information: '),html.Hr(),
    dcc.Input(id='update-search-input', type='text', placeholder='Enter search criteria'),
    # Dash DataTable
    dash_table.DataTable(
        id='editable-table',
        columns=[{'name': col, 'id': col, 'editable': True} for col in df.columns],

        data=df.to_dict('records'),  # Fill table with data
        # page_size=10,
        # editable=True,  # Makes table cells editable
        # row_deletable=True,  # Allow row deletion
        # style_table={'overflowX': 'auto'},  # Table overflow settings
        # style_cell={'textAlign': 'left', 'minWidth': '150px', 'width': '150px', 'maxWidth': '150px'}
        page_size=8,
    page_action='native',     # render all of the data at once
    row_selectable="single",
    row_deletable=False,
    editable=True,


    filter_action="native",
    sort_action="native",
    #style_table={ 'overflowY': 'auto',"overflowX": "auto"},#'height': '600px',
    style_table={"overflowX": "auto"},
    fixed_rows={'headers': True},
    style_cell={'color':'dark', 'text-align':'left'},
    ),

    # Save button
    html.Button('Save the changes !', id='save-button', n_clicks=0),

    # Confirmation text
    html.Div(id='save-confirmation', children='')
])

# # Callback to save edited table data to CSV
# @callback(
#     Output('save-confirmation', 'children'),
#     Input('save-button', 'n_clicks'),
#     State('editable-table', 'data'),
#     prevent_initial_call=True
# )
# def save_data(n_clicks, current_data):
#     # if n_clicks > 0 :
#     original_df = pd.read_csv('data/contacts.csv')
#         # Convert table data to DataFrame
#     current_df = pd.DataFrame(current_data)
#      # Check if the data has changed
#     if original_df.equals(current_df):
#         return 'No changes detected. Nothing to save.'
#     else:
#         # Save DataFrame to CSV
#         current_df.to_csv('data/contacts.csv', index=False)

#         return 'Data saved! in LSU Contact File!'

# @callback(
#     Output('editable-table', 'data'),
#     Output('editable-table', 'selected_rows'),
#     [Input('update-search-input', 'value'),

#      ],
#     prevent_initial_call=True,
#     allow_duplicate=True
# )
# def update_table(search_input):
#     selected_rows = []
#     if not search_input:
#         return df.to_dict('records'), selected_rows # If search input is empty, display all data
#     else:
#         # Filter the DataFrame based on the search criteria
#         filtered_df = df[df.apply(lambda row: any(search_input.lower() in str(cell).lower() for cell in row), axis=1)]

#         return filtered_df.to_dict('records'),selected_rows



# Callback to save edited table data to MySQL
@callback(
    Output('save-confirmation', 'children'),
    Input('save-button', 'n_clicks'),
    State('editable-table', 'data'),
    prevent_initial_call=True
)
def save_data(n_clicks, current_data):
    # Convert table data to DataFrame
    current_df = pd.DataFrame(current_data)

    # Load the original DataFrame from the database
    original_df = load_data_from_db()

    # Check if the data has changed
    if original_df.equals(current_df):
        return 'No changes detected. Nothing to save.'
    else:
        try:
            with engine.connect() as connection:
                # Update only the changed rows
                for _, row in current_df.iterrows():
                    stmt = (
                        update(rsucontacts_table)
                        .where(rsucontacts_table.c['S.No'] == row['S.No'])  # Use the primary key
                        .values(**row.to_dict())
                    )
                    connection.execute(stmt)
                connection.commit()

            return 'Data updated in MySQL database!'
        except Exception as e:
            return f'Error updating data: {str(e)}'

# Callback to update the table based on search input
@callback(
    Output('editable-table', 'data'),
    Output('editable-table', 'selected_rows'),
    Input('update-search-input', 'value'),
    prevent_initial_call=True
)
def update_table(search_input):
    selected_rows = []

    if not search_input:
        # If search input is empty, display all data
        return df.to_dict('records'), selected_rows
    else:
        # Filter the DataFrame based on the search criteria
        filtered_df = df[df.apply(lambda row: any(search_input.lower() in str(cell).lower() for cell in row), axis=1)]
        return filtered_df.to_dict('records'), selected_rows
    
