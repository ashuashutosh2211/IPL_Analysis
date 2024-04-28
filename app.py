# Import necessary libraries
from dash import Dash, dcc, html, Input, Output
import dash
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import preprocess_match_data
import match_data_info
from match_data_info import get_most_time_winner, get_all_teams , get_winner , get_stats , get_scores_data , get_top_batsman , get_top_bowlers , get_all_batsman , get_batter_runs
from match_data_plots import plot_match_won_by_toss_decision, plot_team_performance, plot_percentage_matches_won_and_lost_by_teams, best_batsmen , plot_top_5_batsmen, top_bowlers, plot_top_5_bowlers ,plot_stadium_matches_for_team , plot_matches_by_team
from match_data_plots import plot_batter_dismissals , plot_runs_scored_against_bowlers , stadium_wise_runs , plot_season_wise_runs , plot_season_wise_violin_plot, plot_runs_distribution 
import warnings 
import numpy as np
import json 
warnings.filterwarnings("ignore")

match_data = pd.read_csv("IPL_Matches_2008_2022.csv") 
ball_data = pd.read_csv("IPL_Ball_by_Ball_2008_2022.csv")
preprocess_match_data.preprocess(match_data)
match_data = pd.read_csv("cleaned_match_data.csv")
with open('orange_cap_dict.json', 'r') as file:
    orange_cap_data = json.load(file)
with open('purple_cap_dict.json', 'r') as file:
    purple_cap_data = json.load(file)

with open('teams_score_data.json') as file:
    teams_scores_data = json.load(file)

external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets ,  suppress_callback_exceptions=True )

app.layout = html.Div([
    html.H1("IPL Analysis Dashboard", style={'textAlign': 'center'}),
    
    dcc.Tabs(id='tabs', value='tab-home', children=[
        dcc.Tab(label='Home', value='tab-home'),
        dcc.Tab(label='Teams', value='tab-teams'),
        dcc.Tab(label='Batsman', value='tab-batter'), 
    ]),
    
    html.Div([
        html.Label("Select Season"),
        dcc.Dropdown(
            id='year-dropdown',
            options=[
                {'label': str(year), 'value': year} for year in range(2008, 2023)
            ],
        )
    ], style={'width': '20%', 'display': 'inline-block', 'verticalAlign': 'top'}),
    
    html.Div(id='tabs-content') , 
    
    html.Div(id='selected-season'),
    
    dbc.Row([
        dbc.Col(html.Div(id='trophy-winner-info'),width = 3 ),
        
        dbc.Col(html.Div(id='orange-cap-winner-info'),width = 3 ),
        
        dbc.Col(html.Div(id='purple-cap-winner-info'),width = 3 ) , 
        
        dbc.Col(html.Div(id = 'stats-info' ) , width = 3 )
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(id='matches-by-toss-decision-plot'),
            
        ], width=3) , 
        dbc.Col([
            html.Div(id='team-performance-plot'),
        ], width = 5 ),
        dbc.Col([
            html.Div(id='matches-won-by-teams-plot')
        ], width=4)
    ]),


    dbc.Row([
        dbc.Col(html.Div(id='team-trophy-winner-info'),width = 3 ),
        
        dbc.Col(html.Div(id='team-most-runs'),width = 3 ),

        dbc.Col(html.Div(id='team-most-wickets'),width = 3 ) , 
        
        dbc.Col(html.Div(id = 'team-stats-info' ) , width = 3 )
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(id='team-matches-by-toss-decision-plot'),
            
        ], width=3) , 
        dbc.Col([
            html.Div(id='team-matches-won-by-teams-plot')
        ], width=4)
    ]) , 
    html.Div(
        [dcc.Dropdown(id='team-dropdown')],
        style={'display': 'none'}  
    ),
    html.H3(id = "select-team-info") ,
    dbc.Row([
        dbc.Col([
           html.Div(id='toss-decision-plot'),
        ], width=3),
        dbc.Col([
                html.Div(id='top-batsmen-plot'),
                
        ], width=5),  
        dbc.Col([
                html.Div(id='top-bowlers-plot'),
                
        ], width=4),  
    ]),

    dbc.Row([
        dbc.Col([
            html.Div(id='stadium-matches-plot'),
        ], width=6),
        dbc.Col([ 
            html.Div(id = 'plot-matches-by-team'),
        ] , width=6 )
    ]),
    # html.Div(
    #     [dcc.Dropdown(id='batsman-dropdown')],
    #     style={'display': 'none'}  
    # ),
    html.Div([dcc.Dropdown(id='batsman-dropdown')], style={'display': 'none'}),

    dbc.Row([
        dbc.Col(html.Div(id='batter-runs'),width = 2 ),
        
        dbc.Col(html.Div(id='batter-sixes'),width = 2 ),

        dbc.Col(html.Div(id='batter-fours'),width = 2 ) , 
        
        dbc.Col(html.Div(id = 'batter-av-sr' ) , width = 2 ) , 

        dbc.Col(html.Div(id = 'batter-fifty'  ) , width = 2) , 

        dbc.Col(html.Div(id = 'batter-hundred'  ) , width = 2) , 
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(id='plot-batter-dismissals'),
        ], width=7),

        dbc.Col([ 
            html.Div(id = 'plot-runs-scored-against-bowlers'),
        ] , width=5 )
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(id = 'plot-runs')
        ]) , 
        dbc.Col([
            html.Div(id = "plot-season-wise-violin-plot")
        ])
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(id='plot-stadium-wise-runs'),
        ], width=4),

        dbc.Col([ 
             html.Div(id = 'runs-distribution'),
        ] , width=6  )
    ]),
    
])

