import warnings 
import numpy as np 
import plotly.express as px
import pandas as pd
import matplotlib.pyplot as plt
warnings.filterwarnings("ignore")
import plotly.graph_objects as go
from collections import Counter
import plotly.io as pio

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
    fig.update_layout(width=400, height=400, legend=dict(
                            orientation="h",
                            yanchor="top",
                            y=1.25,
                            xanchor="center",
                            x=0.5
                        ))
    fig.show()
    # return fig
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
    layout = go.Layout( barmode='group', xaxis_title='Count', width=700, height=400 , legend=dict(
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
        marker=dict(color='lightseagreen', line=dict(color='black', width=1.5))  
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
                      yaxis=dict(automargin=True), width=700, height=400, 
                       legend=dict(
                            orientation="h",
                            yanchor="top",
                            y=1.15,
                            xanchor="center",
                            x=0.5
                        )
                      )
    return fig


## TOP 5 BATSMAN PLOT
def best_batsmen(ball_data, match_data, team, season=None):
    team_data = ball_data[ball_data['BattingTeam'] == team].reset_index(drop=True)
    
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
        marker=dict(color='lightseagreen', line=dict(color='black', width=1.5))  
    ))
    fig.update_layout(
        title='',
        xaxis_title='Total Runs',
        yaxis_title='Batsmen',
        yaxis_categoryorder='total ascending' 
    )
    return fig 


## TOP 5 BOWLER PLOT 


def top_bowlers(ball_data, match_data, team, season=None):
    ball_data = ball_data.merge(match_data[['ID', 'Season', 'Team1', 'Team2']], on='ID', how='left')
    ball_data['BowlingTeam'] = np.where(ball_data['BattingTeam'] != ball_data['Team1'], ball_data['Team1'], ball_data['Team2'])
    if season is not None:
        ball_data = ball_data[ball_data['Season'] == season]
    team_data = ball_data[ball_data['BowlingTeam'] == team]
    bowler_wickets = team_data.groupby('bowler')['isWicketDelivery'].sum().reset_index()
    bowler_wickets = bowler_wickets.sort_values(by='isWicketDelivery', ascending=False)
    top_5_bowlers = bowler_wickets.head(10)
    return top_5_bowlers

def plot_top_5_bowlers(bowlers_data):
    fig = go.Figure(go.Bar(
        x=bowlers_data['isWicketDelivery'],
        y=bowlers_data['bowler'],
        orientation='h',
        marker=dict(color='lightseagreen', line=dict(color='black', width=1.5))  
    ))
    fig.update_layout(
        title='',
        xaxis_title='Total Wickets',
        yaxis_title='Bowlers',
        yaxis_categoryorder='total ascending' , width = 600 
    )
    return fig 

# bowlers_data = top_bowlers(ball_data, match_data, "Royal Challengers Bangalore")
# fig = plot_top_5_bowlers(bowlers_data)
# fig.show()



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
    fig.update_layout(width=400, height=400, legend=dict(
        orientation="h",
        yanchor="top",
        y= 1.25 ,
        xanchor="center",
        x=0.5
    ))
    return fig
# fig = plot_match_won_by_toss_decision(match_data ,  selected_team = "Rajasthan Royals" )




def filter_data(match_data , selected_team , season = None ):
    temp_data = match_data.copy() 
    if season != None : 
        temp_data = temp_data[temp_data['Season'] == season ]
    filtered_data = temp_data[(temp_data['Team1'] == selected_team) | (temp_data['Team2'] == selected_team)]
    return filtered_data


def plot_stadium_matches_for_team(match_data, selected_team, season=None, top_n=10):
    filtered_data = filter_data(match_data, selected_team, season=season)
    
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
    
    # Create text for percentages on bars
    percentage_text = [f'{percentage:.1f}%' for percentage in stadium_stats['MatchesWonPercentage']]
    percentage_text_loss = [f'{(100 - percentage):.1f}%' for percentage in stadium_stats['MatchesWonPercentage']]
    # Plotting using Plotly
    fig = go.Figure(data=[
        go.Bar(name='Matches Won %', y=stadium_stats.index, x=stadium_stats['MatchesWonPercentage'], 
               orientation='h', hovertext=hover_text, text=percentage_text, 
               marker=dict(color='lightseagreen', line=dict(color='black', width=1.5))),
        go.Bar(name='Matches Lost %', y=stadium_stats.index, x=stadium_stats['MatchesLostPercentage'], 
               orientation='h', hovertext=hover_text, text=percentage_text_loss, 
               marker=dict(color='salmon', line=dict(color='maroon', width=1.5)))
    ])
    
    fig.update_layout(
        title=f'',
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
        width=800, height=400
    )
    return fig
    


