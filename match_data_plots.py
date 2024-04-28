import warnings 
import numpy as np 
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
import plotly.graph_objects as go
from collections import Counter

def get_mappings():
    team_names_dict = {
        "Chennai Super Kings": "CSK",
        "Mumbai Indians": "MI",
        "Royal Challengers Bangalore": "RCB",
        "Kolkata Knight Riders": "KKR",
        "Sunrisers Hyderabad": "SRH",
        "Rajasthan Royals": "RR",
        "Delhi Capitals": "DC",
        "Delhi Daredevils": "DD",
        "Deccan Chargers": "DCh",
        "Kings XI Punjab": "KXIP",
        "Gujarat Titans": "GT",
        "Rising Pune Supergiants": "RPS",
        "Lucknow Super Giants": "LSG",
        "Gujarat Lions": "GL",
        "Punjab Kings" : "PBKS",
        "Gujarat Titans" : "GT",
        "Pune Warriors" : "PW" , 
        "Kochi Tuskers Kerala" : "KTK"
    }

    reverse_team_mapping = {}
    for i in team_names_dict:
        reverse_team_mapping[team_names_dict[i]] = i 
    return team_names_dict , reverse_team_mapping

def plot_match_won_by_toss_decision(match_data, season=None, selected_team=None, venue=None):
    team_names_dict, reverse_team_mapping = get_mappings()
    temp_data = match_data.copy()
    
    if season is not None:
        temp_data = match_data[match_data['Season'] == season]
    if selected_team is not None:
        temp_data = temp_data[temp_data['TossWinner'] == selected_team]
    if venue is not None:
        temp_data = temp_data[temp_data['Venue'] == venue]
    
    field_wins = temp_data[temp_data['TossDecision'] == 'field']['WinningTeam'].count()
    bat_wins = temp_data[temp_data['TossDecision'] == 'bat']['WinningTeam'].count()

    labels = ['Field', 'Bat']
    values = [field_wins, bat_wins]

    hover_text = [f'Matches Won when Elected to Field: {field_wins}', f'Matches Won when Elected to Bat: {bat_wins}']

    # Define custom colors for 'Field' and 'Bat' segments
    colors = ['lightseagreen', 'blue']  # Blue for Field, Orange for Bat

    fig = go.Figure(go.Pie(labels=labels, values=values, title='', hovertext=hover_text, hoverinfo='label+text',
                           marker=dict(colors=colors)))
    fig.update_layout(width=320, height=350, legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5
    ))

    return fig
# Example usage
# fig = plot_match_won_by_toss_decision(match_data , selected_team = "Rajasthan Royals" , season = 2022 , venue = "Narendra Modi Stadium, Ahmedabad" )
# fig.show()


