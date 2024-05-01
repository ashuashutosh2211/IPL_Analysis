# Import necessary libraries
from dash import Dash, dcc, html, Input, Output
import dash
import dash_bootstrap_components as dbc
import plotly.express as px
import numpy as np
import pandas as pd
import preprocess_match_data
import match_data_info
from match_data_info import get_most_time_winner, get_all_teams , get_winner , get_stats , get_scores_data , get_top_batsman , get_top_bowlers , get_all_batsman , get_batter_runs , get_all_bowlers , get_bowler_wickets 
from match_data_plots import plot_match_won_by_toss_decision, plot_team_performance, plot_percentage_matches_won_and_lost_by_teams, best_batsmen , plot_top_5_batsmen, top_bowlers, plot_top_5_bowlers ,plot_stadium_matches_for_team , plot_matches_by_team
from match_data_plots import plot_batter_dismissals , plot_runs_scored_against_bowlers , stadium_wise_runs , plot_season_wise_runs , plot_season_wise_violin_plot, plot_runs_distribution , toss_winner_match_wins_pie , team_toss_outcomes_bar_chart , plot_match_wins
from match_data_plots import wicket_heatmap_for_team , runs_heatmap_by_bowl_over , average_vs_strike_rate, average_vs_economy_rate , plot_toss_outcome_team , runs_scored_by_over_type , plot_runs_scored_against_teams , runs_heatmap_for_batter
from match_data_plots import wickets_taken_by_over_type , plot_wickets_dot_4s_6s , plot_bowler_most_beaten_by_batsman, plot_bowler_wickets
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
app = dash.Dash(__name__, external_stylesheets=external_stylesheets , suppress_callback_exceptions=True  )

