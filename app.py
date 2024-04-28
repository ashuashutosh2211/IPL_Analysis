# Import necessary libraries
from dash import Dash, dcc, html, Input, Output
import dash
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
import preprocess_match_data
import match_data_info
from match_data_info import get_most_time_winner, get_all_teams , get_winner , get_stats , get_scores_data , get_top_batsman , get_top_bowlers 
from match_data_plots import plot_match_won_by_toss_decision, plot_team_performance, plot_percentage_matches_won_and_lost_by_teams, best_batsmen , plot_top_5_batsmen, top_bowlers, plot_top_5_bowlers ,plot_stadium_matches_for_team 
import warnings 
import numpy as np
import json 
# Suppress warnings
warnings.filterwarnings("ignore")

# Load the data
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

# Initialize the Dash app with Bootstrap theme
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Define the layout
app.layout = html.Div([
    html.H1("IPL Analysis Dashboard", style={'textAlign': 'center'}),
    
    # Tabs for different sections
    dcc.Tabs(id='tabs', value='tab-home', children=[
        dcc.Tab(label='Home', value='tab-home'),
        dcc.Tab(label='Teams', value='tab-teams'),
        dcc.Tab(label="New" , value='tab-new')
        # Add more tabs here as needed
    ]),
    
    # Dropdown to select season
    html.Div([
        html.Label("Select Season"),
        dcc.Dropdown(
            id='year-dropdown',
            options=[
                {'label': str(year), 'value': year} for year in range(2008, 2023)
            ],
        )
    ], style={'width': '20%', 'display': 'inline-block', 'verticalAlign': 'top'}),
    
    # Placeholder for content update based on callback
    html.Div(id='tabs-content') , 
    
    html.Div(id='selected-season'),
    
   # Container for cards
    dbc.Row([
        # First column
        dbc.Col(html.Div(id='trophy-winner-info'),width = 3 ),
        
        # Second column
        dbc.Col(html.Div(id='orange-cap-winner-info'),width = 3 ),
        
        # Third column
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


    # Container for cards
    dbc.Row([
        # First column
        dbc.Col(html.Div(id='team-trophy-winner-info'),width = 3 ),
        
        # Second column
        dbc.Col(html.Div(id='team-most-runs'),width = 3 ),
        
        # Third column
        dbc.Col(html.Div(id='team-most-wickets'),width = 3 ) , 
        
        dbc.Col(html.Div(id = 'team-stats-info' ) , width = 3 )
    ]),
    dbc.Row([
        dbc.Col([
            html.Div(id='team-matches-by-toss-decision-plot'),
            
        ], width=3) , 
        # dbc.Col([
        #     html.Div(id='team-performance-plot'),
        # ], width = 5 ),
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
        
    ]),

])

# Update the callback for the "Home" tab to include the plot components
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
                # html.Div(id='team-selected-info')
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
                            html.Div(id='stadium-matches-plot'),
                        ])
                    ])
                ], width=8),
            ]),

        ])
    elif tab == 'tab-new':
        return html.Div([
            html.H4('New Tab'),
            html.P("This is a new tab. Add content here as needed.")
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


if __name__ == '__main__':
    app.run_server(debug=True)
