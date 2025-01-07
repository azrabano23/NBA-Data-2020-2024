import pandas as pd
import numpy as np
import random
from IPython.display import display

# Load the datasets
# Replace these filenames with your actual file paths or upload them in Colab
def load_datasets():
    regular_season = pd.read_csv("regular_season_box_scores_2010_2024_part_1.csv")
    playoffs = pd.read_csv("play_off_box_scores_2010_2024.csv")
    totals = pd.read_csv("regular_season_totals_2010_2024.csv")
    return regular_season, playoffs, totals

regular_season, playoffs, totals = load_datasets()

# Function to retrieve recent games and outcomes
def get_recent_games(team_name, num_games=5):
    recent_games = totals[totals['TEAM_NAME'].str.contains(team_name, case=False)]
    recent_games = recent_games.sort_values('GAME_DATE', ascending=False).head(num_games)
    return recent_games[['GAME_DATE', 'MATCHUP', 'WL', 'PTS']]

# Function to retrieve player performance stats
def get_player_stats(player_name):
    player_stats = regular_season[regular_season['personName'].str.contains(player_name, case=False)]
    return player_stats[['season_year', 'game_date', 'teamName', 'points', 'assists', 'reboundsTotal']]

# Function to find the highest points scored in a game
def get_highest_points():
    top_score = regular_season.loc[regular_season['points'].idxmax()]
    return top_score[['personName', 'teamName', 'game_date', 'points']]

# Function to compare players based on key metrics
def compare_players(player1, player2):
    p1_stats = regular_season[regular_season['personName'].str.contains(player1, case=False)].mean()
    p2_stats = regular_season[regular_season['personName'].str.contains(player2, case=False)].mean()
    return pd.DataFrame({'Player': [player1, player2], 
                         'Points': [p1_stats['points'], p2_stats['points']],
                         'Rebounds': [p1_stats['reboundsTotal'], p2_stats['reboundsTotal']],
                         'Assists': [p1_stats['assists'], p2_stats['assists']]})

# Function to compare teams based on key metrics
def compare_teams(team1, team2):
    team1_stats = totals[totals['TEAM_NAME'] == team1].mean()
    team2_stats = totals[totals['TEAM_NAME'] == team2].mean()
    return pd.DataFrame({'Team': [team1, team2], 
                         'Points': [team1_stats['PTS'], team2_stats['PTS']],
                         'Win %': [team1_stats['W_PCT_RANK'], team2_stats['W_PCT_RANK']]})

# Function to generate a trivia question
def trivia_question():
    question_type = random.choice(['team_blocks', 'player_points', 'team_wins'])
    if question_type == 'team_blocks':
        year = random.choice(totals['SEASON_YEAR'].unique())
        top_team = totals[totals['SEASON_YEAR'] == year].sort_values('BLK', ascending=False).iloc[0]
        return f"In {year}, which team had the most blocks?", top_team['TEAM_NAME']
    elif question_type == 'player_points':
        top_player = regular_season.loc[regular_season['points'].idxmax()]
        return f"Which player scored the most points in a single game?", top_player['personName']
    elif question_type == 'team_wins':
        year = random.choice(totals['SEASON_YEAR'].unique())
        top_team = totals[totals['SEASON_YEAR'] == year].sort_values('W_RANK', ascending=True).iloc[0]
        return f"In {year}, which team had the most wins?", top_team['TEAM_NAME']

# Function to validate team or player existence
def validate_input(input_name, dataset, column):
    return dataset[column].str.contains(input_name, case=False).any()

# Interactive user interface
def main():
    print("Welcome to the NBA Fan AI Program!")
    while True:
        print("\nOptions:")
        print("[1] Recent Games")
        print("[2] Player Stats")
        print("[3] Compare Players")
        print("[4] Compare Teams")
        print("[5] Trivia")
        print("[6] Exit")
        
        option = input("Choose an option: ")
        
        if option == '1':
            team = input("Enter team name: ")
            if validate_input(team, totals, 'TEAM_NAME'):
                display(get_recent_games(team))
            else:
                print("Team not found. Please try again.")
        elif option == '2':
            player = input("Enter player name: ")
            if validate_input(player, regular_season, 'personName'):
                display(get_player_stats(player))
            else:
                print("Player not found. Please try again.")
        elif option == '3':
            player1 = input("Enter first player: ")
            player2 = input("Enter second player: ")
            if validate_input(player1, regular_season, 'personName') and validate_input(player2, regular_season, 'personName'):
                display(compare_players(player1, player2))
            else:
                print("One or both players not found. Please try again.")
        elif option == '4':
            team1 = input("Enter first team: ")
            team2 = input("Enter second team: ")
            if validate_input(team1, totals, 'TEAM_NAME') and validate_input(team2, totals, 'TEAM_NAME'):
                display(compare_teams(team1, team2))
            else:
                print("One or both teams not found. Please try again.")
        elif option == '5':
            question, answer = trivia_question()
            print("Question:", question)
            print("Answer:", answer)
        elif option == '6':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
