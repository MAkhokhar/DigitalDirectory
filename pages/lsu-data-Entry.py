import dash
from dash import html, dcc
# from dash.dependencies import Input, Output, State,
from dash import dcc, html, callback, Output, Input, State
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import dash_table
import csv
# import pandas as pd
# from data.database import fetch_contacts, insert_contact
from sqlalchemy import create_engine, MetaData, Table, select, text, insert
import pandas as pd
import logging
# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('rsu_dashboard.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('RSU Dashboard')
DATABASE_URI = "mysql+pymysql://root:@localhost/phonebook"
engine = create_engine(DATABASE_URI)
metadata = MetaData()
rsucontacts_table = Table('rsucontacts', metadata, autoload_with=engine)

def add_contact_to_rsucontacts(contact_data):
    """
    Insert contact data into the rsucontacts table in the MySQL database.
    
    Args:
        contact_data (dict): Dictionary containing contact details with keys:
            Name, Gender, Designation, Organisation, Department, Group, Email,
            Cell No, Home phone No, Landline / Fax, CNIC, Postal Address,
            Union Council, District, Tehsil
    
    Returns:
        bool: True if insertion is successful, False otherwise
    """
    try:
        if not contact_data.get('Name') or not contact_data.get('Gender'):
            logger.warning("Attempted to insert contact with missing Name or Gender")
            return False
        
        with engine.connect() as conn:
            conn.execute(
                insert(rsucontacts_table),
                contact_data
            )
            conn.commit()
        
        logger.info(f"Contact added successfully: {contact_data['Name']}")
        return True
    
    except Exception as e:
        logger.error(f"Failed to add contact: {str(e)}")
        return False    
# selected_groups_str = ' '
df=pd.read_csv('data/contacts.csv')

groups=df['Group']
df2=pd.read_csv('data/OOSC Conference participants.csv')
org=df2['Type'].unique()
dept=df2['Department'].unique()
#org=org.tolist()
dash.register_page(__name__, name='LSU Data Entry Form', external_stylesheets=[dbc.themes.BOOTSTRAP])

others_output=  dbc.Form([

                                    dbc.Label('Other Group: ',className='text-start', style={'color':'blue','display': 'inline-block', 'width': '150px', 'text-align': 'left', 'vertical-align': 'middle'}),
                                   dcc.Input(id='group', type='text', required=True,placeholder='Group or Project name if any...')
                                ],
                                className='mb-3'
                            ),

