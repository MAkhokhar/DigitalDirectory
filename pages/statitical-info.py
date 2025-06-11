import dash
import dash_bootstrap_components as dbc
# Code from: https://github.com/plotly/dash-labs/tree/main/docs/demos/multi_page_example1
#dash.register_page(__name__)
from dash import Dash, dcc, html, Input, Output, callback,dash_table
import plotly.express as px
import pandas as pd
from data.database import fetch_lsucontacts, fetch_contacts

# df = pd.read_csv('data/OOSC Conference participants.csv')
# Types = df.Type.unique()
# df = pd.read_csv('data/rsucontacts.csv')html.P(f"Welcome, {logged_in_user['username']}! Logged in at: {logged_in_user['login_time']}"),
df=fetch_contacts()
totalentries=df['S.No'].count()
Types = df.Organisation.unique()
confimby=df.ConfirmedBy.unique()
emails=df.groupby('Organisation')[['Email']].count().reset_index()
current=df.groupby('Organisation')[['Email','Cell No']].count().sort_values(by='Email',ascending=False).reset_index()
dept=df.groupby('Organisation')['Department'].count().sort_values(ascending=False).reset_index()
#wcdstatus2 = df.Status.value_counts().reset_index()
# wcdstatus2=df.groupby('ConfirmedBy')['Status'].value_counts().unstack().reset_index()

# LSU contact info:
# df2 = pd.read_csv('data/contacts.csv')
df2=fetch_lsucontacts()
lsuemails=df2.groupby('District')[['Email','Cell No']].count().sort_values(by='Cell No',ascending=False).reset_index()
# lsudistricts=df2['District'].value_counts().reset_index()
lsuentries=df2['First Name'].count()
lsuemails
# lsudistricts
lsumissing=df2.count().reset_index()


fig2=px.bar(dept, x='Department', y='Organisation' , orientation='h', barmode="group")
# lsufig=px.bar(lsudistricts, x='District', y='count', barmode="group")
dash.register_page(__name__, path="/",name='PhoneBook DashBoard', external_stylesheets=[dbc.themes.SPACELAB],meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5, user-scalable=no'}])
layout = html.Div([

                dbc.Container(
                    [

                        dbc.Row(
                            [
                                dbc.Col(


                        [
                            # html.H4("RSU Digital Directory Dashboard Info:"),
                            html.H4(f"RSU Digital Directory Dashboard Info:{ totalentries} Total Entries"),
                            dash_table.DataTable(id='ooscdatatable-output', data=current.to_dict('records'),
                                                    columns=[{'id': c, 'name': c} for c in current.columns],
                                                    page_action='native',   # all data is passed to the table up-front
                                                    #page_size=10,           # only 10 rows are displayed at a time

                                                    fixed_rows={'headers':True},
                                                  style_table={'height': '200px', 'overflowY': 'auto'},
                                                    style_cell={'color':'dark', 'text-align':'left','width':'200px'},

                                                    ),

                                                    # html.Br(),
                                                    # html.Hr(),
                                                    ],width=12),


        dbc.Col(


                        [

                            html.Br(),
                            html.Hr(),
                            # html.P(f"Welcome, {logged_in_user['username']}! Logged in at: {logged_in_user['login_time']}"),
                            html.H4(f"Digital Directory Total Entries by LSUs :{ lsuentries} "),
                            # html.P(f"Missing Entries :{ lsumissing} Total Entries by LSUs"),

                            dash_table.DataTable(id='lsudatatable-output', data=lsuemails.to_dict('records'),

                                                    columns=[{'id': c, 'name': c} for c in lsuemails.columns],
                                                    page_action='native',   # all data is passed to the table up-front
                                                    #page_size=10,           # only 10 rows are displayed at a time

                                                    fixed_rows={'headers':True},
                                                    style_table={'height': '200px', 'overflowY': 'auto'},
                                                    style_cell={'color':'dark', 'text-align':'left','width':'200px'},

                                                    ),





                                                    ],width=12),
                 dbc.Col(



                        [
                            html.Br(),
                            html.Hr(),
                            dcc.Graph(id="SCbar-chart", figure=fig2),



                            html.Br(),
                            html.Hr(),

                                ],width=12),

                #   dbc.Col(



                #         [

                #          html.Br(),
                #             html.Hr(),
                #             dcc.Graph(id="lsubar-chart", figure=lsufig),
                #         ],width=12),

        # dcc.Dropdown(
        #     id="ooscdropdown",
        #     options=[{"label": x, "value": x} for x in Types],
        #     #value=Types[0],
        #     clearable=False,
        #     disabled=False,
        #     style={"width": "50%"}

        # ),

        #dcc.Graph(id="SCbar-chart", figure=fig2),






        ], style={'border': '1px solid #ccc', 'padding': '20px', 'background-color': '#f2f2f2', 'position': 'relative','display':' -ms-flexbox'},
                                           ),
    ]),
])


# @callback(
#         #    Output('ooscdatatable-output', 'data'),
#         #    Output('ooscdatatable-output', 'columns'),
#            Output("SCbar-chart", "figure"),
#            Input("ooscdropdown", "value"),
#            allow_duplicate=True,
#            prevent_initial_call=True,

#            )

# def update_bar_chart(tt):
#     #print(tt)
#     mask = current['Type'] == tt
#    # print(current[mask])
#     fig = px.bar(current[mask], x='Type', y='Status', barmode="group") #, barmode="group"
#     return fig