@app.callback(
    Output('tabs-content', 'children'),
    [Input('tabs', 'value')]
)
def render_content(tab):
    if tab == 'tab-home':
        return html.Div([
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.Div(html.Img(src='assets/trophy_logo.png', style={'height': '100px', 'width': '100px'})),
                                ]),
                                dbc.Col([
                                    html.H4("Title Winner"),
                                    html.Div(id='trophy-winner-info')
                                ])
                            ])
                        ])
                    ])
                ], width=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.Div(html.Img(src='assets/orange_cap.png', style={'height': '80px', 'width': '140px'})),
                                ]),
                                dbc.Col([
                                    html.H4("Orange Cap"),
                                    html.Div(id='orange-cap-winner-info')
                                ])
                            ]),
                        ])
                    ])
                ], width=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.Div(html.Img(src='assets/purple_cap.png', style={'height': '80px', 'width': '140px'})),
                                ]),
                                dbc.Col([
                                    html.H4("Purple Cap"),
                                    html.Div(id='purple-cap-winner-info')
                                ])
                            ]),
                        ])
                    ])
                ], width=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            # html.H4("Stats"),
                            dbc.Row([
                                dbc.Col([
                                    html.Div(html.Img(src='assets/ipl_logo.png', style={'height': '84px', 'width': '80px'})),
                                ]),
                                dbc.Col([
                                    html.Div(id="stats-info")
                                ])
                            ])
                        ])
                    ])
                ], width=3)
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Matches Won by Toss Decision") , 
                            html.Div(id='matches-by-toss-decision-plot'),
                        ])
                    ])
                ], width=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Teams Overall Performance") ,
                            html.Div(id='team-performance-plot'),
                        ])
                    ])
                ], width=5),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Matches Won vs Lost by Teams"),
                            html.Div(id='matches-won-by-teams-plot')
                        ])
                    ])
                ], width=4)
            ]),
        ])
    elif tab == 'tab-teams':
        return html.Div([
            html.Div([
                html.Label("Select Team"),
                dcc.Dropdown(
                    id='team-dropdown',
                    options=[
                        {'label': team, 'value': team} for team in get_all_teams(match_data)
                    ],
                   value=get_all_teams(match_data)[0],
                ),
            ], style={'width': '20%', 'display': 'inline-block', 'verticalAlign': 'top'}),
            html.H3( id = "select-team-info"), 
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.Div(html.Img(src='assets/trophy_logo.png', style={'height': '100px', 'width': '100px'})),
                                ]),
                                dbc.Col([
                                    # html.H4("Title Winner"),
                                    html.Div(id='team-trophy-winner-info')
                                ])
                            ])
                        ])
                    ])
                ], width=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.Div(html.Img(src='assets/orange_cap.png', style={'height': '80px', 'width': '140px'})),
                                ]),
                                dbc.Col([
                                    html.H4("Most Runs"),
                                    html.Div(id='team-most-runs')
                                ])
                            ]),
                        ])
                    ])
                ], width=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.Div(html.Img(src='assets/purple_cap.png', style={'height': '80px', 'width': '140px'})),
                                ]),
                                dbc.Col([
                                    html.H4("Most Wickets"),
                                    html.Div(id='team-most-wickets')
                                ])
                            ]),
                        ])
                    ])
                ], width=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.Div(html.Img(src='assets/ipl_logo.png', style={'height': '84px', 'width': '80px'})),
                                ]),
                                dbc.Col([
                                    html.Div(id="team-stats-info")
                                ])
                            ])
                        ])
                    ])
                ], width=3)
            ]),

            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Win by Toss Decision") , 
                            html.Div(id='toss-decision-plot'),
                        ])
                    ])
                ], width=3),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Top Batsman"),
                            html.Div(id='top-batsmen-plot'),
                        ])
                    ])
                ], width=5),  
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Top Bowler"),
                            html.Div(id='top-bowlers-plot'),
                        ])
                    ])
                ], width=4),  
                
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Stadium-wise Wins"),
                            html.Div(id='stadium-matches-plot'),
                        ])
                    ])
                ], width=7),

                dbc.Col([ 
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Wins/Losses against opponents"),
                            html.Div(id = 'plot-matches-by-team'),
                        ])
                    ]),
                    
                ] , width=5 )
            ]),

        ])
    elif tab == 'tab-batter':
        return html.Div([
            html.Div([
                html.Label("Select Batsman"),
                dcc.Dropdown(
                    id='batsman-dropdown',
                    options=[
                        {'label': team, 'value': team} for team in get_all_batsman(ball_data)
                    ],
                   value="V Kohli",
                ),
            ], style={'width': '20%', 'display': 'inline-block', 'verticalAlign': 'top'}),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.Div(html.Img(src='assets/ipl_logo.png', style={'height': '84px', 'width': '80px'})),
                                ]),
                                dbc.Col([
                                    html.Div(id='batter-runs')
                                ])
                            ])
                        ])
                    ])
                ], width=2),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.Div(html.Img(src='assets/sixes.png', style={'height': '80px', 'width': '80px'})),
                                ]),
                                dbc.Col([
                                    html.Div(id='batter-sixes')
                                ])
                            ]),
                        ])
                    ])
                ], width=2),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.Div(html.Img(src='assets/fours.png', style={'height': '80px', 'width': '80px'})),
                                ]),
                                dbc.Col([
                                    # html.H4("Most Wickets"),
                                    html.Div(id='batter-fours')
                                ])
                            ]),
                        ])
                    ])
                ], width=2),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.Div(html.Img(src='assets/ipl_logo.png', style={'height': '84px', 'width': '80px'})),
                                ]),
                                dbc.Col([
                                    html.Div(id="batter-av-sr")
                                ])
                            ])
                        ])
                    ])
                ], width=2),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.Div(html.Img(src='assets/fifty.png', style={'height': '84px', 'width': '80px'})),
                                ]),
                                dbc.Col([
                                    html.Div(id="batter-fifty")
                                ])
                            ])
                        ])
                    ])
                ], width=2),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.Div(html.Img(src='assets/hundred.png', style={'height': '84px', 'width': '80px'})),
                                ]),
                                dbc.Col([
                                    html.Div(id="batter-hundred")
                                ])
                            ])
                        ])
                    ])
                ], width=2)
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div(id = 'plot-runs')
                        ])
                    ])
                ]) , 
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div(id = "plot-season-wise-violin-plot")
                        ])
                    ])
                ])
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Most Dismissals against Bowlers"),
                            html.Div(id='plot-batter-dismissals'),
                        ])
                    ])
                ], width=6),

                dbc.Col([ 
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Most Runs Scored against bowlers"),
                            html.Div(id = 'plot-runs-scored-against-bowlers'),
                        ])
                    ]),
                    
                ] , width=6  )
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.Div(id='plot-stadium-wise-runs'),
                        ])
                    ])
                ], width=6),

                dbc.Col([ 
                    dbc.Card([
                        dbc.CardBody([
                            html.Div(id = 'runs-distribution'),
                        ])
                    ]),
                    
                ] , width=6  )
            ]),

        ])

    
    else:
        return html.Div([
            html.H4('404 - Not Found'),
            html.P("The content for this tab is not available.")
        ])