# Define the layout of the app
layout = html.Div([
    dbc.Container(
    [

        dbc.Row(
            [
                dbc.Col(
                    dbc.Form(
                        [html.H6('Enter personal information :', className='text-left'),
                            dbc.Form(
                                [
                                    dbc.Label('First Name  ',className='text-start', style={'color':'blue','display': 'inline-block', 'width': '150px', 'text-align': 'left', 'vertical-align': 'middle'}),
                                    dcc.Input(id='first_name', type='text', placeholder='First Name',required=True, className='text-start')
                                ],
                                className='mb-3'
                            ),
                             dbc.Form(
                                [
                                    dbc.Label('Middle Name  ',className='text-start',style={'color':'blue','display': 'inline-block', 'width': '150px', 'text-align': 'left', 'vertical-align': 'left'}),
                                    dcc.Input(id='middle_name', type='text', placeholder='Middle Name',required=True,className='text-start')
                                ],
                                className='mb-3'
                            ),
                            dbc.Form(
                                [
                                    dbc.Label('Last Name   ',className='text-start',style={'color':'blue','display': 'inline-block', 'width': '150px', 'text-align': 'left', 'vertical-align': 'left'}),
                                    dcc.Input(id='last_name', type='text', placeholder='tribe',className='text-start')
                                ],
                                className='mb-3'
                            ),
                             dbc.Form(
                                [
                                    # dbc.Label('Gender  ',className='text-start',style={'color':'blue','display': 'inline-block', 'width': '150px', 'text-align': 'left', 'vertical-align': 'left'}),
                                    # dcc.Input(id='gender', type='text',required=False, placeholder='Male or Female',className='text-start')
                                
                                    dbc.Label('Gender  ',className='text-start',style={'color':'blue','display': 'inline-block', 'width': '150px', 'text-align': 'left', 'vertical-align': 'left'}),
                                dcc.Dropdown(
                                    id='gender',
                                    options=[
                                        {'label': 'Male', 'value': 'Male'},
                                        {'label': 'Female', 'value': 'Female'}
                                    ],
                                    placeholder='Select Gender',
                                    # className='form-select mb-3'
                                ),
                                ],
                                className='mb-3'
                            ),
                            dbc.Form(
                                [
                                    dbc.Label('Designation  ',className='text-start', style={'color':'blue','display': 'inline-block', 'width': '150px', 'text-align': 'left', 'vertical-align': 'middle'}),
                                    dcc.Input(id='designation', type='text', placeholder='job-Title',required=True)
                                ], className='mb-3'
                            ),
                            dbc.Form(
                                [
                                    dbc.Label('CNIC',className='text-start',style={'color':'blue','display': 'inline-block', 'width': '150px', 'text-align': 'left', 'vertical-align': 'left'}),
                                    dcc.Input(id='cnic', type='text', placeholder='cnic-optional',className='text-start')
                                ],
                                className='mb-3'
                            ),
                             dbc.Form(
                                [
                                    dbc.Label(' postal-Address ',className='text-start',style={'color':'blue','display': 'inline-block', 'width': '150px', 'text-align': 'left', 'vertical-align': 'left'}),
                                    dcc.Input(id='postal_address', type='text', placeholder='address',className='text-start')
                                ],
                                className='mb-3'
                            ),




                             dbc.Form(
                                [
                                    dbc.Label('Email     ',className='text-start', style={'color':'blue','display': 'inline-block', 'width': '150px', 'text-align': 'left', 'vertical-align': 'left'}), #style={'display': 'inline-block', 'width': '150px', 'text-align': 'right', 'vertical-align': 'middle'}
                                    dcc.Input(id='email', type='email', placeholder='email',required=True, className='text-start')
                                ],
                                className='mb-3'
                            ),
                             dbc.Form(
                                [
                                    dbc.Label('Cell No   ',className='text-start', style={'color':'blue','display': 'inline-block', 'width': '150px', 'text-align': 'left', 'vertical-align': 'left'}),
                                    dcc.Input(id='mobile_no', type='number', placeholder='03xxxxxxxxx',required=True, className='text-start')
                                ],
                                className='mb-3'
                            ),
                            dbc.Form(
                                [
                                    dbc.Label('Home phone No   ',className='text-start', style={'color':'blue','display': 'inline-block', 'width': '150px', 'text-align': 'left', 'vertical-align': 'left'}),
                                    dcc.Input(id='home_phone', type='number', placeholder='mobile no',  className='text-start')
                                ],
                                className='mb-3'
                            ),
                            # Add more form fields here0

                        ]#,style={'border': '1px solid #ccc', 'padding': '20px', 'background-color': '#f2f2f2', 'position': 'relative','display':' -ms-flexbox'},

                    )
                ),
                #---------------------------------------------------------------------------------------------
            dbc.Col(
                    dbc.Form(
                        [html.H6('Enter departmental information :', className='text-left'),

                           dbc.Form(
                                [
                                    dbc.Label('Organisation ',className='text-start', style={'color':'blue','display': 'inline-block', 'width': '150px', 'text-align': 'left', 'vertical-align': 'middle'}),
                                    #dcc.Input(id='types', type='text',required=True, placeholder='NGO.GoS....')
                                    dcc.Dropdown(
                                            id='types',
                                            options=[{'label': org, 'value': org} for org in set(org)],
                                            value=None,  # Default value
                                            multi=False  # Set to True if you want to allow multiple selections
                                        ),

                                ],
                                className='mb-3'
                            ),
                            dbc.Form(
                                [

                                    dbc.Label('Department  ',className='text-start', style={'color':'blue','display': 'inline-block', 'width': '150px', 'text-align': 'left', 'vertical-align': 'middle'}),
                                     dcc.Input(id='department', type='text', placeholder='department',required=True)
                                    # dcc.Dropdown(
                                    #         id='department',
                                    #         options=[{'label': dept, 'value': dept} for dept in set(dept)],
                                    #         value=None,  # Default value
                                    #         multi=False  # Set to True if you want to allow multiple selections
                                    #     ),
                                ],
                                className='mb-3'
                            ),

                            dbc.Form(
                                [
                                 dbc.Label("Select Groups:",className='text-start', style={'color':'blue','display': 'inline-block', 'width': '150px', 'text-align': 'left', 'vertical-align': 'middle'}),
                                 dcc.Checklist(
                                        id='group_checkboxes',
                                        options=[

                                            # {'label': 'OTHERS', 'value': 'others'},
                                            {'label': 'LEG', 'value': 'leg'},
                                            {'label': 'DEG', 'value': 'deg'},
                                            {'label': 'DRR', 'value': 'drr'},

                                            {'label': 'ECE', 'value': 'ece'},
                                            {'label': 'CTT', 'value': 'ctt'},
                                            {'label': 'PRC', 'value': 'prc'},
                                            {'label': 'CRC', 'value': 'crc'},
                                            {'label': 'RSC', 'value': 'rsc'},

                                            {'label': 'DROC', 'value': 'droc'},
                                            {'label': 'PROC', 'value': 'proc'},


                                            {'label': 'TWG', 'value': 'twg'},
                                            {'label': 'NFE', 'value': 'nfe'},
                                            {'label': 'PET', 'value': 'pet'},
                                            {'label': 'CWG', 'value': 'cwg'},
                                            {'label': 'GWG', 'value': 'gwg'},
                                            {'label': 'SDG-4', 'value': 'sdj-4'},

                                            {'label': 'JSER', 'value': 'jser'},
                                            {'label': 'OOSC', 'value': 'oosc'},
                                            {'label': 'DOSC', 'value': 'dosc'},
                                            {'label': 'POSC', 'value': 'posc'},
                                            {'label': 'TOSC', 'value': 'tosc'},
                                            {'label': 'SESP&R', 'value': 'sesp-r'},





                                        ],
                                        value=[],  # Initially, none are selected
                                        inline=True,

                                        style={
                                            'columnCount': 6,  # Number of columns
                                            'width': '100%',  # Adjust width as needed
                                            'padding': '20px',
                                            'border': '2px  solid #ccc',
                                        }
                                         ),
                                 html.Div(id='selected-groups-output',children=[]),

                                 ],className='mb-3'
                                ),

                            dbc.Form(
                                [

                                    dbc.Label('Other Group: ',className='text-start', style={'color':'blue','display': 'inline-block', 'width': '150px', 'text-align': 'left', 'vertical-align': 'middle'}),
                                    dcc.Input(id='group', type='text', required=False,placeholder='Group or Project name if any...')
                                ],
                                className='mb-3'
                            ),

                            # dbc.Form(
                            #     [

                            #         dbc.Label('Date-Of-Joining  ',className='text-start', style={'color':'blue','display': 'inline-block', 'width': '150px', 'text-align': 'left', 'vertical-align': 'middle'}),
                            #         dcc.Input(id='doj', type='text', required=True,placeholder='DOJ')
                            #     ],
                            #     className='mb-3'
                            # ),

                             dbc.Form(
                                [
                                    dbc.Label('Landline / Fax ',className='text-start', style={'color':'blue','display': 'inline-block', 'width': '150px', 'text-align': 'left', 'vertical-align': 'middle'}),
                                    dcc.Input(id='ptcl', type='text', placeholder='ptcl no if any',)
                                ],
                                className='mb-3'
                            ),
                            dbc.Form(
                                [
                                    dbc.Label('Union Council ',className='text-start', style={'color':'blue','display': 'inline-block', 'width': '150px', 'text-align': 'left', 'vertical-align': 'middle'}),
                                    dcc.Input(id='uc', type='text', placeholder='Union Council...')
                                ],
                                className='mb-3'
                            ),


                            dbc.Form(
                                [
                                    dbc.Label('District ',className='text-start', style={'color':'blue','display': 'inline-block', 'width': '150px', 'text-align': 'left', 'vertical-align': 'middle'}),
                                    dcc.Input(id='district', required=True, type='text', placeholder='District....')
                                ],
                                className='mb-3'
                            ),
                             dbc.Form(
                                [
                                    dbc.Label('Tehsil ',className='text-start', style={'color':'blue','display': 'inline-block', 'width': '150px', 'text-align': 'left', 'vertical-align': 'middle'}),
                                    dcc.Input(id='tehsil', type='text', placeholder='Tehsil....')
                                ],
                                className='mb-3'
                            ),
                            # Add more form fields hereUnion Council
                             #dbc.Button('Submit', id='submit-button')
                            dbc.Button('Submit', id='submit-btn', color='primary', className='mt-3')
                        ]
                    ),className='form-group row'


                )
            ], style={'border': '1px solid #ccc', 'padding': '20px', 'background-color': '#f2f2f2', 'position': 'relative','display':' -ms-flexbox'},

            justify='center',


        ),

]),

 dash_table.DataTable(id='datatable-output', columns=[], page_size=100,
    page_action='native',     # render all of the data at once
    row_selectable="single",
    row_deletable=True,
    editable=False),
    dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle("RSU Digital Directory:")),
                dbc.ModalBody(id='modal-body'),
                dbc.ModalFooter(
                    dbc.Button(
                        "Close", id="close", className="ms-auto", n_clicks=0
                    )
                ),
            ],
            id="modal",
            is_open=False,
        ),
])

