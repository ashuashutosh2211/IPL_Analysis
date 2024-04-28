import pandas as pd
import numpy as np 
import json 
def orange_cap_winner(ball_data, match_data, season=None): 
    players_run = {} 
    players_ball = {}
    max_runs = 0 
    orange_cap_player = None 
    players_sixes = {}
    players_fours = {}
    for i in range(len(ball_data)): 
        curr_season = None 
        if season is not None: 
            curr_season = match_data[match_data['ID'] == ball_data['ID'][i]]['Season'].item() 
        if curr_season == season:
            player = ball_data['batter'][i]
            batsman_runs = ball_data['batsman_run'][i]
            if player in players_run: 
                players_run[player] += batsman_runs
                players_ball[player] += 1 
                max_runs = max(max_runs , players_run[player])
            else:
                players_run[player] = batsman_runs
                players_ball[player] = 1 
                max_runs = max(max_runs , players_run[player])

            if(batsman_runs == 6 ) : 
                if(player in players_sixes):
                    players_sixes[player] += 1 
                else:
                    players_sixes[player] = 1 

            if(batsman_runs == 4 ) : 
                if(player in players_fours) :
                    players_fours[player] += 1 
                else:
                    players_fours[player] = 1 
            
            if players_run[player] == max_runs: 
                orange_cap_player = player 
    strike_rate = round(players_run[orange_cap_player] / players_ball[orange_cap_player], 4 ) * 100 
    # sixes = len(ball_data[(ball_data['batter'] == orange_cap_player ) & (ball_data['batsman_run'] == 6)])
    # fours = len(ball_data[(ball_data['batter'] == orange_cap_player ) & (ball_data['batsman_run'] == 4)])
    sixes = players_sixes[orange_cap_player]
    fours = players_fours[orange_cap_player] 
    data = {
        "player"  : str(orange_cap_player) , 
        "runs" : str(players_run[orange_cap_player]) , 
        "strike_rate" : str(strike_rate) , 
        "balls" : str(players_ball[orange_cap_player]) , 
        "sixes" : str(sixes) , 
        "fours" : str(fours) 
    }
    return data 
    # return orange_cap_player, players_run[orange_cap_player] , strike_rate 

def get_orange_cap_data( ball_data , match_data ): 
    data = orange_cap_winner(ball_data , match_data )
    orange_cap_dict = {
        'All' : data 
    }
    print("Overall ")
    print(data) 
    print("-" * 75 )
    for i in range(2008 , 2023 ) :

        data = orange_cap_winner( ball_data , match_data , season = i )
        print(f"Season : {i}") 
        print(data) 
        print("-" * 50 )
        orange_cap_dict[str(i)] = data 

    return orange_cap_dict 


ball_data = pd.read_csv("IPL_Ball_by_Ball_2008_2022.csv")
match_data = pd.read_csv("cleaned_match_data.csv")

orange_cap_dict = get_orange_cap_data( ball_data , match_data ) 
file_path = 'orange_cap_dict.json'
with open(file_path, "w") as json_file:
    json.dump(orange_cap_dict , json_file)