app.layout = html.Div([
    html.H1("IPL Analysis Dashboard", 
    style={
        'textAlign': 'center',
        'background-color': '#223577',
        'color': 'white',
        'padding': '10px'  # optional: adds some padding for better appearance
    }
),
    html.Div(
    dcc.Tabs(
        id='tabs', 
        value='tab-home', 
        children=[
        dcc.Tab(label='Home', value='tab-home', 
                selected_style={'backgroundColor': '#0b1434c9'}, 
                style={'backgroundColor': '#223577c9'}),
        dcc.Tab(label='Teams', value='tab-teams', 
                selected_style={'backgroundColor': '#0b1434c9'}, 
                style={'backgroundColor': '#223577c9'}),
        dcc.Tab(label='Batsman', value='tab-batter', 
                selected_style={'backgroundColor': '#0b1434c9'}, 
                style={'backgroundColor': '#223577c9'}),
        dcc.Tab(label='Bowler', value='tab-bowler', 
                selected_style={'backgroundColor': '#0b1434c9'}, 
                style={'backgroundColor': '#223577c9'})
        # Add more tabs here as needed
    ],
        style={
            'font-size': '25px', 
            'color': 'white',            # Text color of the tabs
            'font-weight': 'bold' ,
            # Font size 0.75 times of the heading
        },
              # Bold text
        
        parent_style={
            'width': '100%'  # Width of the tab container
        }
    ),
    style={'margin': '0 10px'}  # Left and right margin of 10px
),
    
    
    html.Div([
        html.Label("Select Season", style={'font-weight': 'bold', 'margin-left': '10px'}),
        dcc.Dropdown(
            id='year-dropdown',
            options=[
                {'label': str(year), 'value': year} for year in range(2008, 2023)
            ],
            style={'width': '100%'}  # Setting the width of the dropdown to 50%
        )
    ], style={'display': 'inline-block', 'verticalAlign': 'top', 'margin-left': '10px'}),
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
            
        ], ) , 
        dbc.Col([
            html.Div(id = "outcome-toss-wins")

        ]) , 
        dbc.Col([
            html.Div(id = "toss-won-by-teams")

        ])
    ]),
    dbc.Row([
        
        dbc.Col([
            html.Div(id='team-performance-plot'),
        ], width = 5 ),
        dbc.Col([
            html.Div(id='matches-won-by-teams-plot')
        ], width=4)
    ]),
    dbc.Row([
        dbc.Col([
            
            html.Div(id='runs-heatmap'),
              
        ], width=6),
        dbc.Col([
           
            html.Div(id='wickets-heatmap'),
                
        ], width=6)
    ]) , 

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
            # html.H4("Toss won v/s lost ") , 
            html.Div(id = "plot-toss-outcome-team")
    
        ]),
        dbc.Col([
           html.Div(id='toss-decision-plot'),
        ], width=3),

        dbc.Col([
            html.Div(id = 'team-outcome-toss-win') , 
        ])
        ,
        
    ]),
    dbc.Row([
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
    dbc.Row([
        dbc.Col([
            html.Div(id = "plot-average-vs-strike_rate-batsman")

        ] , width= 6 ) , 
        dbc.Col([
            html.Div(id = "plot-economy-vs-average-bowler")

        ] , width=6)
    ]),
    dbc.Row([
        dbc.Col([
            
            html.Div(id='team-runs-heatmap'),
              
        ], width=6),
        dbc.Col([
           
            html.Div(id='team-wickets-heatmap'),
                
        ], width=6)
    ]) 
    ,
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
            html.Div(id = 'runs-distribution'),
        ] , width=6  ) , 
        
        dbc.Col([ 
            html.Div(id = 'runs-scored-by-over-type'),
        ] , width=6  )
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
            html.Div(id = "plot-runs-heatmap-batter")
        ])
    ]),
    
    dbc.Row([
        dbc.Col([
            html.Div(id='plot-stadium-wise-runs'),
        ], width=6),
        dbc.Col([
            html.Div(id = "plot-runs-scored-against-teams") ,
        ], width = 6 )
    ]),
    
    html.Div([dcc.Dropdown(id='bowler-dropdown')], style={'display': 'none'}),

    dbc.Row([
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    html.Div(id = 'bowler-wickets')
                ])
            ])
        ] , width= 2 ) ,
         dbc.Col([
             dbc.Row([
                 dbc.Col([
                     html.Div(id = 'bowler-average') 
                 ])
             ])
         ]) , 
         dbc.Col([
             dbc.Row([
                 dbc.Col([
                     html.Div(id = 'bowler-economy-rate') 
                 ])
             ])
         ]) , 
         dbc.Col([
             dbc.Row([
                 dbc.Col([
                     html.Div(id = 'bowler-strike-rate') 
                 ])
             ])
         ]) , 
         dbc.Col([
             dbc.Row([
                 dbc.Col([
                     html.Div(id = 'bowler-matches') 
                 ])
             ])
         ]) , 
         dbc.Col([
             dbc.Row([
                 dbc.Col([
                     html.Div(id = 'runs-given') 
                 ])
             ])
         ]) , 

    ]) , 
    dbc.Row([
        dbc.Col([ 
                    html.Div(id = 'bowling-distribution'),

            
        ] , width=6  ) , 
        
        dbc.Col([ 
                    html.Div(id = 'wickets-taken-by-over-type'),

            
        ] , width=6  )
    ]),
    dbc.Row([
        dbc.Col([

            html.Div(id='plot-bowler-wickets'),

        ], width=6),

        dbc.Col([ 

            html.Div(id = 'plot-bowler-most-beaten-by-batsman'),

            
        ] , width=6  )
    ]),
    
] , id = "main_page" , style={ 'padding': "15px" } )

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
                                    html.H4("Title Winner", style={'font-size': '22px', 'font-weight': 'bold'}),
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
                                    html.H4("Orange Cap", style={'font-size': '22px', 'font-weight': 'bold'}),
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
                                    html.H4("Purple Cap", style={'font-size': '22px', 'font-weight': 'bold'}),
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
                html.H2("Analysis based on toss wins",style={
                    'textAlign': 'center',
                    'padding': '10px'  # optional: adds some padding for better appearance
    }),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Matches Won by Toss Decision", style={'font-size': '22px', 'font-weight': 'bold'}) , 
                            html.Div(id='matches-by-toss-decision-plot'),
                        ])
                    ])
                ], width=4),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Outcomes of Toss Wins: Matches Won vs. Matches Lost", style={'font-size': '22px', 'font-weight': 'bold'}) ,
                            html.Div(id = "outcome-toss-wins")
                        ])
                    ])
                ] , width = 4 ) , 
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Tosses Won by Teams", style={'font-size': '22px', 'font-weight': 'bold'}) , 
                            html.Div(id = "toss-won-by-teams")
                        ])
                    ])
                ] , width = 4 )
                
            ]),
            dbc.Row([
                html.H2("Analysis based on team performance",style={
                    'textAlign': 'center',
                    'padding': '10px'  # optional: adds some padding for better appearance
    }),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Teams Overall Performance", style={'font-size': '22px', 'font-weight': 'bold'}) ,
                            html.Div(id='team-performance-plot'),
                        ])
                    ])
                ], width=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Matches Won and Lost by Teams", style={'font-size': '22px', 'font-weight': 'bold'}),
                            html.Div(id='matches-won-by-teams-plot')
                        ])
                    ])
                ], width=6)
            ]) , 
            dbc.Row([
                html.H2("Analysis of runs and wickets by balls and overs",style={
                    'textAlign': 'center',
                    'padding': '10px'  # optional: adds some padding for better appearance
    }),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Runs", style={'font-size': '22px', 'font-weight': 'bold'}) ,
                            html.Div(id='runs-heatmap'),
                        ])
                    ])
                ], width=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Wickets", style={'font-size': '22px', 'font-weight': 'bold'}) ,
                            html.Div(id='wickets-heatmap'),
                        ])
                    ])
                ], width=6)
            ]) , 
        ])
    elif tab == 'tab-teams':
        return html.Div([
            html.Div([
                html.Label("Select Team", style={'font-weight': 'bold', 'margin-left': '10px'}),
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
                                    html.Div(html.Img(src='assets/trophy_logo.png', style={'height': '150px', 'width': '150px'})),
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
                                    html.H4("Most Runs", style={'font-size': '22px', 'font-weight': 'bold'}),
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
                                    html.H4("Most Wickets", style={'font-size': '22px', 'font-weight': 'bold'}),
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
                            html.H4("Toss won v/s lost ", style={'font-size': '22px', 'font-weight': 'bold'}) , 
                            html.Div(id = "plot-toss-outcome-team")
                        ])
                    ])
                ] , width = 4 ),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Win by Toss Decision", style={'font-size': '22px', 'font-weight': 'bold'}) , 
                            html.Div(id='toss-decision-plot'),
                        ])
                    ])
                ], width=4),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Outcome when won the Toss", style={'font-size': '22px', 'font-weight': 'bold'}) ,
                            html.Div(id = "team-outcome-toss-win") , 
                        ])
                    ])
                ] , width = 4 ),
                
                
                
            ]),
            dbc.Row([
                html.H2("Top Performers",style={
                    'textAlign': 'center',
                    'padding': '10px'  # optional: adds some padding for better appearance
    }),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Batsman", style={'font-size': '22px', 'font-weight': 'bold'}),
                            html.Div(id='top-batsmen-plot'),
                        ])
                    ])
                ], width=6),  
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Bowler", style={'font-size': '22px', 'font-weight': 'bold'}),
                            html.Div(id='top-bowlers-plot'),
                        ])
                    ])
                ], width=6),  
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Stadium-wise Wins", style={'font-size': '22px', 'font-weight': 'bold'}),
                            html.Div(id='stadium-matches-plot'),
                        ])
                    ])
                ], width=7),

                dbc.Col([ 
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Wins/Losses against opponents", style={'font-size': '22px', 'font-weight': 'bold'}),
                            html.Div(id = 'plot-matches-by-team'),
                        ])
                    ]),
                    
                ] , width=5 )
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Batsman Strike rate v/s Average", style={'font-size': '22px', 'font-weight': 'bold'}) ,
                            html.Div(id = "plot-average-vs-strike_rate-batsman")
                        ])
                    ])
                ] , width= 6 ) , 
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Bowler Economy v/s Average", style={'font-size': '22px', 'font-weight': 'bold'}) ,
                            html.Div(id = "plot-economy-vs-average-bowler")
                        ])
                    ])
                ] , width=6)
            ]),
            dbc.Row([
                html.H2("Analysis of runs and wickets by balls and overs",style={
                    'textAlign': 'center',
                    'padding': '10px'  # optional: adds some padding for better appearance
    }),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Runs", style={'font-size': '22px', 'font-weight': 'bold'}) ,
                            html.Div(id='team-runs-heatmap'),
                        ])
                    ])
                ], width=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Wickets", style={'font-size': '22px', 'font-weight': 'bold'}) ,
                            html.Div(id='team-wickets-heatmap'),
                        ])
                    ])
                ], width=6)
            ]) , 

        ])
    elif tab == 'tab-batter':
        return html.Div([
            html.Div([
                html.Label("Select Batsman", style={'font-weight': 'bold', 'margin-left': '10px'}),
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
                            html.H4("Runs distribution", style={'font-size': '22px', 'font-weight': 'bold'}) , 
                            html.Div(id = 'runs-distribution'),
                        ])
                    ]),
                    
                ] , width=6  ) , 
                
                dbc.Col([ 
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Runs by Over type", style={'font-size': '22px', 'font-weight': 'bold'}) , 
                            html.Div(id = 'runs-scored-by-over-type'),
                        ])
                    ]),
                    
                ] , width=6  )
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Most Dismissals against Bowlers", style={'font-size': '22px', 'font-weight': 'bold'}),
                            html.Div(id='plot-batter-dismissals'),
                        ])
                    ])
                ], width=6),

                dbc.Col([ 
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Most Runs Scored against bowlers", style={'font-size': '22px', 'font-weight': 'bold'}),
                            html.Div(id = 'plot-runs-scored-against-bowlers'),
                        ])
                    ]),
                    
                ] , width=6  )
            ]),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Stadium wise runs", style={'font-size': '22px', 'font-weight': 'bold'}) , 
                            html.Div(id='plot-stadium-wise-runs'),
                        ])
                    ])
                ], width=6),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Runs against teams", style={'font-size': '22px', 'font-weight': 'bold'}) , 
                            html.Div(id='plot-runs-scored-against-teams'),
                        ])
                    ])
                ], width=6),
                
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
                                html.H4("Runs distribution across overs", style={'font-size': '22px', 'font-weight': 'bold'}),
                                html.Div(id = "plot-runs-heatmap-batter")
                            ])
                        ])
                    ]),
                ]),
            ]),

        ])
    elif tab == 'tab-bowler':
        return html.Div([
            html.Div([
                html.Label("Select Bowler", style={'font-weight': 'bold', 'margin-left': '10px'}),
                dcc.Dropdown(
                    id='bowler-dropdown',
                    options=[
                        {'label': team, 'value': team} for team in get_all_bowlers(ball_data)
                    ],
                   value="JJ Bumrah",
                ),
            ], style={'width': '20%', 'display': 'inline-block', 'verticalAlign': 'top'}),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            dbc.Row([
                                dbc.Col([
                                    html.Div(html.Img(src='assets\wicket.png', style={'height': '74px', 'width': '70px'})),
                                ]),
                                dbc.Col([
                                    html.H4("Wickets", style={'font-size': '22px', 'font-weight': 'bold'}),
                                    html.Div(id='bowler-wickets')
                                ])
                            ])
                        ])
                    ])
                ], width=2),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            # dbc.Row([
                            #     dbc.Col([
                            #         html.Div(html.Img(src='assets/sixes.png', style={'height': '80px', 'width': '80px'})),
                            #     ]),
                            #     dbc.Col([
                            html.H4("Average", style={'font-size': '22px', 'font-weight': 'bold'}) , 
                            html.Div(id='bowler-average')
                            #     ])
                            # ]),
                        ])
                    ])
                ], width=2),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            
                            html.H4("Economy", style={'font-size': '22px', 'font-weight': 'bold'}),
                            html.Div(id='bowler-economy-rate')
                                
                        ])
                    ])
                ], width=2),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Strike Rate", style={'font-size': '22px', 'font-weight': 'bold'}) , 
                            html.Div(id="bowler-strike-rate")
                              
                        ])
                    ])
                ], width=2),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Matches", style={'font-size': '22px', 'font-weight': 'bold'}) , 
                            html.Div(id="bowler-matches")
                        ])
                    ])
                ], width=2),
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Runs Conceded", style={'font-size': '22px', 'font-weight': 'bold'}) , 
                            html.Div(id="runs-given")
                               
                        ])
                    ])
                ], width=2)
            ]),
            
            dbc.Row([
                dbc.Col([ 
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Bowling Distribution", style={'font-size': '22px', 'font-weight': 'bold'}) , 
                            html.Div(id = 'bowling-distribution'),
                        ])
                    ]),
                    
                ] , width=6  ) , 
                
                dbc.Col([ 
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Runs by Over type", style={'font-size': '22px', 'font-weight': 'bold'}) , 
                            html.Div(id = 'wickets-taken-by-over-type'),
                        ])
                    ]),
                    
                ] , width=6  )
            ]),
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Most wickets taken of batsman", style={'font-size': '22px', 'font-weight': 'bold'}),
                            html.Div(id='plot-bowler-wickets'),
                        ])
                    ])
                ], width=6),

                dbc.Col([ 
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Most runs conceded to batsman", style={'font-size': '22px', 'font-weight': 'bold'}),
                            html.Div(id = 'plot-bowler-most-beaten-by-batsman'),
                        ])
                    ]),
                    
                ] , width=6  )
            ]),
            
            # dbc.Row([
            #     dbc.Col([
            #         dbc.Card([
            #             dbc.CardBody([
            #                 html.H3("Stadium wise runs") , 
            #                 html.Div(id='plot-stadium-wise-runs'),
            #             ])
            #         ])
            #     ], width=6),
            #     dbc.Col([
            #         dbc.Card([
            #             dbc.CardBody([
            #                 html.H3("Runs against teams") , 
            #                 html.Div(id='plot-runs-scored-against-teams'),
            #             ])
            #         ])
            #     ], width=6),
                
            #     dbc.Row([
            #         dbc.Col([
            #             dbc.Card([
            #                 dbc.CardBody([
            #                     html.Div(id = 'plot-runs')
            #                 ])
            #             ])
            #         ]) , 
            #         dbc.Col([
            #             dbc.Card([
            #                 dbc.CardBody([
            #                     html.H3("Runs distribution across overs"),
            #                     html.Div(id = "plot-runs-heatmap-batter")
            #                 ])
            #             ])
            #         ]),
            #     ]),
            # ]),

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
            html.H4(f"Total Matches {stats['total_matches']}", style={'font-size': '22px', 'font-weight': 'bold'}),
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
    if selected_year == None : 
        fig = plot_team_performance(match_data)
        return dcc.Graph(figure=fig)

    else:
        fig = plot_match_wins(match_data , ball_data , season = selected_year )
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
        return html.H4(f"{selected_team}", style={'font-size': '22px', 'font-weight': 'bold'})
    else:
        return "" 


