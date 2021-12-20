# data manipulation
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import cluster
# plotly 
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
# dashboards
import dash 
from jupyter_dash import JupyterDash
from dash import dcc
from dash import html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import dash_table

# app=JupyterDash(__name__,external_stylesheets=[dbc.themes.MINTY])
app=dash.Dash(__name__,external_stylesheets=[dbc.themes.MINTY])

#Overall Data
cleandata=pd.read_csv("cleaned_data.csv")
cleandata['year'] = pd.DatetimeIndex(cleandata['timestamp']).year
ed_count = cleandata["Education"].value_counts()
ed_count_percent = cleandata["Education"].value_counts(normalize =True)

gen_cleandata = cleandata[cleandata['gender'].isin(['Female','Male'])].groupby(['Education','gender'],as_index=False)[['Education','gender','totalyearlycompensation']].mean()

exp_cleandata =  cleandata[['Education','Exp_Level','totalyearlycompensation']]

colors_list = ['rgba(167, 199, 231, 0.5)', 'rgba(96, 130, 182, 0.5)']

yearcompensation = cleandata.groupby(['year','Education'],as_index=False)[['totalyearlycompensation']].mean()

cleandata['state'] = cleandata['location'].str.split(', ', expand=True)[1]
cleandata.head()
cleandata['state'].unique()
cleandata_us=cleandata[cleandata['state'].isin([ 'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
          'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
          'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
          'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
          'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY'])]
cleandata_us['state'].unique()

cleandata1 = cleandata.loc[:,cleandata.columns.intersection(['company', 'title', 'totalyearlycompensation','state','yearsofexperience','yearsatcompany','Education', 'Exp_level'])]

cleandata2 = cleandata1.groupby(['state']).mean().sort_values(by = 'totalyearlycompensation', ascending = False).reset_index()[:10].round(2)

#cluster analysis
#------------- NORMALIZE THE VARIABLES --------------------#
cleandata_cluster = cleandata.loc[:, cleandata.columns.intersection(['yearsofexperience','basesalary','totalyearlycompensation','yearsatcompany','stockgrantvalue','bonus'])]
col_names=cleandata_cluster.columns
z_cols = ['z_'+col for col in col_names]
for col in range(len(z_cols)):
    cleandata_cluster[z_cols[col]]= (cleandata_cluster[col_names[col]]-cleandata_cluster[col_names[col]].mean())/cleandata_cluster[col_names[col]].std()

#------------- CREATE ELBOW PLOT --------------------#
ss=[]
for k in range(2,15):
    model=cluster.KMeans(n_clusters=k , random_state=10)
    model.fit(cleandata_cluster[['z_totalyearlycompensation','z_yearsofexperience','z_yearsatcompany','z_basesalary']])
    ss.append(model.inertia_)
cleandata_elbow=pd.DataFrame({'K':range(2,15),'SS':ss})

#------------- PERFORM CLUSTERING --------------------#
model=cluster.KMeans(n_clusters=4,random_state=9)
model.fit(cleandata_cluster[['z_totalyearlycompensation','z_yearsofexperience']])
cleandata_cluster['cluster']=model.labels_
l=min(cleandata_cluster['totalyearlycompensation'])

#------------- CREATE GRAPHS --------------------#
cleandata_cluster["cluster"] = cleandata_cluster["cluster"].astype(str)
fig_cluster=px.scatter(data_frame=cleandata_cluster,x='yearsofexperience',y='totalyearlycompensation',color='cluster',\
            #color_discrete_sequence=['#5975a5','#cc8964','#5f9e6e','#b65d61']
                    title='Cluster visualization')
fig_countplot =px.histogram(cleandata_cluster,x='cluster',color='cluster',title='Distribution of clusters')
fig_elbow=px.line(cleandata_elbow, x="K", y=ss,title='Elbow plot',labels={'y':'Distortion score'})
fig_elbow.add_vline(x=4,line_dash='dash')


#map data
averages=pd.read_csv('us_average_salaries.csv')
averages = averages[averages['Education'].isin(["Bachelor's Degree", "Master's Degree", 'PhD','Some College'])]

#distribution viz
hist_data = [cleandata['yearsofexperience']]
group_labels = ['Years of experience']
exp_yr = ff.create_distplot(hist_data, group_labels)
exp_yr.update_layout(title='Dist Plot for years of experience(Most people have 2-6 years of experience)')
exp_yr.update_xaxes(title='Years of Experience')
exp_yr.update_yaxes(title='Probability')

