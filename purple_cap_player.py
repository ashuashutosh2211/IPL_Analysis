import pandas as pd
import numpy as np 
import json 

def purple_cap_winner( ball_data , match_data , season  = None ) : 
    
    player_wickets = {} 
    player_runs_conceded = {}
    player_balls = {}
    max_wickets = 0 
    purple_cap_player = None 
    not_by_bowler = ['run out' , 'retired hurt', 'retired out',
       'obstructing the field']
    for i in range(len(ball_data)) : 
        curr_season = None 
        if season is not None: 
            curr_season = match_data[match_data['ID'] == ball_data['ID'][i]]['Season'].item() 
        if curr_season == season:
            player = ball_data['bowler'][i]
            runs_conceded = ball_data['total_run'][i] 
            is_wicket = ball_data['isWicketDelivery'][i]
            kind = ball_data['kind'][i]
            extra_type = ball_data['extra_type'][i]
            if player not in player_wickets:
                player_wickets[player] = is_wicket
                if kind in not_by_bowler : 
                    player_wickets[player] -= is_wicket 
                player_runs_conceded[player] = runs_conceded 
                if extra_type == 'legbyes' or extra_type == 'byes' or extra_type == 'penalty':
                    player_runs_conceded[player] -= ball_data['extras_run'][i]
                player_balls[player] = 1 
                if extra_type == 'wides' or extra_type == 'noballs':
                    player_balls[player] -= 1 
            else:
                player_wickets[player] += is_wicket
                if kind in not_by_bowler : 
                    player_wickets[player] -= is_wicket 
                player_runs_conceded[player] += runs_conceded 
                if extra_type == 'legbyes' or extra_type == 'byes' or extra_type == 'penalty':
                    player_runs_conceded[player] -= ball_data['extras_run'][i]
                player_balls[player] += 1 
                if extra_type == 'wides' or extra_type == 'noballs':
                    player_balls[player] -= 1 

                
            max_wickets = max(max_wickets , player_wickets[player] ) 
            
            if(max_wickets == player_wickets[player]) : 
                purple_cap_player = player 
            
    balls = player_balls[purple_cap_player]
    economy = round((player_runs_conceded[purple_cap_player]/balls ) * 6 , 2 ) 
    average = round( player_runs_conceded[purple_cap_player] / max(1, player_wickets[purple_cap_player])  ,2)
    bowling_strike_rate = round( balls/ max( 1 , player_wickets[purple_cap_player]) ,2 )
    
    data = {
        'player' : str(purple_cap_player) , 
        'wickets' :str( player_wickets[purple_cap_player] ), 
        'runs_conceded' : str(player_runs_conceded[purple_cap_player]) , 
        'balls' : str(balls) , 
        'economy' : str(economy) , 
        'average' : str(average) , 
        'bowling_strike_rate' : str(bowling_strike_rate) , 
    }
    return data

def get_purple_cap_data( ball_data , match_data ) : 
    data = purple_cap_winner(ball_data , match_data ) 
    purple_cap_dict = {
        "All" : data 
    }
    print("All") 
    print(data)
    print('-' * 70 )
    for i in range(2008 , 2023 ) : 

        data = purple_cap_winner(ball_data , match_data , season = i ) 
        print(str(i))
        print(data)
        print('-' * 70)
        purple_cap_dict[str(i)] = data 
    return purple_cap_dict


ball_data = pd.read_csv("IPL_Ball_by_Ball_2008_2022.csv")
match_data = pd.read_csv("cleaned_match_data.csv")

purple_cap_dict = get_purple_cap_data(ball_data , match_data ) 
file_path = 'purple_cap_dict.json'
with open(file_path, "w") as json_file:
    json.dump(purple_cap_dict , json_file)