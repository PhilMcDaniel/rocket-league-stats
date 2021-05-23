import numpy as np
import pandas as pd
import os,sys

#import team data
team_stats = pd.read_csv("personal-python/data.csv", sep=',')
team_stats

#generate a schedule of matches where everyone plays eachother twice

#generate simulated values based on mean and stddev
number_of_sims = 100000

goals_weight = .5
goals_allowed_weight = .5

team1 = 'Rochester Riff'
team2 = 'Bloomington Ursas'

#get team 1 values
team1_goals_mean = team_stats['Goals/Game'][team_stats["Team Name"] == team1].values[0]
team1_goals_stddev = team_stats['Std Dev Goals'][team_stats["Team Name"] == team1].values[0]
team1_goals_allowed_mean = team_stats['Goals Against/Game'][team_stats["Team Name"] == team1].values[0]
team1_goals_allowed_stddev = team_stats['Std Dev Goals Against'][team_stats["Team Name"] == team1].values[0]

#get team 2 values
team2_goals_mean = team_stats['Goals/Game'][team_stats["Team Name"] == team2].values[0]
team2_goals_stddev = team_stats['Std Dev Goals'][team_stats["Team Name"] == team2].values[0]
team2_goals_allowed_mean = team_stats['Goals Against/Game'][team_stats["Team Name"] == team2].values[0]
team2_goals_allowed_stddev = team_stats['Std Dev Goals Against'][team_stats["Team Name"] == team2].values[0]

#generate random data
team1_goals = np.random.normal(team1_goals_mean,team1_goals_stddev,number_of_sims)
team1_goals_allowed = np.random.normal(team1_goals_allowed_mean,team1_goals_allowed_stddev,number_of_sims)
team2_goals = np.random.normal(team2_goals_mean,team2_goals_stddev,number_of_sims)
team2_goals_allowed = np.random.normal(team2_goals_allowed_mean,team2_goals_allowed_stddev,number_of_sims)

#weigh goals and goals against for opponent to get estimated goals for each team
team1_goal_estimate = (team1_goals * goals_weight) + (team2_goals_allowed * goals_allowed_weight)
team2_goal_estimate = (team2_goals * goals_weight) + (team1_goals_allowed * goals_allowed_weight)

#generate compare array with esimated goals to determine winner
team1_result_wins = (team1_goal_estimate > team2_goal_estimate)
print(team1_result_wins)

#count true/false values to determine wins/losses
team1_wins = np.count_nonzero(team1_result_wins)
team1_losses = np.size(team1_result_wins) - np.count_nonzero(team1_result_wins)
team1_win_pct = team1_wins / (team1_wins + team1_losses)
team1_loss_pct = team1_losses / (team1_wins + team1_losses)
print(f"{team1} - Wins: {team1_wins}, Losses: {team1_losses}, Win %: {team1_win_pct}")
print(f"{team2} - Wins: {team1_losses}, Losses: {team1_wins}, Win %: {team1_loss_pct}")
#show summarized totals throughout the simulated season