import dash
from dash import dcc, html, callback, Output, Input,dash_table,State
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
from data.database import fetch_contacts
from clipboard import copy
import pyperclip


dash.register_page(__name__, name='RSU-PhoneBook', external_stylesheets=[dbc.themes.SPACELAB],meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5, user-scalable=no'}])

#-----------------------------------------------------------------------------
# df= pd.read_csv('/home/DigitalDirectory/data/WCD participants list confirmation.csv')
# df= pd.read_csv('data/rsucontacts.csv')
df=fetch_contacts()
total = html.Div(id="total", style={"textAlign": "right"})
#
#-----------------------------------------------------------------------------

layout = html.Div([



    dbc.Row([

            dbc.Col([

                html.Div(id='contact-info', children=[]),
                # dcc.Clipboard(id="clip", style={"fontSize": 20}),
                # html.Div(id='output-container',children=["Digital Directory: make a copy here:"]), #"Digital Directory: make a copy here:"
            ],width=6),


            # dbc.Col([
            #     dcc.Clipboard(id="clip", style={"fontSize": 20}),
                # html.Div("Digital Directory: you can make a copy here:"),
            #  ],width=6),

            ]),
            html.Hr(),

    dbc.Row([


            dbc.Col([
                dcc.Input(id='search-input', type='text', placeholder='Enter search criteria'),
                html.Div('🔍 Select to Display Contact Informtion : '),
                dash_table.DataTable(id="table",

                                data=df.to_dict('records'),
                                columns=[{'id': c, 'name': c} for c in df.columns],

                    #-----------------------------------------------------------------------------
# Vertical Scroll (without Pagination)
#-----------------------------------------------------------------------------
    # page_size=10,
    page_action='native',     # render all of the data at once
    row_selectable="single",
    row_deletable=False,
    editable=True,
    page_size=25,


    filter_action="native",
    sort_action="native",
    #style_table={ 'overflowY': 'auto',"overflowX": "auto"},#'height': '600px',
    style_table={"overflowX": "auto"},
    fixed_rows={'headers': True},
    style_cell={'color':'dark', 'text-align':'left'},


    # If you have more than 1000 rows, your browswer will slow down. Therefore,
    # for over 1000 rows, use pagination as per examples below or virtualization
    # as per last example.

#-----------------------------------------------------------------------------
# Fronent Pagination with Vertical Scroll
#-----------------------------------------------------------------------------
    # page_action='native',   # all data is passed to the table up-front
    # page_size=10,           # only 10 rows are displayed at a time
    # style_table={'height': '200px', 'overflowY': 'auto'}

#-----------------------------------------------------------------------------
# Fronent Pagination without Vertical Scroll
#-----------------------------------------------------------------------------
    # page_action='native',     # all data is passed to the table up-front
    # page_size=10,             # but only 10 rows are displayed at a time

    # If you have over 10,000 rows you should do pagination in the backend
    # to lower network costs and memory. See how with link below:
    # https://dash.plotly.com/datatable/callbacks

#-----------------------------------------------------------------------------
# Vertical Scroll With Fixed Headers
#-----------------------------------------------------------------------------
    # fixed_rows={'headers': True},
    # style_table={'height': 400}  # defaults to 500

    # By default and without wrapping, each row takes up 30px. So 10 rows with
    # one header would set the table to be 330px tall.
    # Since here we have 18 rows+header, that would equal 570px.

#-----------------------------------------------------------------------------
# Width of Headers (partial text)
#-----------------------------------------------------------------------------

    # If the headers are wider than the cells and the table's container isn't wide
    # enough to display all of the headers, then the column headers will be truncated

    # data=df_numeric.to_dict('records'),
    # columns=[{'id': c, 'name': c} for c in df_numeric.columns],

    # fixed_rows={'headers': True}

#-----------------------------------------------------------------------------
# Width of Headers (full text)
#-----------------------------------------------------------------------------
    # fixed_rows={'headers': True},
    # style_cell={
    #     'minWidth': 95, 'maxWidth': 95, 'width': 95
    # }

#-----------------------------------------------------------------------------
# Vertical Scroll with Virtualization
#-----------------------------------------------------------------------------
    # virtualization=True,            # to use when you have over 1000 rows
    # fixed_rows={'headers': True},
    # style_cell={'minWidth': 95, 'width': 95, 'maxWidth': 95}, #set width when using virtualization
    # style_table={'height': 300}     # default is 500px

#----------------------------------------------------------------
),]),
])
])




# @callback(
#     Output('table', 'data'),
#     [Input('search-input', 'value')],
#     prevent_initial_call=True,
#     allow_duplicate=True
# )
# def update_table(search_input):

#     if not search_input:
#         return df.to_dict('records')  # If search input is empty, display all data
#     else:
#         # Filter the DataFrame based on the search criteria
#         filtered_df = df[df.apply(lambda row: any(search_input.lower() in str(cell).lower() for cell in row), axis=1)]

#         return filtered_df.to_dict('records')

# @callback(
#     Output('contact-info', 'children'),
#     Output('contact-info', 'style'),
#     [Input('table', 'selected_rows')],
#     prevent_initial_call=True
# )
# def update_selected_contact_info(selected_rows):

#     if not selected_rows:
#         return [], {'display': 'none'}

#     selected_contact = df.iloc[selected_rows[0]]
#     contact_info = [

#             html.H4("📞 Contact Information :"),
#             html.P(f"Full Name : {selected_contact.get('Name', '')}"),
#             html.P(f"Designation: {selected_contact.get('Designation', '')}"),
#             html.P(f"Department: {selected_contact.get('Department', '')}"),
#             html.P(f"District: {selected_contact.get('District', '')}"),
#             html.P(f"Email: {selected_contact.get('Email', '')}"),
#             html.P(f"Contact No: {selected_contact.get('Cell No', '')}"),
#             html.P(f"Postal Address: {selected_contact.get('Postal Address', '')}"),
#         # Add more fields as needed
#     ]
#     style = {'border': '4px solid #ddd', 'padding': '2px', 'border-radius': '5px'}
#     return contact_info,style

@callback(
    Output('table', 'data'),
    [Input('search-input', 'value')],
    prevent_initial_call=True,
    allow_duplicate=True
)
def update_table(search_input):
    if not search_input:
        return df.to_dict('records')  # If search input is empty, display all data
    else:
        # Filter the DataFrame based on the search criteria
        filtered_df = df[df.apply(lambda row: any(search_input.lower() in str(cell).lower() for cell in row), axis=1)]
        return filtered_df.to_dict('records')

@callback(
    Output('contact-info', 'children'),
    Output('contact-info', 'style'),
    [Input('table', 'selected_rows'),
     Input('search-input', 'value')],
    prevent_initial_call=True
)
def update_selected_contact_info(selected_rows, search_input):
    if not selected_rows:
        return [], {'display': 'none'}

    # Get the filtered DataFrame based on the search input
    if search_input:
        filtered_df = df[df.apply(lambda row: any(search_input.lower() in str(cell).lower() for cell in row), axis=1)]
    else:
        filtered_df = df

    # Map the selected row index from the filtered DataFrame to the original DataFrame
    selected_row_index = filtered_df.index[selected_rows[0]]
    selected_contact = df.iloc[selected_row_index]

    # Display the contact information
    contact_info = [
        html.H4("📞 Contact Information :"),
        html.P(f"Full Name : {selected_contact.get('Name', '')}"),
        html.P(f"Designation: {selected_contact.get('Designation', '')}"),
        html.P(f"Department: {selected_contact.get('Department', '')}"),
        html.P(f"District: {selected_contact.get('District', '')}"),
        html.P(f"Email: {selected_contact.get('Email', '')}"),
        html.P(f"Contact No: {selected_contact.get('Cell No', '')}"),
        html.P(f"Postal Address: {selected_contact.get('Postal Address', '')}"),
    ]
    style = {'border': '4px solid #ddd', 'padding': '2px', 'border-radius': '5px'}
    return contact_info, style