#barchart visualization
fig_bar=px.bar(x=ed_count.index,y=ed_count,title='Number of Degree Holders by Degree Type')
fig_bar.update_xaxes(title='Degree Type')
fig_bar.update_yaxes(title='Count of Degree Holders')

#boxplot visualization
# fig_box=go.Figure()
# fig_box=px.box(cleandata, x='Education', y='totalyearlycompensation',title='Distribution of Yearly Compensation by Degree Type')
# fig_box.update_layout(hovermode='closest')
# fig_box.update_xaxes(title='Degree Type')
# fig_box.update_yaxes(title='Total Yearly Compensation')

#Linechart
# fig_line = px.line(yearcompensation, x="year", y="totalyearlycompensation", color='Education')
# fig_line.update_layout(
#     xaxis = dict(
#         tickmode = 'linear',
#         tick0 = yearcompensation['year'].min,
#         dtick = 1
#     )
# )

#multivariate boxplot
#fig_box_multi=px.box(cleandata, x='Education', y='totalyearlycompensation', color = "Exp_Level",title='Distribution of Yearly Compensation by Degree Type and Experience Level')

app.layout = html.Div([
    html.Br(),
    html.H1("Does a Master's degree lead to higher salaries in the USA?", style={'color': 'black', 'fontSize': '40px', 'text-align':'center'}),
    html.Br(),
    dcc.Tabs( [
              
        #TAB1
        dcc.Tab(label='Salary Distribution', 
        children=[

            html.Br(),
            
            #Filter DropDown
            html.Div([dcc.Dropdown(
                id='map_buttons',
                options=[{'label':i,'value':i} for i in averages['Education'].unique()],
                value = "Bachelor's Degree")
                ]),
            
            html.Br(),

            #3 BOXES
            html.Div([
                dbc.Row([
    dbc.Col(
        dbc.Card(
            [

                dbc.CardBody(
                    [
                        html.H5(id='card_title_1', children=['Average Total Yearly Compensation'], className='card-title',
                                ),
                        html.P(id='card_text_1', children=['Sample text.'],style={'fontSize': '25px', 'color':'darkblue'}),
                    ]
                )
            ]
        ),
        #md=4
    ),
    dbc.Col(
        dbc.Card(
            [

                dbc.CardBody(
                    [
                        html.H5('Maximum Total Yearly Compensation', className='card-title',),
                        html.P(id='card_text_2',children=['Sample text.'],style={'fontSize': '25px', 'color':'darkblue'}),
                    ]
                ),
            ]

        ),
        #md=4
    ),
    dbc.Col(
        dbc.Card(
            [
                dbc.CardBody(
                    [
                        html.H5('Most Popular Job Title', className='card-title',),
                        html.P(id='card_text_3',children=['Sample text.'],style={'fontSize': '25px', 'color':'darkblue'}),
                    ]
                ),
            ]

        ),
        #md=4
    ),
    
])
                
                    ]),

            html.Br(),

            #Title of map
            html.H3('Average Salaries by State'),
            #Map
            html.Div([
            dcc.Graph(
                id='map_graph'),], style ={'height':'400px'}),


            html.Br(),
            html.Br(),

            #BAR AND BOX PLOTS
            html.Div([
                #Box plot for Experience Level
                html.Div([dcc.Graph(
                id='gender plot')], style={'width':'49%',
                        'display':'inline-block'}),

                #Bar plot for Gender
                html.Div([dcc.Graph(
                id='exp plot')], style={'width':'48%',
                        'display':'inline-block'})
                        
                        
                        ])

            ]),

        #TAB2      
        dcc.Tab(label='Exploratory Data Analysis', children=[
                # dcc.Graph(
                #         figure = fig_line
                # ),
                dcc.Graph(
                        figure=fig_bar
                        ),
                # dcc.Graph(
                #         figure=fig_box
                #         ), 
                # dcc.Graph(
                #         figure=fig_box_multi
                #         ),
                dcc.Graph(
                        figure=exp_yr
                        )
                    ],
               ),

        #TAB 3
        dcc.Tab(label='Clustering', children =[
                html.Br(),
                html.H5('There is an elbow formation at 4 clusters(sum of squares falls steepest here)',style = {'margin-left':'60px'}),
                dcc.Graph(figure=fig_elbow),
                html.H5('Plotting the 4 clusters based on total compensation and years of experience',style = {'margin-left':'60px'}),
                dcc.Graph(figure=fig_cluster),
                html.H5('Cluster 0 - Low years of Experience,Low Total Yearly Compensation',style = {'color': 'steelblue','margin-left':'60px'}),
                html.H5('Cluster 1 - High years of Experience,Low Total Yearly Compensation',style = {'color': 'steelblue','margin-left':'60px'}),
                html.H5('Cluster 2 - High Total Yearly Compensation',style = {'color': 'steelblue','margin-left':'60px'}),
                html.H5('Cluster 3 - Low years of Experience,Median Total Yearly Compensation',style = {'color': 'steelblue','margin-left':'60px'}),
                html.Br(),
                html.H5('Most employees are in cluster 0, having entry-intermediate level experience and salary going up to $300k',style = {'margin-left':'60px'}),
                html.Br(),
                html.H5('Employees in cluster 4 have highest salaries($400k+) and usually more than 5 years of experience ',style = {'margin-left':'60px'}),
                dcc.Graph(figure=fig_countplot)

        ],        
        
                ),

        
        dcc.Tab(label = 'Tables', children=[
                  html.Br(),
                  html.H5('Top 10 US States by Total Yearly Compensation',style = {'text-align':'center'}),
                  html.Br(),
                  dash_table.DataTable(
                   id='table',
                   columns=[{"name": i, "id": i} for i in cleandata2.columns],
                   data=cleandata2.to_dict('records'),
                 ),
               ]
               )
        
    ])
])
#Map tab1
@app.callback(Output('map_graph', 'figure'),
              Input('map_buttons', 'value'))