@app.callback(
    Output('trophy-winner-info', 'children'),
    [Input('year-dropdown', 'value')]
)
def update_trophy_winner_info(selected_year):
    if selected_year:
        winner_data = get_winner(match_data, selected_year)
        return html.Div([
            html.P(f"{winner_data['winner']}"),
            # html.P(f"Winning Team: {winner_data['team-1']} vs {winner_data['team-2']}"),
            # html.P(f"{winner_data['won_by']}")
        ])
    else:
        most_time_winner_data = get_most_time_winner(match_data)
        most_time_winners = most_time_winner_data['most_time_winners']
        most_titles_won = most_time_winner_data['most_titles_won_by_a_team']
        
        winner_info = ", ".join(most_time_winners)
        
        return html.Div([
            html.P(f"{winner_info}"),
            html.P(f"{most_titles_won} times    ")
        ])


@app.callback(
    Output('orange-cap-winner-info' , 'children') , 
    [Input('year-dropdown' , 'value')] 
)
def update_orange_cap_winner_info(selected_year):
    if(selected_year):
        data = orange_cap_data[str(selected_year)]
        return html.Div([
            html.P(f"{data['player']}"),
            html.P(f"Runs {data['runs']}") , 
            # html.P(f"Strike Rate {data['strike_rate']}") , 
            # html.P(f"6s {data['sixes']}"),
            # html.P(f"4s {data['fours']}")
        ])
    else:
        data = orange_cap_data['All']
        return html.Div([
            html.P(f"{data['player']}"),
            html.P(f"Runs {data['runs']}") , 
            # html.P(f"Strike Rate {data['strike_rate']}") , 
            # html.P(f"6s {data['sixes']}"),
            # html.P(f"4s {data['fours']}")
        ])
    

