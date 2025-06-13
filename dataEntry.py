# import dash
# from dash import dcc, html, Input, Output, State, callback
# import dash_bootstrap_components as dbc
# from sqlalchemy import create_engine, MetaData, Table, insert
# import logging
# import os

# # Configure logging
# logging.basicConfig(
#     level=logging.INFO,
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     handlers=[
#         logging.FileHandler('rsu_dashboard.log'),
#         logging.StreamHandler()
#     ]
# )
# logger = logging.getLogger('RSU Dashboard')

# # MySQL Database URI
# DATABASE_URI = "mysql+pymysql://root:@localhost/phonebook"

# # Initialize SQLAlchemy engine and table
# engine = create_engine(DATABASE_URI)
# metadata = MetaData()
# rsucontacts_table = Table('rsucontacts', metadata, autoload_with=engine)

# # Initialize the Dash app with a secret key
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# app.server.secret_key = os.urandom(24).hex()

# # Layout for contact insertion form
# app.layout = dbc.Container([
#     html.H1("Add Contact to RSU Directory", className="text-center mt-4"),
#     dbc.Row([
#         dbc.Col([
#             dbc.Card([
#                 dbc.CardBody([
#                     # Form inputs for each column (except S.No, which is auto-increment)
#                     dbc.Label("Name"),
#                     dcc.Input(id='name-input', type='text', placeholder='Enter Name', className='mb-3', style={'width': '100%'}),
                    
#                     dbc.Label("Gender"),
#                     dcc.Dropdown(id='gender-input', options=[
#                         {'label': 'Male', 'value': 'Male'},
#                         {'label': 'Female', 'value': 'Female'}
#                     ], placeholder='Select Gender', className='mb-3'),
                    
#                     dbc.Label("Designation"),
#                     dcc.Input(id='designation-input', type='text', placeholder='Enter Designation', className='mb-3', style={'width': '100%'}),
                    
#                     dbc.Label("Organisation"),
#                     dcc.Input(id='organisation-input', type='text', placeholder='Enter Organisation', className='mb-3', style={'width': '100%'}),
                    
#                     dbc.Label("Department"),
#                     dcc.Input(id='department-input', type='text', placeholder='Enter Department', className='mb-3', style={'width': '100%'}),
                    
#                     dbc.Label("Group"),
#                     dcc.Input(id='group-input', type='text', placeholder='Enter Group', className='mb-3', style={'width': '100%'}),
                    
#                     dbc.Label("Email"),
#                     dcc.Input(id='email-input', type='email', placeholder='Enter Email', className='mb-3', style={'width': '100%'}),
                    
#                     dbc.Label("Cell No"),
#                     dcc.Input(id='cellno-input', type='text', placeholder='Enter Cell No', className='mb-3', style={'width': '100%'}),
                    
#                     dbc.Label("Home Phone No"),
#                     dcc.Input(id='homephone-input', type='text', placeholder='Enter Home Phone No', className='mb-3', style={'width': '100%'}),
                    
#                     dbc.Label("Landline / Fax"),
#                     dcc.Input(id='landline-input', type='text', placeholder='Enter Landline/Fax', className='mb-3', style={'width': '100%'}),
                    
#                     dbc.Label("CNIC"),
#                     dcc.Input(id='cnic-input', type='text', placeholder='Enter CNIC', className='mb-3', style={'width': '100%'}),
                    
#                     dbc.Label("Postal Address"),
#                     dcc.Input(id='address-input', type='text', placeholder='Enter Postal Address', className='mb-3', style={'width': '100%'}),
                    
#                     dbc.Label("Union Council"),
#                     dcc.Input(id='unioncouncil-input', type='text', placeholder='Enter Union Council', className='mb-3', style={'width': '100%'}),
                    
#                     dbc.Label("District"),
#                     dcc.Input(id='district-input', type='text', placeholder='Enter District', className='mb-3', style={'width': '100%'}),
                    
#                     dbc.Label("Tehsil"),
#                     dcc.Input(id='tehsil-input', type='text', placeholder='Enter Tehsil', className='mb-3', style={'width': '100%'}),
                    
#                     html.Button('Submit Contact', id='submit-button', n_clicks=0, className='btn btn-primary mt-3'),
#                     html.Div(id='data-entry-status', className='mt-3')
#                 ])
#             ], style={'width': '500px', 'margin': 'auto'})
#         ])
#     ])
# ], fluid=True)

# # Callback to handle contact submission
# @callback(
#     Output('data-entry-status', 'children'),
#     Input('submit-button', 'n_clicks'),
#     [
#         State('name-input', 'value'),
#         State('gender-input', 'value'),
#         State('designation-input', 'value'),
#         State('organisation-input', 'value'),
#         State('department-input', 'value'),
#         State('group-input', 'value'),
#         State('email-input', 'value'),
#         State('cellno-input', 'value'),
#         State('homephone-input', 'value'),
#         State('landline-input', 'value'),
#         State('cnic-input', 'value'),
#         State('address-input', 'value'),
#         State('unioncouncil-input', 'value'),
#         State('district-input', 'value'),
#         State('tehsil-input', 'value')
#     ],
#     prevent_initial_call=True
# )
# def submit_contact(n_clicks, name, gender, designation, organisation, department, group, email, cellno, homephone, landline, cnic, address, unioncouncil, district, tehsil):
#     if not n_clicks:
#         return ""
    
#     # Validate required fields
#     if not name or not gender:
#         logger.warning("Attempted to submit contact with missing name or gender")
#         return dbc.Alert("Name and Gender are required!", color="danger")
    
#     # Prepare contact data (S.No is auto-increment, so not included)
#     contact_data = {
#         'Name': name,
#         'Gender': gender,
#         'Designation': designation,
#         'Organisation': organisation,
#         'Department': department,
#         'Group': group,
#         'Email': email,
#         'Cell No': cellno,
#         'Home phone No': homephone,
#         'Landline / Fax': landline,
#         'CNIC': cnic,
#         'Postal Address': address,
#         'Union Council': unioncouncil,
#         'District': district,
#         'Tehsil': tehsil
#     }
    
#     logger.info(f"Attempting to add contact: {name}")
#     try:
#         with engine.connect() as conn:
#             conn.execute(
#                 insert(rsucontacts_table),
#                 contact_data
#             )
#             conn.commit()
#         logger.info(f"Contact added successfully: {name}")
#         return dbc.Alert("Contact saved successfully!", color="success")
#     except Exception as e:
#         logger.error(f"Failed to add contact: {str(e)}")
#         return dbc.Alert(f"Error saving contact: {str(e)}", color="danger")

# if __name__ == '__main__':
#     app.run_server(debug=True)

import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
from sqlalchemy import create_engine, MetaData, Table, insert
import logging
import os

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

# MySQL Database URI
DATABASE_URI = "mysql+pymysql://root:@localhost/phonebook"

# Initialize SQLAlchemy engine and table
engine = create_engine(DATABASE_URI)
metadata = MetaData()
rsucontacts_table = Table('rsucontacts', metadata, autoload_with=engine)

# Function to insert contact data
def add_contact_to_db(contact_data):
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

# Initialize the Dash app with a secret key
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.server.secret_key = os.urandom(24).hex()

# Form layout with Bootstrap styling
app.layout = dbc.Container([
    html.H1("Add Contact to RSU Directory", className="text-center mt-4 mb-4", style={'color': '#007bff'}),
    
    dbc.Row(
        dbc.Col(
            dbc.Card(
                [
                    dbc.CardHeader("Contact Information", className="bg-primary text-white"),
                    dbc.CardBody([
                        # Form fields in a two-column grid
                        dbc.Row([
                            # Left column
                            dbc.Col([
                                dbc.Label("Name *", className="fw-bold"),
                                dcc.Input(id='name-input', type='text', placeholder='Enter Name', className='form-control mb-3'),
                                
                                dbc.Label("Gender *", className="fw-bold"),
                                dcc.Dropdown(
                                    id='gender-input',
                                    options=[
                                        {'label': 'Male', 'value': 'Male'},
                                        {'label': 'Female', 'value': 'Female'}
                                    ],
                                    placeholder='Select Gender',
                                    className='form-select mb-3'
                                ),
                                
                                dbc.Label("Designation", className="fw-bold"),
                                dcc.Input(id='designation-input', type='text', placeholder='Enter Designation', className='form-control mb-3'),
                                
                                dbc.Label("Organisation", className="fw-bold"),
                                dcc.Input(id='organisation-input', type='text', placeholder='Enter Organisation', className='form-control mb-3'),
                                
                                dbc.Label("Department", className="fw-bold"),
                                dcc.Input(id='department-input', type='text', placeholder='Enter Department', className='form-control mb-3'),
                                
                                dbc.Label("Group", className="fw-bold"),
                                dcc.Input(id='group-input', type='text', placeholder='Enter Group', className='form-control mb-3'),
                                
                                dbc.Label("Email", className="fw-bold"),
                                dcc.Input(id='email-input', type='email', placeholder='Enter Email', className='form-control mb-3'),
                            ], width=6),
                            
                            # Right column
                            dbc.Col([
                                dbc.Label("Cell No", className="fw-bold"),
                                dcc.Input(id='cellno-input', type='text', placeholder='Enter Cell No', className='form-control mb-3'),
                                
                                dbc.Label("Home Phone No", className="fw-bold"),
                                dcc.Input(id='homephone-input', type='text', placeholder='Enter Home Phone No', className='form-control mb-3'),
                                
                                dbc.Label("Landline / Fax", className="fw-bold"),
                                dcc.Input(id='landline-input', type='text', placeholder='Enter Landline/Fax', className='form-control mb-3'),
                                
                                dbc.Label("CNIC", className="fw-bold"),
                                dcc.Input(id='cnic-input', type='text', placeholder='Enter CNIC', className='form-control mb-3'),
                                
                                dbc.Label("Postal Address", className="fw-bold"),
                                dcc.Input(id='address-input', type='text', placeholder='Enter Postal Address', className='form-control mb-3'),
                                
                                dbc.Label("Union Council", className="fw-bold"),
                                dcc.Input(id='unioncouncil-input', type='text', placeholder='Enter Union Council', className='form-control mb-3'),
                                
                                dbc.Label("District", className="fw-bold"),
                                dcc.Input(id='district-input', type='text', placeholder='Enter District', className='form-control mb-3'),
                                
                                dbc.Label("Tehsil", className="fw-bold"),
                                dcc.Input(id='tehsil-input', type='text', placeholder='Enter Tehsil', className='form-control mb-3'),
                            ], width=6)
                        ]),
                        
                        # Submit button and status
                        html.Button('Submit Contact', id='submit-button', n_clicks=0, className='btn btn-primary btn-lg mt-3'),
                        html.Div(id='data-entry-status', className='mt-3'),
                        html.P("* Required fields", className="text-muted mt-2")
                    ])
                ],
                style={'maxWidth': '900px', 'margin': 'auto'}
            )
        )
    )
], fluid=True)

# Callback to handle contact submission
@callback(
    Output('data-entry-status', 'children'),
    Input('submit-button', 'n_clicks'),
    [
        State('name-input', 'value'),
        State('gender-input', 'value'),
        State('designation-input', 'value'),
        State('organisation-input', 'value'),
        State('department-input', 'value'),
        State('group-input', 'value'),
        State('email-input', 'value'),
        State('cellno-input', 'value'),
        State('homephone-input', 'value'),
        State('landline-input', 'value'),
        State('cnic-input', 'value'),
        State('address-input', 'value'),
        State('unioncouncil-input', 'value'),
        State('district-input', 'value'),
        State('tehsil-input', 'value')
    ],
    prevent_initial_call=True
)
def submit_contact(n_clicks, name, gender, designation, organisation, department, group, email, cellno, homephone, landline, cnic, address, unioncouncil, district, tehsil):
    if not n_clicks:
        return ""
    
    contact_data = {
        'Name': name,
        'Gender': gender,
        'Designation': designation,
        'Organisation': organisation,
        'Department': department,
        'Group': group,
        'Email': email,
        'Cell No': cellno,
        'Home phone No': homephone,
        'Landline / Fax': landline,
        'CNIC': cnic,
        'Postal Address': address,
        'Union Council': unioncouncil,
        'District': district,
        'Tehsil': tehsil
    }
    
    logger.info(f"Attempting to add contact: {name}")
    success = add_contact_to_db(contact_data)
    
    if success:
        return dbc.Alert("Contact saved successfully!", color="success", dismissable=True)
    return dbc.Alert(f"Error saving contact: Check required fields or database connection", color="danger", dismissable=True)

if __name__ == '__main__':
    app.run_server(debug=True)