def plot_matches_by_team( df , team , season = None ):
    team_names_dict , reverse_team_mapping = get_mappings()

    team_matches = df[(df['Team1'] == team) | (df['Team2'] == team)]
    if season != None : 
        team_matches = team_matches[team_matches['Season'] == season ]
    team_opponent_matches = team_matches[team_matches['Team2'] != team]
    # Count matches won and lost by the specified team against each opponent
    win_counts = team_opponent_matches[team_opponent_matches['WinningTeam'] == team]['Team2'].value_counts()
    loss_counts = team_opponent_matches[team_opponent_matches['WinningTeam'] != team]['Team2'].value_counts()

    # Create a Plotly stacked bar chart
    fig = go.Figure()

    # Add wins
    fig.add_trace(go.Bar(
       y=[team_names_dict[team] for team in win_counts.index],
        x=win_counts.values,
        name='Won',
        orientation='h',
        marker=dict(color='lightseagreen', line=dict(color='black', width=1.5))  ,
        hovertext=[f"{team} won {value} matches against {opponent}" for opponent, value in win_counts.items()]
    ))

    # Add losses
    fig.add_trace(go.Bar(
        y=[team_names_dict[team] for team in loss_counts.index],
        x=loss_counts.values,
        name='Lost',
        orientation='h',
        marker=dict(color='salmon', line=dict(color='maroon', width=1.5))  ,
        hovertext=[f"{team} lost {value} matches against {opponent}" for opponent, value in loss_counts.items()]
    ))

    fig.update_layout(
        title="",
        xaxis_title='Number of Matches',
        yaxis_title='Opponent Team',
        barmode='stack' , width = 500 , height = 400  , 
        legend=dict(
                orientation="h",
                yanchor="top",
                y=1.15,
                xanchor="center",
                x=0.5
            )
    )
    return fig 



def plot_batter_dismissals(match_data, ball_data, batter, season=None):
    ball_data = ball_data.merge(match_data[['ID', 'Season', 'Team1', 'Team2']], on='ID', how='left')
    ball_data['BowlingTeam'] = np.where(ball_data['BattingTeam'] != ball_data['Team1'], ball_data['Team1'], ball_data['Team2'])
    if season is not None:
        ball_data = ball_data[ball_data['Season'] == season] 
    ball_data = ball_data[ball_data['batter'] == batter].reset_index(drop=True)
    bowler_dismissal = {}
    for i in range(len(ball_data)):
        if ball_data['player_out'][i] == batter:
            bowler = ball_data['bowler'][i]
            if bowler in bowler_dismissal:
                bowler_dismissal[bowler] += 1
            else:
                bowler_dismissal[bowler] = 1 
    sorted_bowlers = dict(sorted(bowler_dismissal.items(), key=lambda item: item[1], reverse=True))
    
    # Get top 10 bowlers
    top_10_bowlers = dict(list(sorted_bowlers.items())[:10][::-1])
    
    # Extracting bowler names and dismissals
    bowler_names = list(top_10_bowlers.keys())
    dismissals = list(top_10_bowlers.values())
    
    # Plotting using Plotly
    fig = go.Figure(data=[go.Bar(x=dismissals, y=bowler_names, orientation='h',
                                 marker=dict(color='lightseagreen', line=dict(color='black', width=1.5)))])
    fig.update_layout(title='',
                      xaxis_title='Number of Dismissals',
                      yaxis_title='Bowler' , width = 600 , height = 400 )
    return fig
def plot_season_wise_runs(match_data, ball_data, batter, season=None):
    ball_data = ball_data.merge(match_data[['ID', 'Season', 'Team1', 'Team2']], on='ID', how='left')
    ball_data['BowlingTeam'] = np.where(ball_data['BattingTeam'] != ball_data['Team1'], ball_data['Team1'], ball_data['Team2'])
    ball_data = ball_data[ball_data['batter'] == batter].reset_index(drop=True)

    if season is None:
        seasons = [i for i in range(2008, 2023)]
        season_wise_runs = {}

        for season in seasons:
            season_wise_runs[str(season)] = sum(ball_data[ball_data['Season'] == season]['batsman_run'])

        years = list(season_wise_runs.keys())
        runs = list(season_wise_runs.values())

        fig = go.Figure(data=go.Bar(x=runs, y=years, orientation='h', text=runs, hoverinfo='text', marker=dict(color='lightseagreen', line=dict(color='black', width=1.5))))

        fig.update_layout(title='',
                          xaxis_title='Runs',
                          yaxis_title='Year',
                          width=500, height=700)
        return fig
    else:
        ball_data = ball_data[ball_data['Season'] == season]
        matches = ball_data['ID'].unique()
        batting_team = ball_data[ball_data['batter'] == batter]['BattingTeam'].reset_index(drop=True)[0]
        matches_runs = {}
        htexts = {}
        for match in matches:
            matches_runs[str(match)] = sum(ball_data[ball_data['ID'] == match]['batsman_run'])
            team1 = match_data[match_data['ID'] == match ]['Team1'].item()
            team2 = match_data[match_data['ID'] == match ]['Team2'].item()
            opposite_team = team1 
            if team1 == batting_team : 
                opposite_team = team2 
            htexts[str(match)] = f"Batsman Team : {batting_team} <br> Opposite Team : {opposite_team} <br> Runs : {matches_runs[str(match)]}"
        
        runs = list(matches_runs.values())

        fig = go.Figure(data=go.Bar(y=[str(i+1)for i in range(len(runs))], x=runs, orientation='h', hovertext=list(htexts.values()), hoverinfo='text', marker=dict(color='lightseagreen', line=dict(color='black', width=1.5))))

        fig.update_layout(title='',
                          xaxis_title='Runs',
                          yaxis_title='Match number',
                          width=600, height=700 , )
        return fig


