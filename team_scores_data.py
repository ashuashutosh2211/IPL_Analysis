import pandas as pd 
import numpy as np 
import json 

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

def get_all_teams(match_data):
    return list(match_data['Team1'].unique()) 


def get_all_team_scores_data( match_data , ball_data ) : 
    teams_score_data = {} 
    teams = get_all_teams(match_data) 
    for team in teams:
        team_data = {} 
        team_data["All"] = get_scores_data(match_data , ball_data , team = team ) 
        for season in range(2008 , 2023 ) : 
            team_data[str(season)] = get_scores_data(match_data , ball_data , team = team , season = season ) 
        print(team_data)
        teams_score_data[team] = team_data
    return teams_score_data


ball_data = pd.read_csv("IPL_Ball_by_Ball_2008_2022.csv")
match_data = pd.read_csv("cleaned_match_data.csv")
teams_score_data = get_all_team_scores_data(match_data , ball_data ) 


file_path = "teams_score_data.json"

with open(file_path, "w") as json_file:
    json.dump(teams_score_data, json_file)

print(f"Dictionary saved to {file_path}")
