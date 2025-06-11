import dash
from dash import dcc, html, callback, Output, Input,dash_table,State
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
from data.database import fetch_lsucontacts, fetch_contacts


dash.register_page(__name__, name='LSU-PhoneBook', external_stylesheets=[dbc.themes.SPACELAB])



#-----------------------------------------------------------------------------
# df= pd.read_csv('data/contacts.csv')
df=fetch_lsucontacts()
total = html.Div(id="total", style={"textAlign": "left"})
#
#-----------------------------------------------------------------------------

layout = html.Div([

    # html.Div("Digital Directory: you can make a copy here:"),
    # dcc.Clipboard(id="lsuclip", style={"fontSize": 20}),
    html.Div(id='lsucontact-info',title="Digital Directory: Contact here:", children=[]),
    dcc.Clipboard(id="lsuclip", style={"fontSize": 20}), html.Div(id='lsu-contact-info',title="Digital Directory: Contact here:", children=["Select to display Contact info:"]),

    dcc.Download(id="download"),
    html.Button("Download Contacts in Excel", id="download-button", n_clicks=0,style={'margin-top': '10px', 'backgroundColor': '#5db4c6','borderRadius': '5px','color': 'white', 'border': 'none', 'padding': '10px 10px','cursor': 'pointer', 'text-align': 'center', 'text-decoration': 'none', 'display': 'inline-block', 'font-size': '16px'}),
     html.Button('Reload Table', id='reload-table-btn', n_clicks=0, style={'margin-top': '10px', 'backgroundColor': '#5db4c6','borderRadius': '50%','color': 'white', 'border': 'none', 'padding': '10px 20px', 'text-align': 'center', 'text-decoration': 'none', 'display': 'inline-block', 'font-size': '16px'}),

    dash_table.DataTable(id="lsutable",

                                data=df.to_dict('records'),
                                columns=[{'id': c, 'name': c} for c in df.columns],

                    #-----------------------------------------------------------------------------
# Vertical Scroll (without Pagination)
#-----------------------------------------------------------------------------
    page_size=25,
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
    # https://dash.plotly.com/datatable/ callbacks

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
),
])
# @callback(
#     Output("lsuclip", "content"),
#     Input("lsuclip", "n_clicks"),
#     Input("store", "data"),
#     State("lsutable", "data"),
#     prevent_initial_call=True,
#     allow_duplicate=True
#     )

# def custom_copy(n_clicks,content, data):
#     dff = pd.DataFrame(data)
#     return dff.to_csv(index=False)


@callback(
    Output('lsutable', 'data'),
    # Output('store', 'data'),

    [Input('reload-table-btn', 'n_clicks')],
    allow_duplicate=True,
    prevent_initial_call=True

)
def reload_data(n_clicks):
    # Read data from CSV
    df = pd.read_csv('data/contacts.csv')
    # data= df.to_dict('records')
    return df.to_dict('records')

# Callback to update the download link
@callback(
    Output("download", "data"),
    [Input("download-button", "n_clicks")],
    prevent_initial_call=True
)
def download_csv(n_clicks):
    filename = 'contacts.csv'
    df.to_csv(filename, index=False)
    return dict(content=df.to_csv(index=False), filename=filename)


# display contact info
@callback(
    Output('lsucontact-info', 'children'),
    Output('lsucontact-info', 'style'),
    [Input('lsutable', 'selected_rows')],
    allow_duplicate=True,
    prevent_initial_call=True)
def update_selected_contact_info(selected_rows):
    if not selected_rows:
        return [], {'display': 'none'}

    selected_contact = df.iloc[selected_rows[0]]
    contact_info = [
        html.H4(f"Contact Information for:"),
        html.P(f"Full Name : {selected_contact.get('First Name', '')} {selected_contact.get('Middle Name', '')} {selected_contact.get('Last Name', '')}"),
        html.P(f"Designation: {selected_contact.get('Designation', '')}"),
        html.P(f"Department: {selected_contact.get('Department', '')}"),
        html.P(f"District: {selected_contact.get('District', '')}"),
        html.P(f"Email: {selected_contact.get('Email', '')}"),
        html.P(f"Contact No: {selected_contact.get('Cell No', '')}"),
        html.P(f"Postal Address: {selected_contact.get('Postal Address', '')}"),
        # Add more fields as needed
    ]
    style = {'border': '2px solid #ddd', 'padding': '10px', 'border-radius': '5px'}
    return contact_info,style