def stadium_wise_runs(match_data, ball_data, batter, season=None):
    ball_data = ball_data.merge(match_data[['ID', 'Season', 'Team1', 'Team2', 'Venue']], on='ID', how='left')
    ball_data['BowlingTeam'] = np.where(ball_data['BattingTeam'] != ball_data['Team1'], ball_data['Team1'], ball_data['Team2'])
    
    if season is not None:
        ball_data = ball_data[ball_data['Season'] == season] 
    
    ball_data = ball_data[ball_data['batter'] == batter].reset_index(drop=True)
    
    total_batsman_run = ball_data.groupby('Venue')['batsman_run'].sum().reset_index()
    
    total_batsman_run = total_batsman_run.sort_values(by='batsman_run', ascending=False).head(20)[::-1]  
    
    fig = go.Figure(go.Bar(
        x=total_batsman_run['batsman_run'],
        y=total_batsman_run['Venue'],
        orientation='h',
        marker=dict(color='lightseagreen', line=dict(color='black', width=1))
    ))
    
    fig.update_layout(
        title='',
        xaxis_title='Total Runs',
        yaxis_title='Venue',
        width=700,
        height=600
    )
    
    return fig

def plot_runs_scored_against_bowlers(match_data, ball_data, batter, season=None):
    ball_data = ball_data.merge(match_data[['ID', 'Season', 'Team1', 'Team2']], on='ID', how='left')
    ball_data['BowlingTeam'] = np.where(ball_data['BattingTeam'] != ball_data['Team1'], ball_data['Team1'], ball_data['Team2'])
    if season is not None:
        ball_data = ball_data[ball_data['Season'] == season] 
    ball_data = ball_data[ball_data['batter'] == batter].reset_index(drop=True)
    
    bowler_runs = {}
    for i in range(len(ball_data)):
        bowler = ball_data['bowler'][i]
        runs = ball_data['batsman_run'][i]
        if bowler in bowler_runs:
            bowler_runs[bowler] += runs
        else:
            bowler_runs[bowler] = runs
    
    top_10_bowlers = dict(sorted(bowler_runs.items(), key=lambda item: item[1], reverse=True)[:10][::-1])
    
    bowler_names = list(top_10_bowlers.keys())
    runs_scored = list(top_10_bowlers.values())
    
    fig = go.Figure(data=[go.Bar(x=runs_scored, y=bowler_names, orientation='h',
                                 marker=dict(color='lightseagreen', line=dict(color='black', width=1.5)))])
    fig.update_layout(title='',
                      xaxis_title='Runs Scored',
                      yaxis_title='Bowler', 
                      width=600, height=400)
    return fig




def plot_season_wise_violin_plot(match_data, ball_data, batter):
    ball_data = ball_data.merge(match_data[['ID', 'Season', 'Team1', 'Team2']], on='ID', how='left')
    ball_data['BowlingTeam'] = np.where(ball_data['BattingTeam'] != ball_data['Team1'], ball_data['Team1'], ball_data['Team2'])
    ball_data = ball_data[ball_data['batter'] == batter].reset_index(drop=True)
    seasons = [i for i in range(2008, 2023)] 
    season_wise_runs = {} 

    for season in seasons: 
        season_wise_runs[season] = []
        matches = ball_data[(ball_data['Season'] == season)]['ID'].unique() 
        for match in matches: 
            runs = sum(ball_data[(ball_data['Season'] == season) & (ball_data['ID'] == match)]['batsman_run'])
            season_wise_runs[season].append(runs)
    
    years = list(season_wise_runs.keys())
    values = list(season_wise_runs.values())
    
    traces = []
    
    for i, year in enumerate(years):
        trace = go.Violin(y=values[i], name=str(year), box_visible=False, meanline_visible=True, line_color='salmon', showlegend=False)
        traces.append(trace)
    
    layout = go.Layout(title="", yaxis=dict(title="Values") , width=600 , height=400 )
    fig = go.Figure(data=traces, layout=layout)
    return fig
def get_batter_runs( match_data , ball_data , batter , season = None ) : 
    ball_data = ball_data.merge(match_data[['ID', 'Season', 'Team1', 'Team2']], on='ID', how='left')
    ball_data['BowlingTeam'] = np.where(ball_data['BattingTeam'] != ball_data['Team1'], ball_data['Team1'], ball_data['Team2'])
    if season != None :
        ball_data = ball_data[ball_data['Season'] == season ] 
    ball_data = ball_data[ball_data['batter'] == batter ].reset_index(drop = True )
    total_runs = 0 
    fours = 0 
    sixes = 0 
    dot_balls = 0 
    dismissals = 0 
    matches = len(ball_data['ID'].unique())
    balls = 0 
    run_123 = 0 
    for i in range(len(ball_data)): 
        total_runs += ball_data['batsman_run'][i] 
        fours += ball_data['batsman_run'][i] == 4 
        sixes += ball_data['batsman_run'][i] == 6
        dismissals += ball_data['player_out'][i] == batter 
        balls += 1 
        dot_balls += ball_data['batsman_run'][i] == 0 
        if ball_data['batsman_run'][i] > 0 and ball_data['batsman_run'][i] < 4 : 
            run_123 += 1
    strike_rate = '-'
    if balls != 0 : 
        strike_rate = round ((total_runs * 100 )/balls , 2 )
    average = 'inf'
    if dismissals != 0 : 
        average = total_runs/dismissals
    
    fifties = 0 
    hundreds = 0 
    
    match_runs = {} 
    match_ids = list(ball_data['ID'].unique()) 
    for match_id in match_ids : 
        match_runs[match_id] = sum(ball_data[ball_data['ID'] == match_id]['batsman_run']) 
        if match_runs[match_id] >= 100 : 
            hundreds += 1 
        elif match_runs[match_id] >= 50 : 
            fifties += 1 
    data = {
        'total_runs' : total_runs , 
        'fours' : fours , 
        'sixes' : sixes , 
        'strike_rate' : strike_rate , 
        'dismissals' : dismissals , 
        'balls' : balls , 
        'matches' : matches , 
        'hundreds' : hundreds , 
        'fifties' : fifties ,
        'average' : average , 
        'dot_balls' : dot_balls,
        'run123' : run_123
    }
    return data