def plot_team_performance(match_data):
    team_names_dict , reverse_team_mapping = get_mappings()
    temp_data = match_data[match_data['MatchNumber'] == 'Final']
    final_teams = list(temp_data['Team1']) + list(temp_data['Team2']) 
    temp_data2 = match_data.copy()
    playoff_teams = [] 
    final_teams = []
    finals_won = list(temp_data2[temp_data2['MatchNumber'] == "Final"]['WinningTeam'])
    for i in range(2008, 2023):
        season_data = temp_data2[(temp_data2['Season'] == i)]
        season_data = season_data.reset_index(drop=True) 
        curr_season_playoffs = []
        for j in range(len(season_data)): 
            if len(season_data['MatchNumber'][j]) > 2: 
                curr_season_playoffs.append(season_data['Team1'][j]) 
                curr_season_playoffs.append(season_data['Team2'][j])
            if season_data['MatchNumber'][j] == "Final": 
                final_teams.append(season_data['Team1'][j])
                final_teams.append(season_data['Team2'][j]) 
            
        curr_season_playoffs = list(set(curr_season_playoffs))
        playoff_teams.extend(curr_season_playoffs)
    team_counts = {}
    for team in playoff_teams:
        if team not in team_counts:
            team_counts[team] = {'Playoffs': playoff_teams.count(team), 'Finals': final_teams.count(team), 'Wins': finals_won.count(team)}
    
    # Sort teams based on playoffs, finals, and wins counts
    sorted_teams = sorted(team_counts.items(), key=lambda x: (x[1]['Playoffs'], x[1]['Finals'], x[1]['Wins']),)
    team_names = [team_names_dict[team[0]] for team in sorted_teams]
    playoff_counts = [team[1]['Playoffs'] for team in sorted_teams]
    finals_counts = [team[1]['Finals'] for team in sorted_teams]
    wins_counts = [team[1]['Wins'] for team in sorted_teams]
    
    # Create custom hover text for each bar
    hover_text = [f"{reverse_team_mapping[team]} ({team})<br>Playoffs: {playoff}<br>Finals: {finals}<br>Titles: {wins}" for team, playoff, finals, wins in zip(team_names, playoff_counts, finals_counts, wins_counts)]
    
    # Create traces for each stack
    playoffs_trace = go.Bar(y=team_names, x=playoff_counts, name='Playoffs', orientation='h', hoverinfo='text', hovertext=hover_text)
    finals_trace = go.Bar(y=team_names, x=finals_counts, name='Finals', orientation='h', hoverinfo='text', hovertext=hover_text)
    wins_trace = go.Bar(y=team_names, x=wins_counts, name='Titles Won', orientation='h', hoverinfo='text', hovertext=hover_text)
    
    # Create layout
    layout = go.Layout( barmode='group', xaxis_title='Count', width=500, height=400 , legend=dict(
                            orientation="h",
                            yanchor="top",
                            y=1.15,
                            xanchor="center",
                            x=0.5
                        ))
    
    # Create figure
    fig = go.Figure(data=[wins_trace, finals_trace, playoffs_trace], layout=layout)
    return fig

# fig = plot_team_performance(match_data)
# fig.show()


def plot_percentage_matches_won_and_lost_by_teams(match_data, season=None):
    team_names_dict , reverse_team_mapping = get_mappings()
    temp_data = match_data.copy() 
    if season is not None: 
        temp_data = temp_data[temp_data['Season'] == season]
    temp_data = temp_data.dropna(subset=['WinningTeam'])
    
    winning_teams_count = dict(Counter(temp_data['WinningTeam']))
    total_team_matches = {} 
    for i in winning_teams_count:
        total_team_matches[i] = len(temp_data[temp_data['Team1'] == i]) + len(temp_data[temp_data['Team2'] == i])
    
    # Calculate losses for each team
    losing_teams_count = {}
    for team, total_matches in total_team_matches.items():
        if team not in winning_teams_count:
            losing_teams_count[team] = total_matches
        else:
            losing_teams_count[team] = total_matches - winning_teams_count[team]
    
    # Replace original team names with mapped names
    mapped_teams = [team_names_dict[team] for team in winning_teams_count.keys()]
    
    sorted_teams = sorted(zip(mapped_teams, winning_teams_count.values(), losing_teams_count.values()), key=lambda x: x[1])[::-1][:10][::-1]
    
    teams = [team[0] for team in sorted_teams]
    wins = [team[1] for team in sorted_teams]
    losses = [team[2] for team in sorted_teams]
    total_matches = [wins[i] + losses[i] for i in range(len(teams))]
    win_percentages = [round((wins[i] / total_matches[i]) * 100, 2) for i in range(len(teams))]
    loss_percentages = [round((losses[i] / total_matches[i]) * 100, 2) for i in range(len(teams))]
    hover_text = [f'Team: {reverse_team_mapping[team]}<br>Wins: {win} ({win_percent}%)<br>Losses: {loss}({loss_percent}%)' for team, win , win_percent, loss, loss_percent   in zip(teams, wins , win_percentages, losses ,  loss_percentages)]

    # Create stacked bar chart
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=win_percentages,
        y=teams,
        orientation='h',
        name='Wins',
        hovertext=hover_text,  
        text=[f'{wp}%' for wp in win_percentages],  # Text to display within each bar for wins
        textposition='inside',
        hoverinfo='text',  
        marker=dict(color='skyblue', line=dict(color='navy', width=1.5))  
    ))
    fig.add_trace(go.Bar(
        x=loss_percentages,
        y=teams,
        orientation='h',
        name='Losses',
        hovertext=hover_text,  text=[f'{lp}%' for lp in loss_percentages],  # Text to display within each bar for losses
        textposition='inside',
        hoverinfo='text',  
        marker=dict(color='salmon', line=dict(color='maroon', width=1.5))  
    ))
    
    fig.update_layout(
                      barmode='stack',
                      xaxis_title='Percentage of Matches',
                      yaxis_title='Team',
                      yaxis=dict(automargin=True), width=400, height=400, 
                       legend=dict(
                            orientation="h",
                            yanchor="top",
                            y=1.15,
                            xanchor="center",
                            x=0.5
                        )
                      )
    return fig