@app.callback(
    Output('purple-cap-winner-info' , 'children') , 
    [Input('year-dropdown' , 'value')]
)
def update_purple_cap_winner_info(selected_year):
    if(selected_year):
        data = purple_cap_data[str(selected_year)]
        return html.Div([
            html.P(f"{data['player']}"),
            html.P(f"Wickets {data['wickets']}") , 
            # html.P(f"Economy {data['economy']}") , 
            # html.P(f"Average {data['average']}"),
            # html.P(f"Bowling SR {data['bowling_strike_rate']}")
        ])
    else:
        data = purple_cap_data['All'] 
        return html.Div([
            html.P(f"{data['player']}"),
            html.P(f"Wickets {data['wickets']}") , 
            # html.P(f"Economy {data['economy']}") , 
            # html.P(f"Average {data['average']}"),
            # html.P(f"Bowling SR {data['bowling_strike_rate']}")
        ])
    
@app.callback(
    Output('stats-info' , 'children') , 
    [Input('year-dropdown' , 'value')]
)
def update_stats_info(selected_year):
    if(selected_year):
        stats = get_stats(match_data , ball_data , season = selected_year) 
        average_score = stats['average_score'] 
        sixes = stats['sixes'] 
        fours = stats['fours'] 
        return html.Div([
            html.H5(f"Total Matches {stats['total_matches']}"),
            html.P(f"Average Score {average_score}") ,
            html.P(f"6s : {sixes if sixes < 1000 else str(round(sixes/1000 , 2)) + 'k'} 4s : {fours if fours < 1000 else str(round(fours/1000)) + 'k'}")
        ])
    else:
        stats = get_stats(match_data , ball_data , season = selected_year) 
        average_score = stats['average_score'] 
        sixes = stats['sixes'] 
        fours = stats['fours'] 
        return html.Div([
            html.H5(f"Total Matches {stats['total_matches']}"),
            html.P(f"Average Score {average_score}") ,
            html.P(f"6s : {sixes if sixes < 1000 else str(round(sixes/1000 , 2)) + 'k'} 4s : {fours if fours < 1000 else str(round(fours/1000)) + 'k'}")
        ])


