import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output, callback,dash_table
import plotly.express as px
import pandas as pd

df = pd.read_csv('data/WCD participants list confirmation.csv')
Types = df.Type.unique()
confimby=df.ConfirmedBy.unique()
#emails=df.groupby('Type')[['Email Address']].count().reset_index()
wcdstatus=df.groupby('Type')[['Email Address','Status']].count().reset_index()
wcdstatus2 = df.Status.value_counts().reset_index()
dash.register_page(__name__ , name='WCD Event Status', external_stylesheets=[dbc.themes.SPACELAB])
layout = html.Div(
    [
        html.H4("WCD-World Childrens' Day Event on 20th Nov 2023 Status : 20-Nov-2023"),
        dash_table.DataTable(id='datatable-output2',data=wcdstatus.to_dict('records'),
                                columns=[{'id': c, 'name': c} for c in wcdstatus.columns],
                                page_action='native',   # all data is passed to the table up-front
                                page_size=10,           # only 10 rows are displayed at a time

                                style_table={'height': '200px', 'overflowY': 'auto'},
                                style_cell={'color':'dark', 'text-align':'left','width':'10px'},

                                ),
         html.H4("WCD-World Childrens' Day Event: Participnt's Summary "),
        dash_table.DataTable(id='status-output2',data=wcdstatus2.to_dict('records'),
                                columns=[{'id': d, 'name': d} for d in wcdstatus2.columns],
                                page_action='native',   # all data is passed to the table up-front
                                page_size=10,           # only 10 rows are displayed at a time

                                style_table={'height': '200px', 'overflowY': 'auto'},
                                style_cell={'color':'dark', 'text-align':'left','width':'10px'},

                                ),



        # dcc.Dropdown(
        #     id="wcddropdown",
        #     options=[{"label": x, "value": x} for x in Types],
        #     value=Types[0],
        #     clearable=False,
        #     disabled=False,
        #     style={"width": "50%"}

        # ),
        # dcc.Graph(id="wcdbar-chart"),
    ]
)


# @callback(
#         #    Output('datatable-output2', 'data'),
#         #    Output('datatable-output2', 'columns'),
#             Output("wcdbar-chart", "figure"),
#            Input("wcddropdown", "value"),
#            allow_duplicate=True,
#            prevent_initial_call=True,

#            )

# def update_bar_chart(tt):
#     # print(tt)
#     mask = df["Type"] == tt
#     # print(wcdstatus[mask])
#     # #m2=mask[mask]
#     fig = px.bar(wcdstatus, x='Type', y=['Email Address','Status'],barmode="group")
#     return fig