# fig = plot_percentage_matches_won_and_lost_by_teams(match_data , season = 2020 )
# fig.show()


## TOP 5 BATSMAN PLOT
def best_batsmen(ball_data, match_data, team_name, season=None):
    team_data = ball_data[ball_data['BattingTeam'] == team_name].reset_index(drop=True)
    
    team_data = team_data.merge(match_data[['ID', 'Season']], on='ID', how='left')
    
    if season is not None:
        team_data = team_data[team_data['Season'] == season]

    player_total_runs = team_data.groupby('batter')['batsman_run'].sum().reset_index()    
    player_total_runs = player_total_runs.sort_values(by='batsman_run', ascending=False)
    player_total_runs = player_total_runs.reset_index( drop = True ) [0 : 10 ]
    return player_total_runs

def plot_top_5_batsmen(batsmen_data):
    fig = go.Figure(go.Bar(
        x=batsmen_data['batsman_run'],
        y=batsmen_data['batter'],
        orientation='h',
        marker_color='skyblue'
    ))
    fig.update_layout(
        title='',
        xaxis_title='Total Runs',
        yaxis_title='Batsmen',
        yaxis_categoryorder='total ascending' 
    )
    return fig 


## TOP 5 BOWLER PLOT 


def top_bowlers(ball_data, match_data, team_name, season=None):
    ball_data = ball_data.merge(match_data[['ID', 'Season', 'Team1', 'Team2']], on='ID', how='left')
    ball_data['BowlingTeam'] = np.where(ball_data['BattingTeam'] != ball_data['Team1'], ball_data['Team1'], ball_data['Team2'])
    if season is not None:
        ball_data = ball_data[ball_data['Season'] == season]
    team_data = ball_data[ball_data['BowlingTeam'] == team_name]
    bowler_wickets = team_data.groupby('bowler')['isWicketDelivery'].sum().reset_index()
    bowler_wickets = bowler_wickets.sort_values(by='isWicketDelivery', ascending=False)
    top_5_bowlers = bowler_wickets.head(10)
    return top_5_bowlers

def plot_top_5_bowlers(bowlers_data):
    fig = go.Figure(go.Bar(
        x=bowlers_data['isWicketDelivery'],
        y=bowlers_data['bowler'],
        orientation='h',
        marker_color='skyblue'
    ))
    fig.update_layout(
        title='',
        xaxis_title='Total Wickets',
        yaxis_title='Bowlers',
        yaxis_categoryorder='total ascending' 
    )
    return fig 

# bowlers_data = top_bowlers(ball_data, match_data, "Royal Challengers Bangalore")
# fig = plot_top_5_bowlers(bowlers_data)
# fig.show()



def filter_data(match_data , selected_team , season = None ):
    temp_data = match_data.copy() 
    if season != None : 
        temp_data = temp_data[temp_data['Season'] == season ]
    filtered_data = temp_data[(temp_data['Team1'] == selected_team) | (temp_data['Team2'] == selected_team)]
    return filtered_data

