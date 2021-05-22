import numpy as np
import pandas as pd
import os,sys



#import team data
team_stats = pd.read_csv("personal-python/data.csv", sep=',')
team_stats

#generate a schedule of matches where everyone plays eachother twice

#generate simulated values based on mean and stddev
number_of_sims = 5

goals_weight = 0.5
goals_allowed_weight = 0.5

team1_goals_mean = 1
team1_goals_stddev = 1
team1_goals_allowed_mean = 2 
team1_goals_allowed_stddev = 1
team2_goals_mean = 2
team2_goals_stddev = 1
team2_goals_allowed_mean = 1
team2_goals_allowed_stddev = 1

team1_goals = np.random.normal(team1_goals_mean,team1_goals_stddev,number_of_sims)
team1_goals_allowed = np.random.normal(team1_goals_allowed_mean,team1_goals_allowed_stddev,number_of_sims)
team2_goals = np.random.normal(team2_goals_mean,team2_goals_stddev,number_of_sims)
team2_goals_allowed = np.random.normal(team2_goals_allowed_mean,team2_goals_stddev,number_of_sims)

#weigh goals and goals against for opponent to get estimated goals for each team
team1_goal_estimate = (team1_goals * goals_weight) + (team2_goals_allowed * goals_allowed_weight)
team2_goal_estimate = (team2_goals * goals_weight) + (team1_goals_allowed * goals_allowed_weight)

#generate compare array with esimated goals to determine winner
team1_result_wins = (team1_goal_estimate > team2_goals_allowed)
print(team1_result_wins)

#count true/false values to determine wins/losses
team1_wins = np.count_nonzero(team1_result_wins)
team1_losses = np.size(team1_result_wins) - np.count_nonzero(team1_result_wins)
team1_win_pct = team1_wins / (team1_wins + team1_losses)
print(f"Team 1 - Wins: {team1_wins}, Losses: {team1_losses}, Win %: {team1_win_pct}")

#show summarized totals throughout the simulated season