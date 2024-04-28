import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import warnings 
warnings.filterwarnings("ignore")

def get_winner( match_data , year ) : 
    
    temp_data = match_data[(match_data['Season'] == year) & (match_data['MatchNumber'] == 'Final')]
    team1 = temp_data['Team1'].item()
    team2 = temp_data['Team2'].item()
    winner = temp_data['WinningTeam'].item()
    method = temp_data['method']
    won_by = "Won by Super Over"
    if temp_data['method'].isna().any():
        won_by = "Won By " + str(int(temp_data["Margin"].item())) + " " + str(temp_data['WonBy'].item()) 
    data = {
        "team-1" : team1 , 
        "team-2" : team2 , 
        "winner" : winner , 
        "won_by" : won_by , 
    }
    return data


def get_most_time_winner(match_data ):
    temp_data = match_data[match_data['MatchNumber'] == 'Final']
    winners = temp_data['WinningTeam']
    winner_counter = Counter(winners) 
    most_time_winners = [] 
    most_titles = max(winner_counter.values()) 
    for i in winner_counter :
        if(winner_counter[i] == most_titles ) : 
            most_time_winners.append(i)
    data = {
        'most_time_winners' : most_time_winners ,
        'most_titles_won_by_a_team' : most_titles ,
        'titles_winnings' : dict(winner_counter)
    }
    return data

def get_all_batsman(ball_data): 
    return list(ball_data['batter'].unique())

def get_all_bowlers(ball_data):
    return list(ball_data['bowler'].unique())

def get_all_teams(match_data):
    return list(match_data['Team1'].unique()) 