@app.callback(
        Output('outcome-toss-wins' , 'children') , 
        [Input(
            'tabs' , 'value' 
        ),
        Input('year-dropdown' ,'value')]
)
def update_outcome_toss_wins(active_tab , selected_year ) : 
    if active_tab == 'tab-home':
        fig = toss_winner_match_wins_pie(match_data , season = selected_year)
        return dcc.Graph(figure=fig)
    else:
        return ""


@app.callback(
        Output('toss-won-by-teams' , 'children') , 
        [Input(
            'tabs' , 'value' 
        ),
        Input('year-dropdown' ,'value')]
)
def update_toss_won_by_teams(active_tab , selected_year ):
    if active_tab == 'tab-home':
        fig = team_toss_outcomes_bar_chart(match_data , season = selected_year) 
        return dcc.Graph(figure = fig ) 
    else:
        return ""


@app.callback(
    Output('runs-heatmap' , 'children') , 
    [Input(
        'tabs' , 'value' 
    ),
    Input('year-dropdown' ,'value')]
)
def update_runs_heatmap( active_tab , selected_year ) : 
    if active_tab == 'tab-home':
        fig = runs_heatmap_by_bowl_over(match_data , ball_data , season = selected_year)
        return dcc.Graph(figure=fig)
    return ""