@app.callback(
    Output('matches-by-toss-decision-plot', 'children'),
    [Input('year-dropdown', 'value')]
)
def update_matches_by_toss_decision(selected_year):
    if selected_year:
        fig = plot_match_won_by_toss_decision(match_data, season=selected_year)
        return dcc.Graph(figure=fig)
    else:
        fig = plot_match_won_by_toss_decision(match_data)
        return dcc.Graph(figure=fig)

@app.callback(
    Output('team-performance-plot', 'children'),
    [Input('year-dropdown', 'value')]
)
def update_team_performance(selected_year):
    fig = plot_team_performance(match_data)
    return dcc.Graph(figure=fig)


@app.callback(
    Output('matches-won-by-teams-plot', 'children'),
    [Input('year-dropdown', 'value')]
)
def update_matches_won_by_teams(selected_year):
    if selected_year:
        fig = plot_percentage_matches_won_and_lost_by_teams(match_data, season=selected_year)
        return dcc.Graph(figure=fig)
    else:
        fig = plot_percentage_matches_won_and_lost_by_teams(match_data ) 
        return dcc.Graph(figure=fig)


@app.callback(
    Output('select-team-info' , 'children'),
    [Input('tabs' , 'value') ,
    Input('year-dropdown' , 'value'),
    Input('team-dropdown' , 'value') 
    ]
)
def update_team_select_info(active_tab , selected_year , selected_team ) : 
    if active_tab == 'tab-teams':
        return html.H3(f"{selected_team}")
    else:
        return "" 

@app.callback(
    Output('team-trophy-winner-info', 'children'),
    [Input('tabs', 'value'),
     Input('year-dropdown', 'value'),
     Input('team-dropdown', 'value')]
)
def update_team_trophy_winner_info(active_tab, selected_year, selected_team):
    if active_tab == 'tab-teams':
        if selected_team is None:
            selected_team = get_all_teams(match_data)[0]
        titles = len(match_data[(match_data['MatchNumber'] == 'Final') & (match_data['WinningTeam'] == selected_team) ])
        # if selected_year != None : 
        #     titles = len(match_data[(match_data['MatchNumber'] == 'Final') & (match_data['WinningTeam'] == selected_team) & (match_data['Season'] == selected_year)])

        return html.Div(
            [html.H3("Titles"),
            html.H4(f"{titles}")]
        )
       
    else:
        return ""
    


@app.callback(
    Output('team-most-runs', 'children'),
    [Input('tabs', 'value'),
     Input('year-dropdown', 'value'),
     Input('team-dropdown', 'value')]
)
def update_team_most_runs(active_tab, selected_year, selected_team):
    if active_tab == 'tab-teams':
        if selected_team is None:
            selected_team = get_all_teams(match_data)[0]  
        try:
            best_batsman , best_score = get_top_batsman(ball_data , match_data , team_name=selected_team , season = selected_year) 
            return html.Div(
                [html.H3(f"{best_batsman}"),
                html.H4(f"{best_score}") , 
                ]
            )
        except:
            return html.Div([html.P(f"Error: {selected_team} did not played season {selected_year}")])
    else:
        return ""


@app.callback(
    Output('team-most-wickets', 'children'),
    [Input('tabs', 'value'),
     Input('year-dropdown', 'value'),
     Input('team-dropdown', 'value')]
)
def update_team_most_wickets(active_tab, selected_year, selected_team):
    if active_tab == 'tab-teams':
        if selected_team is None:
            selected_team = get_all_teams(match_data)[0]  
        try:
            best_bowler , best_wickets = get_top_bowlers(ball_data , match_data , team_name=selected_team , season = selected_year) 
            return html.Div(
                [html.H3(f"{best_bowler}"),
                html.H4(f"{best_wickets}") , 
                ]
            )
        except:
            return html.Div([html.P(f"Error: {selected_team} did not played season {selected_year}")])
    else:
        return ""