def plot_runs_distribution( match_data , ball_data , batter , season = None ):
    batter_data = get_batter_runs( match_data , ball_data , batter , season = season )
    # Data for pie chart
    labels = ['4s', '6s', '1s, 2s, 3s', 'Dot balls']
    sizes = [batter_data['fours'], batter_data['sixes'], batter_data['run123'], batter_data['dot_balls']]

    # Create pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=sizes, hole=.3)])

    # Update layout
    fig.update_layout(
        title='',
        width=600,
        height=400,
        legend=dict(orientation="h", y=1.2 , x = 0.5 ,
        xanchor="center",  ) 
    )
    return fig



def team_toss_outcomes_bar_chart(match_data, season=None):
    if season is not None:
        match_data = match_data[match_data['Season'] == season]

    # Count the number of times each team has won and lost the toss
    toss_outcomes = match_data.groupby('TossWinner')['toss_winner_wins_match'].value_counts().unstack(fill_value=0)

    mapping, _ = get_mappings()
    teams = mapping.keys()
    won = {}
    lost = {}
    for i in teams:
        won[i] = len(match_data[match_data['TossWinner'] == i])
        lost[i] = len(match_data[match_data['Team1'] == i]) + len(match_data[match_data['Team2'] == i]) - won[i]
        if won[i] == 0 and lost[i] == 0:
            del won[i]
            del lost[i]
    teams = list(won.keys())
    matches_won = [won[team] for team in teams]
    matches_lost = [lost[team] for team in teams]

    # Calculate total matches played
    total_matches = [won[team] + lost[team] for team in teams]

    # Calculate percentages
    percent_won = [mw / tm * 100 for mw, tm in zip(matches_won, total_matches)]
    percent_lost = [ml / tm * 100 for ml, tm in zip(matches_lost, total_matches)]

    # Sort data based on total matches played
    sorted_indices = sorted(range(len(total_matches)), key=lambda k: total_matches[k])
    teams_sorted = [teams[i] for i in sorted_indices]
    percent_won_sorted = [percent_won[i] for i in sorted_indices]
    percent_lost_sorted = [percent_lost[i] for i in sorted_indices]

    # Create hover text
    hover_text = [f'Team: {team}<br>Tosses Won: {won}<br>Tosses Lost: {lost}' for team, won, lost in zip(teams_sorted, matches_won, matches_lost)]

    # Plot
    fig = go.Figure(data=[
        go.Bar(name='Toss Wins', y=teams_sorted, x=percent_won_sorted, orientation='h', marker=dict(color='lightseagreen', line=dict(color='black', width=1)),
               hoverinfo='text', text=[f'{p:.2f}%' for p in percent_won_sorted], textposition='auto', hovertext=hover_text),
        go.Bar(name='Toss Losses', y=teams_sorted, x=percent_lost_sorted, orientation='h', marker=dict(color='salmon', line=dict(color='maroon', width=1)),
               hoverinfo='text', text=[f'{p:.2f}%' for p in percent_lost_sorted], textposition='auto', hovertext=hover_text)
    ])

    fig.update_layout(
        barmode='stack',
        title='Toss Wins and Losses Percentage by Team',
        xaxis_title='Percentage', width=500, height=500,
        yaxis=dict(
            title='Teams',
            tickvals=list(range(len(teams_sorted))),
            ticktext=[mapping[team] for team in teams_sorted]
        ),
        legend=dict(
            orientation="h",
            yanchor="top",
            y=1.15,
            xanchor="center",
            x=0.5
        )
    )

    return fig 

def toss_winner_match_wins_pie(match_data, team = None , season=None):
    if season is not None:
        match_data = match_data[match_data['Season'] == season]
    if team is not None : 
        match_data = match_data[match_data['WinningTeam'] == team ] 
    if team == None : 
        match_data['toss_winner_wins_match'] = match_data['TossWinner'] == match_data['WinningTeam']
    else:
        match_data['toss_winner_wins_match'] = match_data['TossWinner'] == team
    match_data = match_data.reset_index(drop=True)
    for i in range(len(match_data)):
        if match_data['toss_winner_wins_match'][i]:
            match_data['toss_winner_wins_match'][i] = "Won"
        else:
            match_data['toss_winner_wins_match'][i] = "Lost"
    field_wins = len(match_data[match_data['toss_winner_wins_match'] == 'Won'])
    bat_wins = len(match_data[match_data['toss_winner_wins_match'] == 'Lost'])

    labels = ['Won', 'Lost']
    values = [field_wins, bat_wins]
    
    hover_text = [f'Matches won when lost the toss: {field_wins}', f'Matches lost when won the toss: {bat_wins}']
    
    colors = ['lightseagreen', 'salmon']

    fig = go.Figure(go.Pie(labels=labels, values=values, title='', hovertext=hover_text, hoverinfo='label+text', 
                           marker=dict(colors=colors)))
    fig.update_layout(width=400, height=400, legend=dict(
                            orientation="h",
                            yanchor="top",
                            y=1.25,
                            xanchor="center",
                            x=0.5
                        ))
    
    return fig