def plot_stadium_matches_for_team(match_data , selected_team, season = None , top_n=10):
    filtered_data = filter_data(match_data , selected_team , season = season )
    
    # Count matches won and lost by each stadium
    stadium_stats = filtered_data.groupby('Venue')['WinningTeam'].value_counts().unstack(fill_value=0)
    stadium_stats['MatchesLost'] = stadium_stats.sum(axis=1) - stadium_stats.get(selected_team, 0)
    stadium_stats['MatchesWon'] = stadium_stats.get(selected_team, 0)
    
    # Calculate percentages
    stadium_stats['MatchesWonPercentage'] = (stadium_stats['MatchesWon'] / (stadium_stats['MatchesWon'] + stadium_stats['MatchesLost'])) * 100
    stadium_stats['MatchesLostPercentage'] = (stadium_stats['MatchesLost'] / (stadium_stats['MatchesWon'] + stadium_stats['MatchesLost'])) * 100
    
    # Sort stadiums based on total matches played
    stadium_stats['TotalMatches'] = stadium_stats['MatchesWon'] + stadium_stats['MatchesLost']
    stadium_stats = stadium_stats.sort_values(by='TotalMatches', ascending=False).head(top_n)
    stadium_stats = stadium_stats[::-1]
    
    # Create custom hover text
    hover_text = [f'Total Matches: {total}<br>Matches Won: {won}<br>Matches Lost: {lost}' 
                  for total, won, lost in zip(stadium_stats['TotalMatches'], 
                                              stadium_stats['MatchesWon'], 
                                              stadium_stats['MatchesLost'])]
    
    # Plotting using Plotly
    fig = go.Figure(data=[
        go.Bar(name='Matches Won %', y=stadium_stats.index, x=stadium_stats['MatchesWonPercentage'], 
               orientation='h', hovertext=hover_text),
        go.Bar(name='Matches Lost %', y=stadium_stats.index, x=stadium_stats['MatchesLostPercentage'], 
               orientation='h', hovertext=hover_text)
    ])
    
    fig.update_layout(
        title=f'Stadium-wise Matches Won vs Lost for {selected_team}',
        yaxis=dict(title='Stadium'),
        xaxis=dict(title='Percentage of Matches'),
        barmode='stack',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.1,
            xanchor="center",
            x=0.5
        ),
        width = 800 , height = 400 
    )
    return fig
    

# # Example usage
# selected_team = "Royal Challengers Bangalore"
# plot_stadium_matches_for_team(selected_team)

def plot_match_won_by_toss_decision(match_data, season=None, selected_team=None, venue=None):
    team_names_dict, reverse_team_mapping = get_mappings()
    temp_data = match_data.copy()
    
    if season is not None:
        temp_data = match_data[match_data['Season'] == season]
    if selected_team is not None:
        temp_data = temp_data[temp_data['TossWinner'] == selected_team]
    if venue is not None:
        temp_data = temp_data[temp_data['Venue'] == venue]
    
    field_wins = temp_data[temp_data['TossDecision'] == 'field']['WinningTeam'].count()
    bat_wins = temp_data[temp_data['TossDecision'] == 'bat']['WinningTeam'].count()

    labels = ['Field', 'Bat']
    values = [field_wins, bat_wins]

    hover_text = [f'Matches Won when Elected to Field: {field_wins}', f'Matches Won when Elected to Bat: {bat_wins}']

    colors = ['lightseagreen', 'blue'] 

    fig = go.Figure(go.Pie(labels=labels, values=values, title='', hovertext=hover_text, hoverinfo='label+text',
                           marker=dict(colors=colors)))
    fig.update_layout(width=320, height=350, legend=dict(
        orientation="h",
        yanchor="bottom",
        y=-0.2,
        xanchor="center",
        x=0.5
    ))
    return fig
# fig = plot_match_won_by_toss_decision(match_data ,  selected_team = "Rajasthan Royals" )