def update_graph(level):
    subset = averages[averages['Education'] == level]
    fig = go.Figure(data=go.Choropleth(
        locations=subset['state'], # Spatial coordinates
        z = subset['totalyearlycompensation'].astype(float), # Data to be color-coded
        locationmode = 'USA-states', # set of locations match entries in `locations`
        colorscale = 'Blues',
        ))
    fig.update_layout(geo_scope='usa')
    return fig

#Gender tab1
@app.callback(Output('gender plot', 'figure'),
              Input('map_buttons', 'value'))
def update_graph(level):
    gen_ed = gen_cleandata[gen_cleandata['Education'] == level]
    fig = px.bar(gen_ed, x="gender", y="totalyearlycompensation", color = 'gender',
                  color_discrete_sequence = ["skyblue","steelblue"],barmode="group")
    fig.update_layout(title="Average Total Yearly Compensation by Gender",
    xaxis_title="Gender",
    yaxis_title="Total Yearly Compensation",
    legend_title="Gender")
    #fig.update_traces(marker_color = 'steelblue')   
               
    return fig 

#Exp level tab1
@app.callback(Output('exp plot', 'figure'),
              Input('map_buttons', 'value'))
def update_graph(level):
    exp_ed = exp_cleandata[exp_cleandata['Education'] == level]
    fig = px.box(exp_ed, x="Exp_Level", y="totalyearlycompensation", color = 'Exp_Level',
                  color_discrete_sequence = ["lightskyblue","skyblue","steelblue"])
    fig.update_layout(title="Total Yearly Compensation by Experience Level",
    xaxis_title="Experience Level",
    yaxis_title="Total Yearly Compensation",
    legend_title="Experience Level")
    #fig.update_traces(marker_color = 'steelblue')   
               
    return fig

#Card1
@app.callback(Output('card_text_1', 'children'),
              Input('map_buttons', 'value'))
def update_card_text_1(level):
    exp_ed = exp_cleandata[exp_cleandata['Education'] == level]
    mean_ed_sal = round(exp_ed['totalyearlycompensation'].mean())
    #txt_content = print(f'${mean_ed_sal}')

    return mean_ed_sal

#Card2
@app.callback(Output('card_text_2', 'children'),
              Input('map_buttons', 'value'))
def update_card_text_2(level):
    exp_ed = exp_cleandata[exp_cleandata['Education'] == level]
    max_ed_sal = round(exp_ed['totalyearlycompensation'].max())
    #txt_content = print(f'${mean_ed_sal}')

    return max_ed_sal

#Card3
@app.callback(Output('card_text_3', 'children'),
              Input('map_buttons', 'value'))
def update_card_text_2(level):
    exp_ed = cleandata[cleandata['Education'] == level]
    #min_ed_sal = round(exp_ed['totalyearlycompensation'].min())
    titles = exp_ed['title'].value_counts()
    job_title = titles.idxmax()
    #txt_content = print(f'${mean_ed_sal}')
    #us_avg = averages[averages['Education']==level]
    #mean_us = us_avg['totalyearlycompensation'].mean()

    return job_title

# if __name__ == '__main__':
#     app.run_server(mode='external', height= 500, width = '100%',port=8053)

if __name__ == '__main__':
    app.run_server(debug=True)