def run_rate(ball_data , match_data  , team , season = None ) : 
    ball_data = ball_data.merge(match_data[['ID', 'Season', 'Team1', 'Team2' , 'MatchNumber']], on='ID', how='left')
    ball_data['BowlingTeam'] = np.where(ball_data['BattingTeam'] != ball_data['Team1'], ball_data['Team1'], ball_data['Team2'])
    ball_data = ball_data[ball_data['MatchNumber'].str.len() < 3]
    if season is not None:
        ball_data = ball_data[ball_data['Season'] == season] 
    batting_data = ball_data[(ball_data['BattingTeam'] == team)]
    balls_played = len(batting_data) - len(batting_data[batting_data['extra_type'] == 'wides'])
    overs = balls_played/6
    batting_rate = sum(batting_data['total_run'])/overs

    bowling_data = ball_data[ball_data['BowlingTeam'] == team ] 
    balls_played = len(bowling_data) 
    overs = balls_played/6 
    bowling_rate = sum(bowling_data['total_run'])/overs
    return batting_rate - bowling_rate 
# run_rate(ball_data , match_data , team = "Royal Challengers Bangalore" , season = 2022 )



def plot_match_wins(match_data, ball_data, season=None):
    if season is not None:
        match_data = match_data[match_data['Season'] == season]

    wins_by_team = match_data['WinningTeam'].value_counts().reset_index()
    wins_by_team.columns = ['Team', 'Wins']

    # Calculate net run rate for each team
    net_run_rates = []
    for team in wins_by_team['Team']:
        net_run_rate = run_rate(ball_data, match_data, team, season=season)
        net_run_rates.append(net_run_rate)

    # Add net run rate to the DataFrame
    wins_by_team['NetRunRate'] = net_run_rates

    # Sort teams by wins and net run rate
    wins_by_team = wins_by_team.sort_values(by=['Wins', 'NetRunRate'], ascending=[True, True])

    # Assign colors to top 4 teams
    top_teams = wins_by_team.iloc[-4:]
    top_teams_colors = ['lightseagreen' if team in top_teams['Team'].values else 'salmon' for team in wins_by_team['Team']]

    # Create a bar trace
    trace = go.Bar(
        x=wins_by_team['Wins'],
        y=wins_by_team['Team'],  
        hovertemplate="Wins: %{x}<br>Net Run Rate: %{customdata}",  
        customdata=wins_by_team['NetRunRate'],  
        orientation='h',
        marker=dict(color=top_teams_colors, line=dict(color='black', width=1)) , name = "Teams"
    )

    # Define layout
    layout = go.Layout(
        title='',
        xaxis=dict(title='Number of Wins'),
        yaxis=dict(title='Teams'), width=600, height=400,
        hovermode='closest'  
    )

    fig = go.Figure(data=[trace], layout=layout)

    # Annotate bars for qualified teams
    for team, wins in zip(wins_by_team['Team'], wins_by_team['Wins']):
        if team in top_teams['Team'].values:
            fig.add_annotation(
                x=wins - 1.2, 
                y=team,
                text="Qualified",
                showarrow=False
            )
    return fig

# Example usage
# plot_match_wins(match_data, ball_data, season=2016)

# for plotting the wickets taken by over and balls by season 
def wicket_heatmap_for_team(match_data, ball_data, team = None , season=None):
    ball_data = ball_data.merge(match_data[['ID', 'Season', 'Team1', 'Team2']], on='ID', how='left')
    ball_data['BowlingTeam'] = np.where(ball_data['BattingTeam'] != ball_data['Team1'], ball_data['Team1'], ball_data['Team2'])
    
    if season is not None:
        ball_data = ball_data[ball_data['Season'] == season] 
    
    if team != None :
        ball_data = ball_data[ball_data['BowlingTeam'] == team].reset_index(drop=True)

    new_df = ball_data.groupby(['overs', 'ballnumber'])['isWicketDelivery'].sum().unstack(fill_value=0)
    new_df = new_df.reindex(index=range(20), columns=range(1, 7), fill_value=0)
    new_df.index = new_df.index.astype(str)
    new_df.columns = new_df.columns.astype(str)

    trace = go.Heatmap(
        z=new_df.values,
        x=new_df.columns,
        y=new_df.index,
        colorscale='YlGnBu',
        colorbar=dict(title='Wickets'),
        hovertemplate='Over Number: %{y}<br>Ball Number: %{x}<br>Wickets: %{z}' , 
        name = "wickets" , 
    )
    
    # Create layout
    layout = go.Layout(
        title='',
        xaxis=dict(title='Ball Number'),
        yaxis=dict(title='Overs'),
        width=600,
        height=700
    )
    
    # Create figure
    fig = go.Figure(data=[trace], layout=layout)
    return fig