# selected_groups_str = ', ',
#callback  for checkbox
@callback(
    Output('selected-groups-output', 'children'),
    [Input('group_checkboxes', 'value')],
    prevent_initial_call=True,
    allow_duplicate=True
)
def update_output(selected_groups):
    #print(selected_groups_str)

    if not selected_groups:
        return "No groups selected."
    elif selected_groups==['others']:
        return others_output

    else:
        output_text=f"Selected Groups: {', '.join(selected_groups)}"
        return output_text


# Callback to update DataTable and save to CSV
@callback(
    #Output('output-dictionary', 'children'),,Output('first_name', 'value')
    # Output('first_name', 'value'),Output('middle_name', 'value'),
    Output('datatable-output', 'data'),
    Output('datatable-output', 'columns'),
    Output("modal", "is_open"),Output('modal-body', 'children'),

   [ Input('submit-btn', 'n_clicks'), Input("close", "n_clicks")],
   [ State('group_checkboxes', 'value'),
    State('first_name', 'value'),
    State('middle_name', 'value'),
    State('last_name', 'value'),
    State('gender', 'value'),
    State('cnic', 'value'),
    State('postal_address', 'value'),
    State('email', 'value'),
    State('mobile_no', 'value'),
    State('home_phone', 'value'),
    State('types', 'value'),
    State('department', 'value'),
    State('designation', 'value'),

    #State('doj', 'value'),
    State('group', 'value'),
    State('ptcl', 'value'),
    State('uc', 'value'),
    State('district', 'value'),
    State('tehsil', 'value'),
    State("modal", "is_open")],
    prevent_initial_call=True,
    allow_duplicate=True
)
def submit_form(n_clicks,n_close, selected_checkboxes,first_name , middle_name, last_name, gender, cnic, address, email, mobile_no, home_no,
                  types, department,designation,group, ptcl, uc,  district, tehsil,is_open):

   # Create a list of dictionaries with the selected checkboxes
    # data = [{"Checkbox": checkbox, "Checked": True} for checkbox in selected_checkboxes]
    # # Create columns based on the keys of the first dictionary
    # columns = [{"name": key, "id": key} for key in data[0].keys()]
    # print(selected_checkboxes)

    columns =[]
    dff=pd.read_csv('data/contacts.csv')
    existing_data = df.to_dict('records')
    if selected_checkboxes or n_clicks :
        group =','.join(selected_checkboxes)
        # existing_data =df.to_dict('records')
        if not first_name or not middle_name or not designation or not email or not mobile_no or not department or not district:
            model='Please fill all red entries'
            return existing_data, columns, not is_open, model
        else:
            try:
                    with open('data/contacts.csv', 'r') as csvfile:
                        reader = csv.DictReader(csvfile)
                        # for row in reader:
                        #     existing_data.append(row)
                        existing_data =dff.to_dict('records')
            except FileNotFoundError:
                    pass
            # Add new entry
       
        # Combine name parts
         
        full_name = f"{first_name} {middle_name} {last_name}".strip()
        
        # Prepare data dictionary with exact column names
        db_data = {
            'Name': full_name,
            'Gender': gender,
            'CNIC': cnic,
            'Postal Address': address,
            'Email': email,
            'Cell No': mobile_no,
            'Home phone No': home_no,
            'Designation': designation,
            'Organisation': types,
            'Department': department,
            #'Date-Of-Joining': doj,
            'Group': group,
            'Landline / Fax': ptcl,
            'Union Council': uc,
            'District': district,
            'Tehsil': tehsil,
            
            }
        new_entry = {
            'First Name': first_name,
            'Middle Name': middle_name,
            'Last Name': last_name,
            'Gender': gender,
            'CNIC': cnic,
            'Postal Address': address,
            'Email': email,
            'Cell No': mobile_no,
            'Home phone No': home_no,
            'Designation': designation,
            'Organisation': types,
            'Department': department,
            #'Date-Of-Joining': doj,
            'Group': group,
            'Landline / Fax': ptcl,
            'Union Council': uc,
            'District': district,
            'Tehsil': tehsil,
            }
        existing_data.append(new_entry)
        message = add_contact_to_rsucontacts(db_data)
        print(message)
        with open('data/contacts.csv', 'w', newline='') as csvfile:
                  fieldnames = list(new_entry.keys())
                  writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                  writer.writeheader()
                  writer.writerows(existing_data)       



        # Prepare data for DataTable
       
        columns = [{'name': col, 'id': col} for col in fieldnames]
        first_name=''
        middle_name=''
        model='thanks: For new Entry click on LSU Data Entry Form.'
        return existing_data, columns, not is_open, model

    return  dash.no_update