def get_stats(match_data, ball_data, season=None):
    temp_match_data = match_data.copy()
    temp_ball_data = ball_data.copy()

    if season is not None:
        temp_match_data = temp_match_data[temp_match_data['Season'] == season]

    match_ids = temp_match_data['ID'].unique()

    innings_1_data = temp_ball_data[(temp_ball_data['ID'].isin(match_ids)) & (temp_ball_data['innings'] == 1)]
    innings_2_data = temp_ball_data[(temp_ball_data['ID'].isin(match_ids)) & (temp_ball_data['innings'] == 2)]

    innings_1_runs = innings_1_data.groupby('ID')['total_run'].sum()
    innings_2_runs = innings_2_data.groupby('ID')['total_run'].sum()

    innings_1_wickets = innings_1_data.groupby('ID')['isWicketDelivery'].sum()
    innings_2_wickets = innings_2_data.groupby('ID')['isWicketDelivery'].sum()

    innings_1_sixes = (innings_1_data[innings_1_data['batsman_run'] == 6].groupby('ID')['total_run'].sum() // 6).fillna(0)
    innings_1_fours = (innings_1_data[innings_1_data['batsman_run'] == 4].groupby('ID')['total_run'].sum() // 4).fillna(0)

    innings_2_sixes = (innings_2_data[innings_2_data['batsman_run'] == 6].groupby('ID')['total_run'].sum() // 6).fillna(0)
    innings_2_fours = (innings_2_data[innings_2_data['batsman_run'] == 4].groupby('ID')['total_run'].sum() // 4).fillna(0)

    total_sixes = innings_1_sixes.sum() + innings_2_sixes.sum()
    total_fours = innings_1_fours.sum() + innings_2_fours.sum()

    total_matches = len(match_ids)

    average_inning1_score = innings_1_runs.mean()
    average_inning2_score = innings_2_runs.mean()
    average_score = int((average_inning1_score + average_inning2_score) / 2)

    data = {
        'average_inning1_score': average_inning1_score,
        'average_inning2_score': average_inning2_score,
        'sixes': total_sixes,
        'fours': total_fours,
        'average_score': average_score,
        'total_matches': total_matches
    }
    return data

# get_stats(match_data , ball_data , season = 2020 )
def get_scores_data(match_data, ball_data, team, season=None):
    inning1_scores = []
    inning2_scores = []
    inning1_wickets_lost = []
    inning2_wickets_lost = []
    inning1_sixes = []
    inning2_sixes = []
    inning1_fours = []
    inning2_fours = []
    match_ids = list(match_data['ID'])
    for match_id in match_ids:
        temp_data = ball_data[(ball_data['ID'] == match_id) & (ball_data['BattingTeam'] == team)]
        if len(temp_data) == 0:
            continue
        curr_season = match_data[match_data['ID'] == match_id]['Season'].item()
        if curr_season != season and season != None : 
            continue

        runs_scored = temp_data['total_run'].sum()
        wickets_lost = temp_data['isWicketDelivery'].sum()
        fours = len(temp_data[temp_data['batsman_run'] == 4])
        sixes = len(temp_data[temp_data['batsman_run'] == 6])
        if temp_data['innings'].iloc[0] == 1:
            inning1_scores.append(runs_scored)
            inning1_wickets_lost.append(wickets_lost)
            inning1_sixes.append(sixes)
            inning1_fours.append(fours)
        elif temp_data['innings'].iloc[0] == 2:
            inning2_scores.append(runs_scored)
            inning2_wickets_lost.append(wickets_lost)
            inning2_sixes.append(sixes)
            inning2_fours.append(fours)
    avg_inning1_score = 0 
    avg_inning2_score = 0
    max_inning1_score = 0 
    max_inning2_score = 0 
    if len(inning1_scores )> 0 :
        avg_inning1_score = round(sum(inning1_scores) / len(inning1_scores), 0) 
        max_inning1_score = max(inning1_scores)
    if len(inning2_scores )  > 0: 
        avg_inning2_score = round(sum(inning2_scores)/ len(inning1_scores) , 0 ) 
        max_inning2_score = max(inning2_scores)
    avg_score = 0 
    if len(inning1_scores) > 0 or len(inning2_scores) > 0 :  
        avg_score = (sum(inning1_scores) + sum(inning2_scores))/(len(inning1_scores) + len(inning2_scores ))
    total_sixes_inning1 = sum(inning1_sixes)
    total_sixes_inning2 = sum(inning2_sixes)
    total_fours_inning1 = sum(inning1_fours)
    total_fours_inning2 = sum(inning2_fours)
    total_fours = total_fours_inning1 + total_fours_inning2
    total_sixes = total_sixes_inning1 + total_sixes_inning2
    avg_wickets_lost_inning1 = 0 
    avg_wickets_lost_inning2 = 0 
    if len(inning1_wickets_lost) > 0 : 
        avg_wickets_lost_inning1 = sum(inning1_wickets_lost) // len(inning1_wickets_lost) 
    if len(inning2_wickets_lost) > 0 : 
        avg_wickets_lost_inning2 = sum(inning2_wickets_lost) // len(inning2_wickets_lost) 

    best_score = max( max_inning1_score , max_inning2_score )  
    best_score_wicket = 0
    for i in range(len(inning1_scores)):
        if inning1_scores[i] == best_score : 
            best_score_wicket = inning1_wickets_lost[i] 
            break 

    for i in range(len(inning2_scores)):
        if inning2_scores[i] == best_score : 
            best_score_wicket = inning2_wickets_lost[i] 
    matches_played = len(inning1_scores) + len(inning2_scores) 
    
    best = str(best_score) + '/' + str(best_score_wicket)
    return {
        'matches_played' : str(matches_played) , 
        'average_score' : str(int(avg_score)),
        'avg_inning1_score': str(avg_inning1_score),
        'avg_inning2_score': str(avg_inning2_score),
        'total_sixes_inning1': str(total_sixes_inning1),
        'total_sixes_inning2': str(total_sixes_inning2),
        'total_fours_inning1': str(total_fours_inning1),
        'total_fours_inning2': str(total_fours_inning2),
        'total_fours': str(total_fours),
        'total_sixes': str(total_sixes),
        'avg_wickets_lost_inning1': str(avg_wickets_lost_inning1),
        'avg_wickets_lost_inning2': str(avg_wickets_lost_inning2),
        'best' : best
    }


# result = get_scores_data(match_data, ball_data, team='Rajasthan Royals' , )
# print(result)


def get_top_batsman(ball_data, match_data, team_name, season=None):
    team_data = ball_data[ball_data['BattingTeam'] == team_name].reset_index(drop=True)
    
    team_data = team_data.merge(match_data[['ID', 'Season']], on='ID', how='left')
    
    if season is not None:
        team_data = team_data[team_data['Season'] == season]

    player_total_runs = team_data.groupby('batter')['batsman_run'].sum().reset_index()
    player_total_runs.columns = ['Player', 'TotalRuns']

    best_players = player_total_runs[player_total_runs['TotalRuns'] == max(player_total_runs['TotalRuns'])]
    
    return best_players.iloc[0]['Player'] , best_players.iloc[0]['TotalRuns']


def get_top_bowlers(ball_data, match_data, team_name, season=None):
    # Merge match_data to ball_data to get 'Season' information
    ball_data = ball_data.merge(match_data[['ID', 'Season', 'Team1', 'Team2']], on='ID', how='left')

    # Determine BowlingTeam based on BattingTeam and Team1/Team2
    ball_data['BowlingTeam'] = np.where(ball_data['BattingTeam'] != ball_data['Team1'], ball_data['Team1'], ball_data['Team2'])

    # Filter data based on season if provided
    if season is not None:
        ball_data = ball_data[ball_data['Season'] == season]

    # Filter data for the specified team
    team_data = ball_data[ball_data['BowlingTeam'] == team_name]

    # Group by bowler and sum up wickets taken
    bowler_wickets = team_data.groupby('bowler')['isWicketDelivery'].sum().reset_index()

    # Find the best bowler
    best_bowler_data = bowler_wickets[bowler_wickets['isWicketDelivery'] == bowler_wickets['isWicketDelivery'].max()]
    best_bowler = best_bowler_data.iloc[0]['bowler']
    best_wickets = best_bowler_data.iloc[0]['isWicketDelivery']

    return best_bowler, best_wickets
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
    
# get_batter_runs(match_data , ball_data , "V Kohli" , season = 2022 )

def get_bowler_wickets(match_data, ball_data, bowler, season=None):
    ball_data = ball_data.merge(match_data[['ID', 'Season', 'Team1', 'Team2']], on='ID', how='left')
    
    if season is not None:
        ball_data = ball_data[ball_data['Season'] == season] 
    
    ball_data = ball_data[ball_data['bowler'] == bowler].reset_index(drop=True)
    
    total_wickets = ball_data['player_out'].notnull().sum()
    total_runs_given = ball_data['total_run'].sum()
    total_balls_bowled = len(ball_data)
    economy_rate = (total_runs_given / total_balls_bowled) * 6
    if total_wickets != 0:
        average = total_runs_given / total_wickets
    else:
        average = None
    
    data = {
        'total_wickets': total_wickets,
        'total_runs_given': total_runs_given,
        'total_balls_bowled': total_balls_bowled,
        'economy_rate': economy_rate,
        'average': average
    }
    return data
# get_bowler_wickets(match_data , ball_data , bowler = "Mohammed Shami" , season = 2022 )