def runs_heatmap_by_bowl_over( match_data , ball_data , team = None , season = None ) : 
    ball_data = ball_data.merge(match_data[['ID', 'Season', 'Team1', 'Team2']], on='ID', how='left')
    ball_data['BowlingTeam'] = np.where(ball_data['BattingTeam'] != ball_data['Team1'], ball_data['Team1'], ball_data['Team2'])
    if season is not None:
        ball_data = ball_data[ball_data['Season'] == season] 
    if team!= None : 
        ball_data = ball_data[ball_data['BattingTeam'] == team].reset_index(drop=True)
  
    new_df = ball_data.groupby(['overs', 'ballnumber'])['batsman_run'].sum().unstack(fill_value=0)
    
    new_df = new_df.reindex(index=range(20), columns=range(1, 7), fill_value=0)
    new_df.index = new_df.index.astype(str)
    new_df.columns = new_df.columns.astype(str)

    trace = go.Heatmap(
        z=new_df.values,
        x=new_df.columns,
        y=new_df.index,
        colorscale='YlGnBu',
        colorbar=dict(title='Runs') , 
        hovertemplate='Over Number: %{y}<br>Ball Number: %{x}<br>Runs: %{z}' ,
        name = "runs"
    )
    
    # Create layout
    layout = go.Layout(
        title='',
        xaxis=dict(title='Ball Number'),
        yaxis=dict(title='Overs') , width = 600 , height = 700
    )
    
    # Create figure
    fig = go.Figure(data=[trace], layout=layout)
    return fig
# runs_heatmap_by_bowl_over(match_data , ball_data  )



def average_vs_strike_rate( match_data , ball_data , team = None , season = None ) : 
    ball_data = ball_data.merge(match_data[['ID', 'Season', 'Team1', 'Team2']], on='ID', how='left')
    ball_data['BowlingTeam'] = np.where(ball_data['BattingTeam'] != ball_data['Team1'], ball_data['Team1'], ball_data['Team2'])
    if season is not None:
        ball_data = ball_data[ball_data['Season'] == season] 
    if team != None :
        ball_data = ball_data[ball_data['BattingTeam'] == team].reset_index(drop=True)
    batsman_stats = ball_data.groupby('batter').agg(
        runs=('batsman_run', 'sum'),  
        balls_played=('batter', 'count'),  
        dismissals=('player_out', lambda x: x.notna().sum())  
    ).reset_index()
    if season == None : 
        batsman_stats = batsman_stats[(batsman_stats['dismissals'] != 0) & (batsman_stats['balls_played'] >= 150)]
    
    batsman_stats = batsman_stats[(batsman_stats['dismissals'] != 0)]
    batsman_stats = batsman_stats.reset_index( drop = True )
    batsman_stats['average'] = ((batsman_stats['runs'])/batsman_stats['dismissals'] )
    batsman_stats['strike_rate'] = ((batsman_stats['runs'] * 100)/batsman_stats['balls_played'] )
    fig = px.scatter(batsman_stats, x='average', y='strike_rate', hover_name='batter',
                     hover_data={'batter': False, 'runs': True, 'balls_played': True, 'dismissals': True},
                     labels={'average': 'Average', 'strike_rate': 'Strike Rate'},
                     title='Batsman Average vs Strike Rate')
    fig.update_traces(marker=dict(size=5))
    fig.update_layout(hovermode='closest' , height = 600 , width = 600 )
    return fig 

# average_vs_strike_rate(match_data , ball_data , season = 2016   )



def average_vs_economy_rate(match_data, ball_data, team=None, season=None):
    ball_data = ball_data.merge(match_data[['ID', 'Season', 'Team1', 'Team2']], on='ID', how='left')
    
    ball_data['BowlingTeam'] = np.where(ball_data['BattingTeam'] != ball_data['Team1'], ball_data['Team1'], ball_data['Team2'])
    
    if season is not None:
        ball_data = ball_data[ball_data['Season'] == season]
    
    if team is not None:
        ball_data = ball_data[ball_data['BowlingTeam'] == team].reset_index(drop=True)
    
    bowler_stats = ball_data.groupby(['bowler', 'BowlingTeam']).agg(
        runs_conceded=('batsman_run', 'sum'),  
        balls_bowled=('bowler', 'count'),  
        wickets=('isWicketDelivery', 'sum')  
    ).reset_index()
    
    bowler_stats['average'] = bowler_stats['runs_conceded'] / bowler_stats['wickets']
    bowler_stats['economy'] = bowler_stats['runs_conceded'] / (bowler_stats['balls_bowled'] / 6)
    
    bowler_stats = bowler_stats[(bowler_stats['balls_bowled'] > 0) & (bowler_stats['wickets'] > 5)]
    
    fig = go.Figure(data=go.Scatter(
        x=bowler_stats['average'],
        y=bowler_stats['economy'],
        mode='markers',
        marker=dict(size=5),
        text=bowler_stats['bowler'],
        hoverinfo='text+x+y',
    ))
    
    fig.update_layout(
        title='Bowler Average vs Economy Rate',
        xaxis_title='Average',
        yaxis_title='Economy Rate',
        hovermode='closest',
        width=600,
        height=600,
    )
    
    return fig


