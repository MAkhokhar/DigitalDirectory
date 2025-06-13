import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
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

# Load data from MySQL
with engine.connect() as conn:
    df = pd.read_sql_table('rsucontacts', conn)

# Function to insert contact data
def add_contact_to_db(contact_data):
    try:
        if not contact_data.get('Name') or not contact_data.get('Gender'):
            logger.warning("Attempted to insert contact with missing Name or Gender")
            return False
        with engine.connect() as conn:
            conn.execute(insert(rsucontacts_table), contact_data)
            conn.commit()
        logger.info(f"Contact added successfully: {contact_data['Name']}")
        return True
    except Exception as e:
        logger.error(f"Failed to add contact: {str(e)}")
        return False

# Initialize the Dash app with a secret key
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.server.secret_key = os.urandom(24).hex()

# Calculate statistics
total_entries = len(df)
male_count = df['Gender'].value_counts().get('Male', 0)
female_count = df['Gender'].value_counts().get('Female', 0)
rsu_org_count = df['Organisation'].value_counts().get('RSU', 0)

# Create graphs
gender_fig = px.pie(
    df, names='Gender', title='Gender Distribution',
    color_discrete_map={'Male': '#007bff', 'Female': '#ff69b4'},
    hole=0.4
)
org_fig = px.bar(
    df['Organisation'].value_counts().reset_index(),
    x='Organisation', y='count',
    title='Organisation Distribution',
    color='Organisation',
    color_discrete_sequence=px.colors.qualitative.Plotly
)

# Dashboard layout
app.layout = dbc.Container([
    html.H1("RSU Digital Phone Book Dashboard", className="text-center mt-4 mb-4", style={'color': '#007bff'}),
    
    # Stats Cards
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Total Entries", className="card-title"),
                html.H2(f"{total_entries}", className="card-text text-center", style={'color': '#007bff'})
            ])
        ], color="light", outline=True, className="shadow-sm"), width=3),
        
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Male Contacts", className="card-title"),
                html.H2(f"{male_count}", className="card-text text-center", style={'color': '#17a2b8'})
            ])
        ], color="light", outline=True, className="shadow-sm"), width=3),
        
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("Female Contacts", className="card-title"),
                html.H2(f"{female_count}", className="card-text text-center", style={'color': '#28a745'})
            ])
        ], color="light", outline=True, className="shadow-sm"), width=3),
        
        dbc.Col(dbc.Card([
            dbc.CardBody([
                html.H4("RSU Organisation", className="card-title"),
                html.H2(f"{rsu_org_count}", className="card-text text-center", style={'color': '#ffc107'})
            ])
        ], color="light", outline=True, className="shadow-sm"), width=3),
    ], className="mb-4"),
    
    # Graphs
    dbc.Row([
        dbc.Col(dcc.Graph(id='gender-pie', figure=gender_fig), width=6),
        dbc.Col(dcc.Graph(id='org-bar', figure=org_fig), width=6),
    ], className="mb-4"),
    
    # Contact Entry Form
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Add New Contact", className="bg-primary text-white"),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dbc.Label("Name *", className="fw-bold"),
                            dcc.Input(id='name-input', type='text', placeholder='Enter Name', className='form-control mb-3'),
                            dbc.Label("Gender *", className="fw-bold"),
                            dcc.Dropdown(id='gender-input', options=[
                                {'label': 'Male', 'value': 'Male'},
                                {'label': 'Female', 'value': 'Female'}
                            ], placeholder='Select Gender', className='form-select mb-3'),
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
                        dbc.Col([
                            dbc.Label("Cell No", className="fw-bold"),
                            dcc.Input(id='cellno-input', type='text', placeholder='Enter Cell No', className='form-control mb-3'),
                            dbc.Label("Home Phone No", className="fw-bold"),
                            dcc.Input(id='homephone-input', type='text', placeholder='Enter Home Phone No', className='form-control mb-3'),
                            dbc.Label("Landline / Fax", className="fw-bold"),
                            dcc.Input(id='landline-input', type='text', placeholder='Enter Landline/F IMPORTANT: System: / Fax', className='form-control mb-3'),
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
                    html.Button('Submit Contact', id='submit-button', n_clicks=0, className='btn btn-primary btn-lg mt-3'),
                    html.Div(id='data-entry-status', className='mt-3'),
                    html.P("* Required fields", className="text-muted mt-2")
                ])
            ], style={'maxWidth': '900px', 'margin': 'auto'})
        ])
    ])
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
        # Reload data for updated graphs
        with engine.connect() as conn:
            global df
            df = pd.read_sql_table('rsucontacts', conn)
            # Update graph figures
            gender_fig.data[0].values = [df['Gender'].value_counts().get('Male', 0), df['Gender'].value_counts().get('Female', 0)]
            org_fig.data[0].y = df['Organisation'].value_counts().values
        return dbc.Alert("Contact saved successfully!", color="success", dismissable=True)
    return dbc.Alert(f"Error saving contact: Check required fields or database connection", color="danger", dismissable=True)

if __name__ == '__main__':
    # Insert sample data (optional, comment out after initial run)
    sample_data = [
        {'Name': 'John Doe', 'Gender': 'Male', 'Designation': 'Professor', 'Organisation': 'RSU', 'Department': 'CS', 'Group': 'Faculty', 'Email': 'john@rsu.edu', 'Cell No': '123-456-7890', 'Home phone No': '098-765-4321', 'Landline / Fax': '111-222-3333', 'CNIC': '12345-6789012-3', 'Postal Address': '123 Main St', 'Union Council': 'UC-1', 'District': 'District A', 'Tehsil': 'Tehsil B'},
        {'Name': 'Jane Smith', 'Gender': 'Female', 'Designation': 'Lecturer', 'Organisation': 'RSU', 'Department': 'EE', 'Group': 'Faculty', 'Email': 'jane@rsu.edu', 'Cell No': '234-567-8901', 'Home phone No': '987-654-3210', 'Landline / Fax': '222-333-4444', 'CNIC': '98765-4321098-7', 'Postal Address': '456 Oak St', 'Union Council': 'UC-2', 'District': 'District B', 'Tehsil': 'Tehsil C'}
    ]
    with engine.connect() as conn:
        conn.execute(rsucontacts_table.delete())
        conn.execute(rsucontacts_table.insert(), sample_data)
        conn.commit()
    
    app.run_server(debug=True)