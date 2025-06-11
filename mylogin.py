import dash
from dash import dcc, html, Input, Output, State, callback
import dash_bootstrap_components as dbc
from dash.exceptions import PreventUpdate
from sqlalchemy import create_engine, MetaData, Table, select
import pandas as pd
import logging
from functools import wraps
import time
from datetime import datetime

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

# Timing decorator
def logtime(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        logger.info(f"STARTED {func.__name__}")
        try:
            result = func(*args, **kwargs)
            duration = time.time() - start_time
            logger.info(f"COMPLETED {func.__name__} in {duration:.2f}s")
            return result
        except Exception as e:
            logger.error(f"FAILED {func.__name__} with error: {str(e)}")
            raise
    return wrapper

# MySQL Database URI
DATABASE_URI = "mysql+pymysql://root:@localhost/phonebook"

# Initialize SQLAlchemy engine and table
engine = create_engine(DATABASE_URI)
metadata = MetaData()
users_table = Table('login', metadata, autoload_with=engine)

# Initialize the Dash app with a secret key for session management
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.server.secret_key = 'your_secret_key_here'  # Set a secret key to enable sessions

# Store logged-in user info with login time
logged_in_user = {"username": None, "role": None, "login_time": None}
login_logged = False  # Flag to ensure login is logged only once

# Login Layout
login_layout = html.Div([
    html.H1("Login"),
    dbc.Card([
        dbc.CardBody([
            dcc.Input(id='username', type='text', placeholder='Username', className='mb-3'),
            dcc.Input(id='password', type='password', placeholder='Password', className='mb-3'),
            html.Button('Login', id='login-button', n_clicks=0, className='btn btn-primary'),
            html.Div(id='login-output', className='mt-3')
        ])
    ], style={'width': '300px', 'margin': 'auto'})
], style={'textAlign': 'center', 'paddingTop': '100px'})

# Admin Dashboard Layout
admin_layout = html.Div([
    html.H1("Admin Dashboard"),
    html.P(f"Welcome, {logged_in_user['username']}! Logged in at: {logged_in_user['login_time']}"),
    html.Button("Logout", id="logout-admin", n_clicks=0)
])

# User Dashboard Layout
user_layout = html.Div([
    html.H1("User Dashboard"),
    html.P(f"Welcome, {logged_in_user['username']}! Logged in at: {logged_in_user['login_time']}"),
    html.Button("Logout", id="logout-user", n_clicks=0)
])

# Main App Layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

# Verify login credentials
@logtime
def get_valid_credentials(username, password):
    with engine.connect() as connection:
        query = select(users_table).where(
            (users_table.c.username == username) & 
            (users_table.c.password == password)
        )
        result = connection.execute(query).fetchone()
        if result:
            return {"username": result['username'], "role": result['role']}
    return None

# Login callback
@callback(
    [Output('login-output', 'children'),
     Output('url', 'pathname')],
    Input('login-button', 'n_clicks'),
    [State('username', 'value'),
     State('password', 'value')],
    prevent_initial_call=True
)
def login(n_clicks, username, password):
    global login_logged
    if not username or not password:
        return "Please enter both username and password", "/login"
    
    user_info = get_valid_credentials(username, password)
    if user_info:
        logged_in_user["username"] = user_info["username"]
        logged_in_user["role"] = user_info["role"]
        logged_in_user["login_time"] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Log login info only once per session
        if not login_logged:
            logger.info(f"User {logged_in_user['username']} logged in at {logged_in_user['login_time']}")
            login_logged = True
        
        if user_info["role"] == "admin":
            return "Login successful! Redirecting...", "/admin"
        return "Login successful! Redirecting...", "/user"
    return "Invalid credentials", "/login"

# Page content callback
@callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/admin' and logged_in_user["role"] == "admin":
        return admin_layout
    elif pathname == '/user' and logged_in_user["role"] in ["user", "admin"]:
        return user_layout
    else:
        return login_layout

# Logout callback
@callback(
    Output('url', 'pathname', allow_duplicate=True),
    [Input('logout-admin', 'n_clicks'),
     Input('logout-user', 'n_clicks')],
    prevent_initial_call=True
)
def logout(n_clicks_admin, n_clicks_user):
    global login_logged
    if n_clicks_admin or n_clicks_user:
        logger.info(f"User {logged_in_user['username']} logged out")
        logged_in_user["username"] = None
        logged_in_user["role"] = None
        logged_in_user["login_time"] = None
        login_logged = False  # Reset flag for next login
        return "/login"
    raise PreventUpdate

if __name__ == '__main__':
    # Setup sample data in MySQL (run once or comment out after initial run)
    with engine.connect() as conn:
        conn.execute(users_table.delete())  # Clear existing data (optional)
        conn.execute(users_table.insert(), [
            {"username": "admin", "password": "admin123", "role": "admin"},
            {"username": "user1", "password": "pass123", "role": "user"}
        ])
        conn.commit()
    
    app.run_server(debug=True)