def plot_toss_outcome_team(match_data, team, season=None):
    if season is not None: 
        match_data = match_data[match_data['Season'] == season]
    team_data = match_data[(match_data['Team1'] == team) | (match_data['Team2'] == team)]
    
    toss_outcome = team_data['toss_winner_wins_match'].value_counts()
    trace = go.Pie(
        labels=['Won', 'Lost'],
        values=toss_outcome.values,
        marker=dict(colors=['lightseagreen', 'salmon']),
        hoverinfo='label+value',
        textinfo='percent',
        title='',
    )

    # Define layout
    layout = go.Layout(
        legend=dict(orientation="h", yanchor="top", y=1.25, xanchor="center", x=0.5),
        width=400,
        height=400
    )

    # Create figure
    fig = go.Figure(data=[trace], layout=layout)

    return fig


def runs_heatmap_for_batter( match_data , ball_data , batter  , season = None ) : 
    ball_data = ball_data.merge(match_data[['ID', 'Season', 'Team1', 'Team2']], on='ID', how='left')
    ball_data['BowlingTeam'] = np.where(ball_data['BattingTeam'] != ball_data['Team1'], ball_data['Team1'], ball_data['Team2'])
    if season is not None:
        ball_data = ball_data[ball_data['Season'] == season] 
    if batter!= None : 
        ball_data = ball_data[ball_data['batter'] == batter].reset_index(drop=True)
  
    new_df = ball_data.groupby(['overs', 'ballnumber'])['batsman_run'].sum().unstack(fill_value=0)
    
    new_df = new_df.reindex(index=range(20), columns=range(1, 7), fill_value=0)
    new_df.index = new_df.index.astype(str)
    new_df.columns = new_df.columns.astype(str)

    trace = go.Heatmap(
        z=new_df.values,
        x=new_df.columns,
        y=new_df.index,
        colorscale='YlGnBu',
        colorbar=dict(title='Runs') , 
        hovertemplate='Over Number: %{y}<br>Ball Number: %{x}<br>Runs: %{z}' , 
        name = "wickets"
    )
    
    # Create layout
    layout = go.Layout(
        title='',
        xaxis=dict(title='Ball Number'),
        yaxis=dict(title='Overs') , width = 600 , height = 700
    )
    
    fig = go.Figure(data=[trace], layout=layout)
    return fig


def runs_scored_by_over_type(match_data, ball_data, batter, season=None):
    ball_data = ball_data.merge(match_data[['ID', 'Season', 'Team1', 'Team2']], on='ID', how='left')
    ball_data['BowlingTeam'] = np.where(ball_data['BattingTeam'] != ball_data['Team1'], ball_data['Team1'], ball_data['Team2'])
    if season is not None:
        ball_data = ball_data[ball_data['Season'] == season] 
    ball_data = ball_data[ball_data['batter'] == batter].reset_index(drop=True)
    grouped_data = ball_data.groupby('overs').agg({ 'batsman_run': 'sum'}).reset_index()

    grouped_data.rename(columns={'batsman_run': 'total_runs'}, inplace=True)
    powerplay_runs = grouped_data.loc[grouped_data['overs'] <= 6, 'total_runs'].sum()
    middle_overs_runs = grouped_data.loc[(grouped_data['overs'] > 6) & (grouped_data['overs'] <= 15), 'total_runs'].sum()
    death_overs_runs = grouped_data.loc[grouped_data['overs'] > 15, 'total_runs'].sum()
    
    labels = ['Powerplay', 'Middle Overs', 'Death Overs']
    values = [powerplay_runs, middle_overs_runs, death_overs_runs]
    
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3)])
    
    fig.update_layout(title='',
                      showlegend=True,
                      legend=dict(orientation="h", y=1.15, x=0.5 , xanchor="center",) , width = 600 , height = 400 )
    
    return fig

def plot_runs_scored_against_teams(match_data, ball_data, batter, season=None):
    ball_data = ball_data.merge(match_data[['ID', 'Season', 'Team1', 'Team2']], on='ID', how='left')
    ball_data['BowlingTeam'] = np.where(ball_data['BattingTeam'] != ball_data['Team1'], ball_data['Team1'], ball_data['Team2'])
    if season is not None:
        ball_data = ball_data[ball_data['Season'] == season]
    ball_data = ball_data[ball_data['batter'] == batter].reset_index(drop=True)
    batsman_bowling_team_runs = ball_data.groupby(['batter', 'BowlingTeam'])['batsman_run'].sum().reset_index()
    df = batsman_bowling_team_runs.copy()
    df = df.sort_values(by='batsman_run', ascending=True)
    
    fig = go.Figure(data=[
        go.Bar(
            x=df['batsman_run'],
            y=df['BowlingTeam'],
            orientation='h',
            hoverinfo='x+y',
            
            marker=dict(color='lightseagreen', line=dict(color='black', width=1.5))  
        )
    ])
    
    fig.update_layout(
        title='',
        xaxis_title='Runs',
        yaxis_title='Bowling Team',
        width=600,
        height=600
    )
    
    return fig


