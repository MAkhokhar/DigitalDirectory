import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State

from flask import request
import dash_auth
from assets.login import get_valid_credentials  
from assets.logingtime import logtime, logger
import os
from datetime import datetime

VALID_USERNAME_PASSWORD_PAIRS = get_valid_credentials()
# {"admin": "rwp123","LSU": "lsu2023",   "RSU": "rsu2023", "RSU": "rsu2023"}
dbc_css = "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates/dbc.min.css"

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SPACELAB, dbc_css],meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5, user-scalable=no'}])

auth = dash_auth.BasicAuth(app, VALID_USERNAME_PASSWORD_PAIRS)
app.server.secret_key = os.urandom(24).hex()
server = app.server
pages = [
    {"name": "📠 PhoneBook Dashboard", "path": "/"},
    
     {"name": "📞 RSU-PhoneBook", "path": "/contact-info"},
     {"name": "📱 LSU-PhoneBook", "path":"/lsu-contct-info"},
    {"name": " 📥 LSU Data Entry Form", "path":"/lsu-data-entry"},
     {"name": "📥 LSU Data Entry Update", "path":"/update-info"},
    # {"name": "PhoneBook DashBoard", "path":"/statitical-info"},
    {"name": "📊 WCD Event Status", "path":"/wcdevent"},
    {"name": "📊 List of Master Trainers", "path":"/mt-list"},
]
lsupages = [
    {"name": "📠 PhoneBook DashBoard", "path":"/"},
    {"name": "📞LSU-PhoneBook", "path":"/lsu-contct-info"},
    {"name": "📱 LSU Data Entry Form", "path":"/lsu-data-entry"},
    {"name": "📞LSU Data Entry Update", "path":"/update-info"},
    # {"name": "OOSC Event Status", "path":"/statitical-info"},
    # {"name": "WCD Event Status", "path":"/wcdevent"},
]
GuestPages=[ {"name": "📠 PhoneBook DashBoard", "path":"/"},
    {"name": "📞RSU-PhoneBook", "path":"/contact-info"},
    {"name": "📱LSU-PhoneBook", "path":"/lsu-contct-info"},
     {"name": "📊 WCD Event Status", "path":"/wcdevent"},]

img = html.Img(src="assets\images\logo.jpg", height="80px")
Guestsidebar=dbc.Nav(
    [
        dbc.NavLink(
            [
                html.Div(page["name"], className="ms-2"),
            ],
            href=page["path"],
            active="exact",
        )
        for page in GuestPages
    ],
    vertical=True,
    pills=True,
    className="bg-light",
)

lsusidebar = dbc.Nav(
    [
        dbc.NavLink(
            [
                html.Div(page["name"], className="ms-2"),
            ],
            href=page["path"],
            active="exact",
        )
        for page in lsupages
    ],
    vertical=True,
    pills=True,
    className="bg-light",
)
sidebar = dbc.Nav(
    [
        dbc.NavLink(
            [
                html.Div(page["name"], className="ms-2"),
            ],
            href=page["path"],
            active="exact",
        )
        for page in pages
    ],
    vertical=True,
    pills=True,
    className="bg-light",
)

app.layout = dbc.Container(
    [
        dbc.Row(
            [
                dcc.Store(id="store", data={}),
                dbc.Col(html.Div(img), width=1),
                dbc.Col(
                    html.Div(
                        " ☎️ Reform Support Unit-Digital Directory: ",
                    ),
                    style={"padding": "0.1rem", "fontSize": 50, "textAlign": "center"},
                    width=11,
                ),
            ]
        ),
        html.Br(),
        html.Hr(),
        html.Br(),
        dbc.Row(
            [
                dbc.Col(
                    [
                        # sidebar,
                        dcc.Location(id="url", refresh=False),
                        html.Div(id="pages"),
                    ],
                    xs=2,
                    sm=2,
                    md=2,
                    lg=2,
                    xl=2,
                    xxl=2,
                ),
                dbc.Col(
                    [

                        #html.Div(id="page-content"),
                        dash.page_container,
                    ],
                    xs=10,
                    sm=10,
                    md=10,
                    lg=10,
                    xl=10,
                    xxl=10,
                ),
            ]
        ),
    ],
    fluid=True,
)

# # Callback to determine which pages are accessible based on the logged-in user
# @logtime
# @app.callback(
#     Output("pages", "children"),
#     [Input("url", "pathname")],
#     prevent_initial_call=True,
# )
# def display_page(pathname):
   
#     password =request.authorization['password']
#     user=request.authorization['username']
#     print(user)
#     if auth.is_authorized() and password=='admin123'  :
      
        
#         logger.info(f"User {user['username']} logged in at {user['login_time']}")
       
#         accessible_pages = pages
#         return sidebar
    
#     elif auth.is_authorized() and password=='lsu2023':
#         accessible_pages = [page for page in lsupages if page["name"] =="LSU Data Entry Form"]
#         return lsusidebar


#     elif auth.is_authorized() and password=='rsu2023':
#         accessible_pages = GuestPages
#         return Guestsidebar

#     else:
#         accessible_pages = []
#     return sidebar

# Callback to determine which pages are accessible based on the logged-in user
@logtime
@app.callback(
    Output("pages", "children"),
    [Input("url", "pathname")],
    prevent_initial_call=True,
)
def display_page(pathname):
    # Check if authorization is provided
    if not request.authorization:
        logger.warning("No authorization provided.")
        return "Unauthorized", 401

    username = request.authorization['username']
    password = request.authorization['password']
    login_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    logger.info(f"User {username} logged in at {login_time}")

    if auth.is_authorized() and password == 'admin123':
        accessible_pages = pages
        return sidebar

    elif auth.is_authorized() and password == 'lsu2023':
        accessible_pages = [page for page in lsupages if page["name"] == "LSU Data Entry Form"]
        return lsusidebar

    elif auth.is_authorized() and password == 'rsu2023' or password == 'alikhokhar':
        accessible_pages = GuestPages
        return Guestsidebar

    else:
        logger.warning(f"Unauthorized access attempt by {username}.")
        return "Unauthorized", 401

# Define callback to update page content
# @app.callback(
#     Output("page-content", "children"),
#     [Input("url", "pathname")],
# )
# def display_page_content(pathname):
#     # You can customize this function to load the content of each page dynamically

#     return html.Div(f"Content for {pathname}")


if __name__ == "__main__":
    app.run_server(debug=True)
