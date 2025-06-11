import dash
import pandas as pd
import dash_bootstrap_components as dbc
# Code from: https://github.com/plotly/dash-labs/tree/main/docs/demos/multi_page_example1

from dash import Dash, dcc, html, Input, Output, callback, dash_table
import plotly.express as px
df=pd.read_csv('data/mts.csv')
district = df.District.unique()
mt_count=df['SrNo'].count()
DistrictMT=df.groupby('District')[['ECE','DRR','MHPSS','DL','SMC','MD']].count().reset_index()
DistrictMT_long = pd.melt(DistrictMT, id_vars=['District'], var_name='Training', value_name='Count')
df_long = pd.melt(DistrictMT, id_vars=['District'], var_name='Subject', value_name='Count')
mt_fig = px.bar(df_long, x='District', y='Count', color='Subject',
             barmode='group', # Clustered bar chart
             labels={'Count': 'Count', 'District': 'District'},
             title='Master Trainers by District')
mt_fig.update_layout(xaxis_title='District', yaxis_title='Count')
# MT_Gender=df.groupby('District')['Sex'].value_counts().reset_index()
MT_Gender = df.groupby(['District', 'Sex']).size().reset_index(name='count')
dash.register_page(__name__ , name='List of Master Trainers', external_stylesheets=[dbc.themes.SPACELAB])

layout = html.Div(
    [

        html.H4(f"List of Trained Master Trainers Under Rolling Out-Reform Support Unit:  {mt_count} Total"),
        dcc.Input(id='MT-search-input', type='text', placeholder='Enter search criteria for the Master Trainer'),

        # dash_table.DataTable(id='MT-output',data=df.to_dict('records'),
        #                         columns=[{'id': c, 'name': c} for c in df.columns],
        #                         page_action='native',   # all data is passed to the table up-front
        #                         page_size=10,           # only 10 rows are displayed at a time

        #                         style_table={'height': '200px', 'overflowY': 'auto'},
        #                         style_cell={'color':'dark', 'text-align':'left','width':'10px'},

        #                         ),
        dash_table.DataTable(
        id='MT-output',
        data=df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df.columns],
        page_action='native',   # all data is passed to the table up-front
        page_size=10,
        fixed_rows={'headers': True},       # only 10 rows are displayed at a time

        style_table={'height': '300px', 'overflowY': 'auto', 'border': 'thin lightgrey solid'},
        style_header={
            'backgroundColor': 'rgb(230, 230, 230)',
            'fontWeight': 'bold',
            'border': '1px solid black',
            'textAlign': 'center'
        },
        style_cell={
            'color': 'black',
            'textAlign': 'center',
            'padding': '5px',
            'fontFamily': 'Arial',
            'border': '1px solid lightgrey',
            'minWidth': '150px', 'width': '150px', 'maxWidth': '150px',
            'whiteSpace': 'normal',
            'overflow': 'hidden',
            'textOverflow': 'ellipsis',
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            },
            {
                'if': {'state': 'selected'},
                'backgroundColor': 'rgba(0, 116, 217, 0.3)',
                'border': '1px solid blue'
            }
        ],
        style_as_list_view=True,
    ),
        # dcc.Dropdown(
        #         id='district-dropdown',
        #         options=[{'label': district, 'value': district} for district in DistrictMT['District']],
        #         value=DistrictMT['District'][0],
        #         clearable=False,
        #         style={"width": "50%"}
        # ),



        #  html.Hr(),
        dcc.Graph(id='mt-chart',figure=mt_fig),
        html.Hr(),
         dcc.Dropdown(
                id='district-dropdown',
                options=[{'label': district, 'value': district} for district in DistrictMT['District']],
                value=DistrictMT['District'][0],
                clearable=False,
                style={"width": "50%"}
        ),
        dbc.Row([
        dbc.Col([

             dcc.Graph(id='bar-chart'),
        ], width=6),

        dbc.Col([
             dcc.Graph(id='pie-chart'),
        ],width=5)
    ]),

    ]
)

@callback(Output("bar-chart", "figure"),
          Input("district-dropdown", "value"))
def update_bar_chart(selected_district):
    filtered_df = df[df['District'] == selected_district]
    counts = filtered_df[['ECE','DRR','MHPSS','DL','SMC','MD']].count()
    fig = px.bar(
        x=counts.index,
        y=counts.values,
        labels={'x': 'Metric', 'y': 'Count'},
        title=f"Master Trainings of District :{selected_district} ",
        color=counts.index,  # Color each bar differently
        text=counts.values , # Show values on top of the bars

     )
    fig.update_traces(
        texttemplate='%{text}',
        textposition='outside'
    )
    fig.update_layout(
        xaxis_title='Master Training in Subjects',
        yaxis_title='Counts',
        legend_title='Trainings',
        showlegend=True,
        # legend=dict(
        #     orientation="h",
        #     yanchor="bottom",
        #     y=1.02,
        #     xanchor="left",
        #     x=0.1
        # ),
    )
    return fig

@callback(
    Output('pie-chart', 'figure'),
    [Input('district-dropdown', 'value')]
)
def update_pie_chart(selected_district):

    filtered_df =MT_Gender[MT_Gender['District'] == selected_district]
    # print(filtered_df)
    fig = px.pie(
        filtered_df,
        names='Sex',
        values='count',
        title=f"Master Trainer Gender Distribution : {selected_district}",
        # color_discrete_sequence=px.colors.qualitative.Pastel,  # Use different colors for the slices

        color_discrete_map={'Male': 'lightblue', 'Female': 'pink'}
    )
    fig.update_traces(textinfo='label+percent', insidetextorientation='radial')
    return fig

@callback(
    Output('MT-output', 'data'),
    Output('MT-output', 'selected_rows'),
    [Input('MT-search-input', 'value'),

     ],
    prevent_initial_call=True,
    allow_duplicate=True
)
def update_table(search_input):
    selected_rows = []
    if not search_input:
        return df.to_dict('records'), selected_rows # If search input is empty, display all data
    else:
        # Filter the DataFrame based on the search criteria
        filtered_df = df[df.apply(lambda row: any(search_input.lower() in str(cell).lower() for cell in row), axis=1)]

        return filtered_df.to_dict('records'),selected_rows