@app.callback(
    Output('wickets-heatmap' , 'children') , 
    [Input(
        'tabs' , 'value' 
    ),
    Input('year-dropdown' ,'value')]
)
def update_runs_heatmap( active_tab , selected_year ) : 
    if active_tab == 'tab-home':
        fig = wicket_heatmap_for_team(match_data , ball_data , season = selected_year)
        return dcc.Graph(figure=fig)
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
            [html.H3("Titles", style={'font-size': '22px', 'font-weight': 'bold'}),
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
                [html.H3(f"{best_batsman}", style={'font-size': '22px', 'font-weight': 'bold'}),
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
                [html.H3(f"{best_bowler}", style={'font-size': '22px', 'font-weight': 'bold'}),
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
    Output('plot-toss-outcome-team' , 'children') , 
    [Input('tabs' , 'value') , 
     Input('year-dropdown' , 'value') , 
     Input('team-dropdown' , 'value')]
)
def update_plot_toss_outcome_team(active_tab , selected_year , selected_team ) : 
    if active_tab == 'tab-teams':
        fig = plot_toss_outcome_team(match_data=match_data , team = selected_team , season = selected_year)
        return dcc.Graph(figure = fig )
    return ""


@app.callback(
    Output('team-outcome-toss-win' , 'children') , 
    [Input('tabs' , 'value') , 
     Input('year-dropdown' , 'value') , 
     Input('team-dropdown' , 'value')]
)
def update_team_outcome_toss_win( active_tab , selected_year , selected_team ) : 
    if active_tab == 'tab-teams':
        fig = toss_winner_match_wins_pie(match_data=match_data , team=selected_team , season=selected_year)
        return dcc.Graph(figure = fig )
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
    Output('plot-average-vs-strike_rate-batsman' , 'children') , 
    [Input('tabs', 'value'),Input('year-dropdown' , 'value'),
     Input('team-dropdown' , 'value')]  
)
def update_plot_average_vs_strike_rate_batsman(active_tab , selected_year , selected_team ) : 
    if active_tab == 'tab-teams':
        fig = average_vs_strike_rate(match_data= match_data , ball_data=ball_data , team = selected_team , season = selected_year)
        return dcc.Graph(figure = fig )
    return ""


@app.callback(
    Output('plot-economy-vs-average-bowler' , 'children') , 
    [Input('tabs', 'value'),Input('year-dropdown' , 'value'),
     Input('team-dropdown' , 'value')]  
)
def update_plot_average_vs_strike_rate_batsman(active_tab , selected_year , selected_team ) : 
    if active_tab == 'tab-teams':
        fig = average_vs_economy_rate(match_data= match_data , ball_data=ball_data , team = selected_team , season = selected_year)
        return dcc.Graph(figure = fig )
    return ""



@app.callback(
    Output('team-runs-heatmap' , 'children') , 
    [Input(
        'tabs' , 'value' 
    ),
    Input('year-dropdown' ,'value') , 
    Input('team-dropdown' , 'value')]
)
def update_runs_heatmap( active_tab , selected_year , selected_team  ) : 
    if active_tab == 'tab-teams':
        fig = runs_heatmap_by_bowl_over(match_data , ball_data , season = selected_year , team =selected_team )
        return dcc.Graph(figure=fig)
    return ""


@app.callback(
    Output('team-wickets-heatmap' , 'children') , 
    [Input(
        'tabs' , 'value' 
    ),
    Input('year-dropdown' ,'value'),
    Input('team-dropdown' , 'value')]
)
def update_runs_heatmap( active_tab , selected_year , selected_team ) : 
    if active_tab == 'tab-teams':
        fig = wicket_heatmap_for_team(match_data , ball_data , season = selected_year , team = selected_team)
        return dcc.Graph(figure=fig)
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
        html.H4("Runs", style={'font-size': '22px', 'font-weight': 'bold'}),
        html.P(f"{data['total_runs']}")
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
        html.H4(f"{data['fours']}", style={'font-size': '22px', 'font-weight': 'bold'})
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
        html.H4(f"{data['sixes']}", style={'font-size': '22px', 'font-weight': 'bold'})
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
        html.H4(f"SR {data['strike_rate']}", style={'font-size': '22px', 'font-weight': 'bold'}),
        html.H4(f"Av {average}", style={'font-size': '22px', 'font-weight': 'bold'})
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
        html.H4(f"{data['hundreds']}", style={'font-size': '22px', 'font-weight': 'bold'})

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
        html.H4(f"{data['fifties']}", style={'font-size': '22px', 'font-weight': 'bold'})

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
    if selected_batter == None : 
        selected_batter = "V Kohli"
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
    if selected_batter == None : 
        selected_batter = "V Kohli"
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
    if selected_batter == None : 
        selected_batter = "V Kohli"
    fig = plot_season_wise_runs(match_data , ball_data, batter=selected_batter , season=selected_year) 
    title = f"Runs scored in each match of season : {selected_year}"
    if selected_year == None : 
        title = "Runs scored season wise"
    return html.Div([
        html.H4(f"{title}", style={'font-size': '22px', 'font-weight': 'bold'}),
        dcc.Graph(figure=fig)
    ])


# @app.callback(
#     Output('plot-runs-violin-plot-batter' , 'children') , 
#     [
#         Input('tabs' , 'value'),
#         Input('year-dropdown' , 'value') ,
#         Input('batsman-dropdown' , 'value') 
#     ]
# )
# def update_plot_season_wise_violin_plot( active_tab , selected_year , selected_battter ) : 
#     if active_tab != 'tab-batter':
#         return "" 
#     if selected_batter == None : 
#         selected_batter = "V Kohli"
#     fig = plot_season_wise_violin_plot(match_data , ball_data , batter=selected_battter ) 
#     return html.Div([
#         html.H3("Season Wise Runs Violin plot"),
#         dcc.Graph(figure = fig)
#     ])

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
    if selected_batter == None : 
        selected_batter = "V Kohli"
    fig = stadium_wise_runs(match_data , ball_data , batter = selected_batter , season = selected_year) 
    return html.Div([
        dcc.Graph(figure=fig)
    ])

@app.callback(
    Output('plot-runs-scored-against-teams' , 'children') , 
    [
        Input('tabs' , 'value') , 
        Input('year-dropdown' , 'value') , 
        Input('batsman-dropdown' , 'value') 
    ]
)
def update_plot_runs_scored_against_teams(active_tab , selected_year , selected_batter ) : 
    if active_tab != 'tab-batter' : 
        return "" 
    if selected_batter == None : 
        selected_batter = "V Kohli"
    fig = plot_runs_scored_against_teams(match_data=match_data , ball_data = ball_data , batter=selected_batter , season = selected_year ) 
    return dcc.Graph(figure=fig )


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
    if selected_batter == None : 
        selected_batter = "V Kohli"
    fig = plot_runs_distribution(match_data , ball_data , batter = selected_batter , season = selected_year) 
    return html.Div([
        dcc.Graph(figure=fig)
    ])



@app.callback(
    Output('runs-scored-by-over-type' , 'children'),
    [
        Input('tabs' , 'value'),
        Input('year-dropdown' , 'value') ,
        Input('batsman-dropdown' , 'value') ,
        
    ]
)
def update_runs_scored_by_over_type( active_tab , selected_year , selected_batter ) : 
    if active_tab != 'tab-batter':
        return "" 
    if selected_batter == None : 
        selected_batter = "V Kohli"
    fig = runs_scored_by_over_type(match_data=match_data, ball_data=ball_data , batter=selected_batter , season=selected_year)
    return dcc.Graph(figure = fig )

@app.callback(
    Output('plot-runs-heatmap-batter','children') ,
    [
        Input('tabs' , 'value') ,
        Input('year-dropdown' , 'value') , 
        Input('batsman-dropdown' , 'value')
    ]
)
def updaate_plot_runs_heatmap_batter(active_tab , selected_year , selected_batter ) : 
    if active_tab != 'tab-batter' : 
        return ""
    if selected_batter == None : 
        selected_batter = "V Kohli"
    fig = runs_heatmap_for_batter(match_data=match_data, ball_data= ball_data , batter= selected_batter , season = selected_year)
    return dcc.Graph(figure= fig )

@app.callback(
    Output('bowler-wickets' , 'children') , 
    [
        Input('tabs' , 'value' ) , 
        Input('year-dropdown' , 'value') , 
        Input('bowler-dropdown' , 'value')
    ]
)
def update_bowler_wickets(active_tab , selected_year , selected_bowler ) : 
    if active_tab != 'tab-bowler' :
        return ""
    data = get_bowler_wickets(match_data=match_data , ball_data = ball_data , bowler=selected_bowler , season = selected_year)
    return html.H4(f"{data['total_wickets']}", style={'font-size': '22px', 'font-weight': 'bold'})



@app.callback(
    Output('bowler-average' , 'children') , 
    [
        Input('tabs' , 'value' ) , 
        Input('year-dropdown' , 'value') , 
        Input('bowler-dropdown' , 'value')
    ]
)
def update_bowler_wickets(active_tab , selected_year , selected_bowler ) : 
    if active_tab != 'tab-bowler' :
        return ""
    data = get_bowler_wickets(match_data=match_data , ball_data = ball_data , bowler=selected_bowler , season = selected_year)
    return html.H4(f"{data['average']}", style={'font-size': '22px', 'font-weight': 'bold'})


@app.callback(
    Output('bowler-economy-rate' , 'children') , 
    [
        Input('tabs' , 'value' ) , 
        Input('year-dropdown' , 'value') , 
        Input('bowler-dropdown' , 'value')
    ]
)
def update_bowler_wickets(active_tab , selected_year , selected_bowler ) : 
    if active_tab != 'tab-bowler' :
        return ""
    data = get_bowler_wickets(match_data=match_data , ball_data = ball_data , bowler=selected_bowler , season = selected_year)
    return html.H4(f"{data['economy_rate']}", style={'font-size': '22px', 'font-weight': 'bold'})



@app.callback(
    Output('bowler-strike-rate' , 'children') , 
    [
        Input('tabs' , 'value' ) , 
        Input('year-dropdown' , 'value') , 
        Input('bowler-dropdown' , 'value')
    ]
)
def update_bowler_wickets(active_tab , selected_year , selected_bowler ) : 
    if active_tab != 'tab-bowler' :
        return ""
    data = get_bowler_wickets(match_data=match_data , ball_data = ball_data , bowler=selected_bowler , season = selected_year)
    return html.H4(f"{data['strike_rate']}", style={'font-size': '22px', 'font-weight': 'bold'})


@app.callback(
    Output('bowler-matches' , 'children') , 
    [
        Input('tabs' , 'value' ) , 
        Input('year-dropdown' , 'value') , 
        Input('bowler-dropdown' , 'value')
    ]
)
def update_bowler_wickets(active_tab , selected_year , selected_bowler ) : 
    if active_tab != 'tab-bowler' :
        return ""
    data = get_bowler_wickets(match_data=match_data , ball_data = ball_data , bowler=selected_bowler , season = selected_year)
    return html.H4(f"{data['matches']}", style={'font-size': '22px', 'font-weight': 'bold'})




@app.callback(
    Output('runs-given' , 'children') , 
    [
        Input('tabs' , 'value' ) , 
        Input('year-dropdown' , 'value') , 
        Input('bowler-dropdown' , 'value')
    ]
)
def update_bowler_wickets(active_tab , selected_year , selected_bowler ) : 
    if active_tab != 'tab-bowler' :
        return ""
    data = get_bowler_wickets(match_data=match_data , ball_data = ball_data , bowler=selected_bowler , season = selected_year)
    return html.H4(f"{data['total_runs_given']}", style={'font-size': '22px', 'font-weight': 'bold'})


@app.callback(
    Output('bowling-distribution' , 'children') , 
    [
        Input('tabs' , 'value' ) , 
        Input('year-dropdown' , 'value') , 
        Input('bowler-dropdown' , 'value')
    ]
)
def update_wickets_taken_by_over_type( active_tab , selected_year , selected_bowler) : 
    if active_tab != 'tab-bowler' : 
        return "" 
    fig = plot_wickets_dot_4s_6s(match_data= match_data , ball_data= ball_data , bowler=selected_bowler , season=selected_year)
    return dcc.Graph(figure=fig) 



@app.callback(
    Output('wickets-taken-by-over-type' , 'children') , 
    [
        Input('tabs' , 'value' ) , 
        Input('year-dropdown' , 'value') , 
        Input('bowler-dropdown' , 'value')
    ]
)
def update_wickets_taken_by_over_type( active_tab , selected_year , selected_bowler) : 
    if active_tab != 'tab-bowler' : 
        return "" 
    fig = wickets_taken_by_over_type(match_data= match_data , ball_data= ball_data , bowler=selected_bowler , season=selected_year)
    return dcc.Graph(figure=fig) 


@app.callback(
    Output('plot-bowler-wickets' , 'children') , 
    [
        Input('tabs' , 'value' ) , 
        Input('year-dropdown' , 'value') , 
        Input('bowler-dropdown' , 'value')      
    ]
)
def update_wickets_taken_by_over_type( active_tab , selected_year , selected_bowler) : 
    if active_tab != 'tab-bowler' : 
        return "" 
    fig = plot_bowler_wickets(match_data= match_data , ball_data= ball_data , bowler=selected_bowler , season=selected_year)
    return dcc.Graph(figure=fig) 



@app.callback(
    Output('plot-bowler-most-beaten-by-batsman' , 'children') , 
    [
        Input('tabs' , 'value' ) , 
        Input('year-dropdown' , 'value') , 
        Input('bowler-dropdown' , 'value')
    ]
)
def update_wickets_taken_by_over_type( active_tab , selected_year , selected_bowler) : 
    if active_tab != 'tab-bowler' : 
        return "" 
    fig = plot_bowler_most_beaten_by_batsman(match_data= match_data , ball_data= ball_data , bowler=selected_bowler , season=selected_year)
    return dcc.Graph(figure=fig) 



if __name__ == '__main__':
    app.run_server(debug=False ,)


