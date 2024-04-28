import pandas as pd

def get_top_players(team_name, season=None):
    # Load the ball-by-ball ball_data or player-level statistics ball_data

    # Filter the ball_data for the given team and season (if provided)
    team_data = ball_data[ball_data['batting_team'] == team_name]
    if season is not None:
        team_data = team_data[team_data['season'] == season]

    # Calculate runs scored and wickets taken for each player
    runs_scored = team_data.groupby('batter')['runs_scored'].sum().reset_index()
    wickets_taken = team_data.groupby('bowler')['dismissal_kind'].count().reset_index()
    wickets_taken.rename(columns={'dismissal_kind': 'wickets_taken'}, inplace=True)

    # Sort the players based on runs scored and wickets taken
    top_scorers = runs_scored.sort_values(by='runs_scored', ascending=False)
    top_wicket_takers = wickets_taken.sort_values(by='wickets_taken', ascending=False)

    # Return the top players' names, runs scored, and wickets taken
    return top_scorers.head(), top_wicket_takers.head()

# Example usage
top_scorers, top_wicket_takers = get_top_players('Mumbai Indians', season=2022)
print("Top Scorers:")
print(top_scorers)
print("\nTop Wicket-Takers:")
print(top_wicket_takers)