@app.callback(
    Output('team-stats-info', 'children'),
    [Input('tabs', 'value'),
     Input('year-dropdown', 'value'),
     Input('team-dropdown', 'value')]
)
def update_team_stats_info(active_tab, selected_year, selected_team):
    if active_tab == 'tab-teams':
        if selected_team is None:
            selected_team = get_all_teams(match_data)[0]  
        # data = get_scores_data(match_data , ball_data , selected_team , selected_year ) 
        if selected_year is None : 
            selected_year = "All"
        try:
            selected_year = str(selected_year)
            data = teams_scores_data
            average_score = data[selected_team][selected_year]['average_score'] 
            sixes = str(data[selected_team][selected_year]['total_sixes']) if int(data[selected_team][selected_year]['total_sixes']) < 1000 else str(round(int(data[selected_team][selected_year]['total_sixes'])/1000 , 2 ) )+ 'k'
            fours = str(data[selected_team][selected_year]['total_fours']) if int(data[selected_team][selected_year]['total_fours']) < 1000 else str(round(int(data[selected_team][selected_year]['total_fours'])/1000 , 2) )+ 'k' 
        
            if selected_year != "All":
                matches_won = len(match_data[(match_data['WinningTeam'] == selected_team) & (match_data['Season'] == int(selected_year))])
            else:
                matches_won = len(match_data[match_data['WinningTeam'] == selected_team])
            return html.Div([
                html.P(f"Matches : {data[selected_team][selected_year]['matches_played']}"),
                html.P(f"Won : {matches_won}"), 
                html.P(f"Average Score: {average_score}"),
                html.P(f"6s: {sixes}    4s: {fours}"),
                html.P(f"Best {data[selected_team][selected_year]['best']}")
            ])
        except:
            return html.Div([html.P(f"Error: {selected_team} did not played season {selected_year}")])
    else:
        return ""


@app.callback(
    Output('top-batsmen-plot', 'children'),
    [Input('year-dropdown', 'value'),
     Input('team-dropdown', 'value')]
)
def update_top_batsmen_plot(selected_year, selected_team):
    if selected_year and selected_team:
        batsmen_data = best_batsmen(ball_data, match_data, selected_team, season=selected_year)
        fig = plot_top_5_batsmen(batsmen_data)
        return dcc.Graph(figure=fig)
    elif selected_year == None and selected_team:
        batsmen_data = best_batsmen(ball_data, match_data, selected_team)
        fig = plot_top_5_batsmen(batsmen_data)
        return dcc.Graph(figure=fig)
    else:
        return ""

@app.callback(
    Output('top-bowlers-plot', 'children'),
    [Input('year-dropdown', 'value'),
     Input('team-dropdown', 'value')]
)
def update_top_bowlers_plot(selected_year, selected_team):
    if selected_year and selected_team:
        bowlers_data = top_bowlers(ball_data, match_data, selected_team, season=selected_year)
        fig = plot_top_5_bowlers(bowlers_data)
        return dcc.Graph(figure=fig)
    if selected_year == None and selected_team:
        bowlers_data = top_bowlers(ball_data, match_data, selected_team)
        fig = plot_top_5_bowlers(bowlers_data)
        return dcc.Graph(figure=fig)
    else:
        return ""
# Update the callbacks to generate plots
@app.callback(
    Output('stadium-matches-plot', 'children'),
    [Input('year-dropdown', 'value'),
     Input('team-dropdown', 'value')]
)
def update_stadium_matches_plot(selected_year, selected_team):
    if selected_team:
        fig = plot_stadium_matches_for_team(match_data, selected_team , season = selected_year)
        # return ""
        return dcc.Graph(figure=fig)
    else:
        return ""