def wickets_taken_by_over_type(match_data, ball_data, bowler, season=None):
    ball_data = ball_data.merge(match_data[['ID', 'Season', 'Team1', 'Team2']], on='ID', how='left')
    ball_data['BowlingTeam'] = np.where(ball_data['BattingTeam'] != ball_data['Team1'], ball_data['Team1'], ball_data['Team2'])
    if season is not None:
        ball_data = ball_data[ball_data['Season'] == season] 
    ball_data = ball_data[ball_data['bowler'] == bowler].reset_index(drop=True)
    grouped_data = ball_data.groupby('overs').agg({'isWicketDelivery': 'sum', 'total_run': 'sum'}).reset_index()

    grouped_data.rename(columns={'isWicketDelivery': 'total_wickets'}, inplace=True)
    powerplay_wickets = grouped_data.loc[grouped_data['overs'] <= 6, 'total_wickets'].sum()
    middle_overs_wickets = grouped_data.loc[(grouped_data['overs'] > 6) & (grouped_data['overs'] <= 15), 'total_wickets'].sum()
    death_overs_wickets = grouped_data.loc[grouped_data['overs'] > 15, 'total_wickets'].sum()
    
    # Create labels and values for the pie chart
    labels = ['Powerplay', 'Middle Overs', 'Death Overs']
    values = [powerplay_wickets, middle_overs_wickets, death_overs_wickets]
    
    # Create the pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3)])
    
    # Set the layout
    fig.update_layout(title='',
                      showlegend=True,
                      legend=dict(orientation="h", y=1.35, x=0.5 , xanchor="center",) , width = 600 , height = 400 )
    
    return fig


def plot_wickets_dot_4s_6s(match_data , ball_data, bowler , season = None ):
    ball_data = ball_data.merge(match_data[['ID', 'Season', 'Team1', 'Team2']], on='ID', how='left')
    ball_data['BowlingTeam'] = np.where(ball_data['BattingTeam'] != ball_data['Team1'], ball_data['Team1'], ball_data['Team2'])
    ball_data = ball_data[ball_data['bowler'] == bowler].reset_index(drop=True)
    if season != None :
        ball_data = ball_data[ball_data['Season'] == season ]
    bowler_data = ball_data[ball_data['bowler'] == bowler]
    
    # Count wickets, dot balls, 4s, and 6s
    wickets = bowler_data['player_out'].count()
    dot_balls = bowler_data[bowler_data['batsman_run'] == 0]['batsman_run'].count()
    fours = bowler_data[bowler_data['batsman_run'] == 4]['batsman_run'].count()
    sixes = bowler_data[bowler_data['batsman_run'] == 6]['batsman_run'].count()
    one_two_three = bowler_data[(bowler_data['batsman_run'] > 0) & (bowler_data['batsman_run'] < 4)]['batsman_run'].count()
    
    # Create labels and values for the pie chart
    labels = ['Wickets', 'Dot Balls', '4s', '6s', '1s, 2s, 3s']
    values = [wickets, dot_balls, fours, sixes, one_two_three]
    
    # Create the pie chart
    fig = go.Figure(data=[go.Pie(labels=labels, values=values , hole=.3 )])
    fig.update_layout(title='' , width = 600 , height = 400 , legend=dict(orientation="h", y=1.35, x=0.5 , xanchor="center",) )
    
    return fig


def plot_bowler_wickets(match_data, ball_data, bowler, season=None):
    ball_data = ball_data.merge(match_data[['ID', 'Season', 'Team1', 'Team2']], on='ID', how='left')
    
    if season is not None:
        ball_data = ball_data[ball_data['Season'] == season] 
    
    ball_data = ball_data[ball_data['bowler'] == bowler].reset_index(drop=True)
    
    bowler_wickets = {}
    for i in range(len(ball_data)):
        player_out = ball_data['player_out'][i]
        if pd.notnull(player_out):
            if player_out in bowler_wickets:
                bowler_wickets[player_out] += 1
            else:
                bowler_wickets[player_out] = 1
    
    sorted_bowler_wickets = dict(sorted(bowler_wickets.items(), key=lambda item: item[1], reverse=True))
    
    batsmen_names = list(sorted_bowler_wickets.keys())[0:10][::-1]
    wickets_taken = list(sorted_bowler_wickets.values())[0:10][::-1]
    
    fig = go.Figure(data=[go.Bar(x=wickets_taken, y=batsmen_names, orientation='h',
                                 marker=dict(color='skyblue', line=dict(color='navy', width=1.5)))])
    fig.update_layout(title='',
                      xaxis_title='Number of Wickets Taken',
                      yaxis_title='Batsman',
                      width=600, height=400)
    return fig

def plot_bowler_most_beaten_by_batsman(match_data, ball_data, bowler, season=None):
    ball_data = ball_data.merge(match_data[['ID', 'Season', 'Team1', 'Team2', 'Venue']], on='ID', how='left')
    ball_data['BowlingTeam'] = np.where(ball_data['BattingTeam'] != ball_data['Team1'], ball_data['Team1'], ball_data['Team2'])

    if season is not None:
        ball_data = ball_data[ball_data['Season'] == season]
    ball_data = ball_data[ball_data['bowler'] == bowler]
    total_batsman_runs = ball_data.groupby('batter')['batsman_run'].sum().reset_index()
    total_batsman_runs = total_batsman_runs.sort_values(by='batsman_run', ascending=False)[:10]

    # Plotting using Plotly
    fig = go.Figure(go.Bar(
        x=total_batsman_runs['batsman_run'],
        y=total_batsman_runs['batter'],
        orientation='h',
        marker_color='skyblue'
    ))

    fig.update_layout(
        title='Beaten by batsman',
        xaxis_title='Runs',
        yaxis_title='Batsman',
        yaxis=dict(autorange="reversed"),
        xaxis=dict(side='bottom') , width = 600 , height = 400 
    )

    return fig

# Call the function and display the Plotly figure

