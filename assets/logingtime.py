import logging
from functools import wraps
import time
from datetime import datetime



# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s  - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('rsu_dashboard.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('RSU Dashboard')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
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


# Modified database operations with logging
# @logtime
# def add_contact_to_db(contact_data):
#     try:
#         with engine.connect() as conn:
#             conn.execute(text("""
#                 INSERT INTO rsucontacts 
#                 (name, gender, email, cellno, department, position)
#                 VALUES (:name, :gender, :email, :cellno, :department, :position)
#             """), contact_data)
#             conn.commit()
#         logger.info(f"New contact added: {contact_data['name']}")
#         return True
#     except Exception as e:
#         logger.error(f"Failed to add contact: {str(e)}")
#         return False

# Modified login callback with logging
# @logtime
# @app.callback(
#     [Output('page-content', 'children'),
#      Output('url', 'pathname')],
#     [Input('url', 'pathname'),
#      Input('login-button', 'n_clicks')],
#     [State('username', 'value'),
#      State('password', 'value')]
# )
# def auth_flow(pathname, n_clicks, username, password):
#     ctx = dash.callback_context
#     logger.debug(f"Auth flow triggered by: {ctx.triggered[0]['prop_id']}")
    
#     if not ctx.triggered:
#         logger.info("Initial page load")
#         return login_layout, "/login"
    
#     if ctx.triggered[0]['prop_id'] == 'login-button.n_clicks':
#         logger.info(f"Login attempt by: {username}")
#         # ... rest of login logic ...
#         if valid_credentials:
#             logger.info(f"Successful login: {username} ({user_role})")
#         else:
#             logger.warning(f"Failed login attempt: {username}")
    
#     # ... rest of the function ...

# Modified data entry callback with logging
# @logtime
# @app.callback(
#     Output('data-entry-status', 'children'),
#     Input('submit-button', 'n_clicks'),
#     [State('name-input', 'value'),
#      State('gender-input', 'value'),
#      State('email-input', 'value'),
#      State('cellno-input', 'value'),
#      State('dept-input', 'value'),
#      State('position-input', 'value')]
# )
# def submit_contact(n_clicks, name, gender, email, cellno, dept, position):
#     if not n_clicks:
#         logger.debug("Data entry form opened")
#         return ""
    
#     contact_data = {
#         'name': name,
#         'gender': gender,
#         'email': email,
#         'cellno': cellno,
#         'department': dept,
#         'position': position
#     }
    
#     logger.info(f"Attempting to add contact: {contact_data}")
#     success = add_contact_to_db(contact_data)
    
#     if success:
#         logger.info("Contact added successfully")
#         return dbc.Alert("Contact saved successfully!", color="success")
#     else:
#         logger.error("Failed to add contact")
#         return dbc.Alert("Error saving contact!", color="danger")

# # Add this component to your layout to show log status
# log_status = html.Div(
#     id='log-status',
#     style={
#         'position': 'fixed',
#         'bottom': '10px',
#         'right': '10px',
#         'padding': '5px',
#         'background': 'rgba(255,255,255,0.9)',
#         'borderRadius': '5px'
#     }
# )

# # Add this callback for real-time log display
# @app.callback(
#     Output('log-status', 'children'),
#     [Input('url', 'pathname'),
#      Input('interval-component', 'n_intervals')]
# )
# @logtime
# def update_log_display(pathname, n):
#     try:
#         with open('rsu_dashboard.log', 'r') as f:
#             logs = f.readlines()[-5:]  # Show last 5 log entries
#         return [
#             html.P(f"📝 {log.strip()}", style={'margin': '2px'})
#             for log in reversed(logs)
#         ]
#     except Exception as e:
#         return html.P(f"Error reading logs: {str(e)}")