@app.callback(
    Output('toss-decision-plot', 'children'),
    [Input('year-dropdown', 'value'),
     Input('team-dropdown', 'value')]
)
def update_toss_decision_plot(selected_year, selected_team):
    if selected_year and selected_team:
        fig = plot_match_won_by_toss_decision(match_data, selected_team=selected_team, season=selected_year)
        return dcc.Graph(figure=fig)
    elif selected_year is None and selected_team:
        fig = plot_match_won_by_toss_decision(match_data, selected_team=selected_team)
        return dcc.Graph(figure=fig)
    else:
        return ""


@app.callback(
    Output('plot-matches-by-team' , 'children') , 
    [Input('year-dropdown' , 'value'),
     Input('team-dropdown' , 'value')]  
)
def update_plot_matches_by_team(selected_year , selected_team ) : 
    if selected_team : 
        fig = plot_matches_by_team(match_data , selected_team , season = selected_year ) 
        return dcc.Graph(figure = fig ) 
    else: 
        return ""


@app.callback(
    Output('batter-runs' , 'children') , 
    [Input('tabs', 'value'),
        Input('year-dropdown' , 'value') , 
     Input('batsman-dropdown' , 'value')] 
)
def update_batter_runs(active_tab , selected_year , selected_batter ) : 
    if active_tab != 'tab-batter':
        return ""
    if selected_batter == None : 
        selected_batter == "V Kohli"
    data = get_batter_runs(match_data , ball_data , batter= selected_batter , season = selected_year) 
    return html.Div([
        html.H3("Runs"),
        html.H3(f"{data['total_runs']}")
    ])

@app.callback(
    Output('batter-fours' , 'children'),
    [Input('tabs', 'value'),
        Input('year-dropdown' , 'value') , 
        Input('batsman-dropdown' , 'value') 
    ]
)
def update_batter_fours(active_tab , selected_year , selected_batter ) : 
    if active_tab != 'tab-batter':
        return ""
    if selected_batter == None : 
        selected_batter == "V Kohli"
    data = get_batter_runs(match_data , ball_data , batter= selected_batter , season = selected_year) 
    return html.Div([
        html.H2(f"{data['fours']}")
    ])


@app.callback(
    Output('batter-sixes' , 'children'),
    [Input('tabs', 'value'),
        Input('year-dropdown' , 'value') , 
        Input('batsman-dropdown' , 'value') 
    ]
)
def update_batter_sixes(active_tab, selected_year , selected_batter ) : 
    if active_tab != 'tab-batter':
        return ""
    if selected_batter == None : 
        selected_batter == "V Kohli"
    data = get_batter_runs(match_data , ball_data , batter= selected_batter , season = selected_year) 
    return html.Div([
        html.H2(f"{data['sixes']}")
    ])


@app.callback(
    Output('batter-av-sr' , 'children') , 
    [Input('tabs' , 'value') ,
     Input('year-dropdown' , 'value'),
     Input('batsman-dropdown' , 'value')] 
)
def update_batter_av_sr(active_tab , selected_year , selected_batter ) : 
    if active_tab != 'tab-batter':
        return ""
    if selected_batter == None : 
        selected_batter == "V Kohli"
    data = get_batter_runs(match_data , ball_data , batter=selected_batter , season=selected_year) 
    average = data['average'] 
    if average == 'inf':
        average = '-'
    else : 
        average = round(average , 2 )
    return html.Div([
        html.H5(f"SR {data['strike_rate']}"),
        html.H5(f"Av {average}")
    ])

@app.callback(
    Output('batter-hundred' , 'children') , 
    [Input('tabs' , 'value'),
     Input('year-dropdown' , 'value'),
     Input('batsman-dropdown' , 'value')] 
)
def update_batter_hundred(active_tab , selected_year , selected_batter ):
    if active_tab != 'tab-batter':
        return ""
    if selected_batter == None : 
        selected_batter == "V Kohli"
    data = get_batter_runs(match_data , ball_data , batter=selected_batter , season=selected_year) 
    return html.Div([
        html.H2(f"{data['hundreds']}")

    ])