# # In your callback function for form submission
# @callback(
#     Output('submission-status', 'children'),
#     Input('submit-button', 'n_clicks'),
#     [ State('group_checkboxes', 'value'),
#     State('first_name', 'value'),
#     State('middle_name', 'value'),
#     State('last_name', 'value'),
#     State('gender', 'value'),
#     State('cnic', 'value'),
#     State('postal_address', 'value'),
#     State('email', 'value'),
#     State('mobile_no', 'value'),
#     State('home_phone', 'value'),
#     State('types', 'value'),
#     State('department', 'value'),
#     State('designation', 'value'),

#     #State('doj', 'value'),
#     State('group', 'value'),
#     State('ptcl', 'value'),
#     State('uc', 'value'),
#     State('district', 'value'),
#     State('tehsil', 'value'),
#     ]
# )
# def handle_submission(n_clicks, first_name, middle_name, last_name, gender, cnic, 
#                       postal_address, email, cell_no, designation, organisation, 
#                       department, district, tehsil, union_council):
#     if not n_clicks:
#         return ""
    
#     # Prepare data dictionary
#     contact_data = {
#         'First Name': first_name,
#         'Middle Name': middle_name,
#         'Last Name': last_name,
#         'Gender': gender,
#         'CNIC': cnic,
#         'Postal Address': postal_address,
#         'Email': email,
#         'Cell No': cell_no,
#         'Designation': designation,
#         'Organisation': organisation,
#         'Department': department,
#         'District': district,
#         'Tehsil': tehsil,
#         'Union Council': union_council
#     }
    
#     # Add to database
#     success, message = add_contact_to_db(contact_data)
    
#     if success:
#         return dbc.Alert(message, color="success")
#     else:
#         return dbc.Alert(message, color="danger")