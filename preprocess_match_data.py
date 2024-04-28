import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import seaborn as sns
import warnings 
warnings.filterwarnings("ignore")

def preprocess(match_data):
    match_data['City'] = match_data['City'].fillna("NA")
    match_data['Player_of_Match'] = match_data['Player_of_Match'].fillna("NA")
    match_data.loc[match_data['Venue'] == 'Arun Jaitley Stadium', 'Venue'] = 'Arun Jaitley Stadium, Delhi'
    match_data.loc[match_data['Venue'] == 'Brabourne Stadium', 'Venue'] = 'Brabourne Stadium, Mumbai'
    match_data.loc[match_data['Venue'] == 'Dr DY Patil Sports Academy', 'Venue'] = 'Dr DY Patil Sports Academy, Mumbai'
    match_data.loc[match_data['Venue'] == 'Eden Gardens', 'Venue'] = 'Eden Gardens, Kolkata'
    match_data.loc[match_data['Venue'] == 'M.Chinnaswamy Stadium', 'Venue'] = 'M Chinnaswamy Stadium'
    match_data.loc[match_data['Venue'] == 'MA Chidambaram Stadium', 'Venue'] = 'MA Chidambaram Stadium, Chepauk, Chennai'
    match_data.loc[match_data['Venue'] == 'MA Chidambaram Stadium, Chepauk', 'Venue'] = 'MA Chidambaram Stadium, Chepauk, Chennai'
    match_data.loc[match_data['Venue'] == 'Maharashtra Cricket Association Stadium', 'Venue'] = 'Maharashtra Cricket Association Stadium, Pune'
    match_data.loc[match_data['Venue'] == 'Punjab Cricket Association IS Bindra Stadium', 'Venue'] = 'Punjab Cricket Association IS Bindra Stadium, Mohali'
    match_data.loc[match_data['Venue'] == 'Punjab Cricket Association Stadium, Mohali', 'Venue'] = 'Punjab Cricket Association IS Bindra Stadium, Mohali'
    match_data.loc[match_data['Venue'] == 'Rajiv Gandhi International Stadium', 'Venue'] = 'Rajiv Gandhi International Stadium, Uppal'
    match_data.loc[match_data['Venue'] == 'Wankhede Stadium', 'Venue'] = 'Wankhede Stadium, Mumbai'
    match_data.loc[match_data['WinningTeam'] == 'Rising Pune Supergiant', 'WinningTeam'] = 'Rising Pune Supergiants'
    match_data.loc[match_data['Team1'] == 'Rising Pune Supergiant', 'Team1'] = 'Rising Pune Supergiants'
    match_data.loc[match_data['Team2'] == 'Rising Pune Supergiant', 'Team2'] = 'Rising Pune Supergiants'
    match_data.loc[match_data['TossWinner'] == 'Rising Pune Supergiant', 'TossWinner'] = 'Rising Pune Supergiants'
    for i in range(len(match_data)):
        if(len(match_data['Season'][i]) > 4 ):
            temp = match_data['Season'][i]
            if(temp == '2020/21'):
                match_data['Season'][i] = 2020
            else:
                match_data['Season'][i] = temp[0:2] + temp[5:]

    match_data.to_csv("cleaned_match_data.csv")

