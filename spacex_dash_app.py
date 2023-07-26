# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

suclist =[]
clslist = spacex_df['class'].tolist()

for i,clas in enumerate(clslist):
    if clas == 0:
        suclist.append('Failure')
    else:
        suclist.append('Success')

spacex_df['Mission Outcome']=suclist

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                options=[{'label': 'All Sites', 'value': 'ALL'},
                                         {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                         {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                         {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                         {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}],
                                value='ALL',
                                placeholder="Select a Launch Site Here",
                                searchable=True),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                min=0, max=10000, step=1000,
                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
               [Input(component_id='site-dropdown', component_property='value')])

def get_pie_chart(entered_site):
    
    if entered_site == 'ALL':
        allsuc_df = spacex_df.groupby('Launch Site')[['class']].sum().rename(columns={"class":'Success Count'}).reset_index()
        fig = px.pie(allsuc_df, values='Success Count', 
        names='Launch Site', 
        title='Total Successful Missions by Launch Site')
        return fig
    else:
        site_df = spacex_df.loc[spacex_df['Launch Site']==entered_site]
        sitesuc_df = site_df.groupby('class')[['class']].count().rename(columns={"class":'Count'}).reset_index()
        sitesuc_df['Outcomes'] = ['Failure', 'Success']
        fig = px.pie(sitesuc_df, values='Count', 
        names='Outcomes', 
        title='Mission Outcome for Launch Site '+ entered_site)
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
               [Input(component_id='site-dropdown', component_property='value'),
               Input(component_id='payload-slider', component_property='value')])

def get_scatter_chart(entered_site, payload_range):
    
    if entered_site == 'ALL':
        fig = px.scatter(spacex_df, x='Payload Mass (kg)',
        y='Mission Outcome', 
        title='Mission Success vs Payload Mass for all Launch Sites',
        color='Booster Version Category',
        range_x=payload_range)
        return fig
    else:
        site_df2 = spacex_df.loc[spacex_df['Launch Site']==entered_site]
        fig = px.scatter(site_df2, x='Payload Mass (kg)',
        y='Mission Outcome', 
        title='Mission Success vs Payload Mass for Launch Site ' + entered_site,
        color='Booster Version Category',
        range_x=payload_range)
        return fig



# Run the app
if __name__ == '__main__':
    app.run_server()