@app.callback(
    Output('batter-fifty' , 'children') , 
    [Input('tabs' , 'value'),
     Input('year-dropdown' , 'value'),
     Input('batsman-dropdown' , 'value')] 
)
def update_batter_fifty(active_tab , selected_year , selected_batter ):
    if active_tab != 'tab-batter':
        return ""
    if selected_batter == None : 
        selected_batter == "V Kohli"
    data = get_batter_runs(match_data , ball_data , batter=selected_batter , season=selected_year) 
    return html.Div([
        html.H2(f"{data['fifties']}")

    ])


@app.callback(
    Output('plot-batter-dismissals' , 'children'), 
    [Input('tabs' , 'value'),
        Input('year-dropdown' , 'value') ,
        Input('batsman-dropdown' , 'value') 
    ]
)
def update_plot_batter_dismissals(active_tab , selected_year , selected_batter ) : 
    if active_tab != 'tab-batter':
        return ""
    fig = plot_batter_dismissals(match_data, ball_data, batter= selected_batter, season=selected_year)
    return html.Div([
        dcc.Graph(figure=fig)
    ])



@app.callback(
    Output('plot-runs-scored-against-bowlers' , 'children') , 
    [Input('tabs' , 'value'),
        Input('year-dropdown' , 'value') ,
        Input('batsman-dropdown' , 'value') 
    ]
)
def update_plot_runs_scored_against_bowler(active_tab , selected_year , selected_batter ) : 
    if active_tab != 'tab-batter':
        return ""
    fig = plot_runs_scored_against_bowlers(
        match_data , ball_data , batter= selected_batter , season= selected_year
    )
    return html.Div([
        dcc.Graph(figure=fig)
    ])


@app.callback(
    Output('plot-runs' , 'children') , 
    [
        Input('tabs' , 'value'),
        Input('year-dropdown' , 'value') ,
        Input('batsman-dropdown' , 'value') 
    ]
)
def update_plot_runs(active_tab , selected_year , selected_batter ) : 
    if active_tab != 'tab-batter':
        return "" 
    fig = plot_season_wise_runs(match_data , ball_data, batter=selected_batter , season=selected_year) 
    return html.Div([
        html.H3("Line Plot of Runs scored"),
        dcc.Graph(figure=fig)
    ])


@app.callback(
    Output('plot-season-wise-violin-plot' , 'children') , 
    [
        Input('tabs' , 'value'),
        Input('year-dropdown' , 'value') ,
        Input('batsman-dropdown' , 'value') 
    ]
)
def update_plot_season_wise_violin_plot( active_tab , selected_year , selected_battter ) : 
    if active_tab != 'tab-batter':
        return "" 
    fig = plot_season_wise_violin_plot(match_data , ball_data , batter=selected_battter ) 
    return html.Div([
        html.H3("Season Wise Runs Violin plot"),
        dcc.Graph(figure = fig)
    ])

@app.callback(
    Output('plot-stadium-wise-runs' , 'children'),
    [
        Input('tabs' , 'value'),
        Input('year-dropdown' , 'value') ,
        Input('batsman-dropdown' , 'value') 
    ]
)
def update_plot_stadium_wise_runs(active_tab, selected_year , selected_batter ) :
    if active_tab != 'tab-batter':
        return ""
    fig = stadium_wise_runs(match_data , ball_data , batter = selected_batter , season = selected_year) 
    return html.Div([
        html.H3("Stadium wise runs (top 5)") , 
        dcc.Graph(figure=fig)
    ])


@app.callback(
    Output('runs-distribution' , 'children'),
    [
        Input('tabs' , 'value'),
        Input('year-dropdown' , 'value') ,
        Input('batsman-dropdown' , 'value') ,
        
    ]
)
def update_plot_runs_distribution(active_tab, selected_year , selected_batter ) :
    if active_tab != 'tab-batter':
        return ""
    fig = plot_runs_distribution(match_data , ball_data , batter = selected_batter , season = selected_year) 
    return html.Div([
        html.H3("Runs distribution") , 
        dcc.Graph(figure=fig)
    ])

if __name__ == '__main__':
    app.run_server(debug=False ,)
