import numpy as np
import pandas as pd
import os,sys

#import team data
team_stats = pd.read_csv("personal-python/data.csv", sep=',')
#team_stats

teams = team_stats['Team Name'].to_list()
#generate dictionary to hold standings
standings = {}
for team in teams:
    standings.update({team:{"match wins":0,"match losses":0,"game wins":0,"game losses":0}})

#generate a schedule of matches where everyone plays eachother twice
match_list = []
for team in teams:
    for team2 in teams:
        if(team2 == team):
            pass
        else:
            match_list.append([team,team2])
#print(match_list)

#set number of games per match & weight for goals and goals allowed
number_of_sims = 100

goals_weight = .5
goals_allowed_weight = .5

for match in match_list:

    team1 = match[0]
    team2 = match[1]

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
    #print(team1_result_wins)

    #count true/false values to determine wins/losses
    team1_wins = np.count_nonzero(team1_result_wins)
    team1_losses = np.size(team1_result_wins) - np.count_nonzero(team1_result_wins)
    #team1_win_pct = team1_wins / (team1_wins + team1_losses)
    #team1_loss_pct = team1_losses / (team1_wins + team1_losses)
    #print(f"{team1} - Wins: {team1_wins}, Losses: {team1_losses}, Win %: {team1_win_pct}")
    #print(f"{team2} - Wins: {team1_losses}, Losses: {team1_wins}, Win %: {team1_loss_pct}")
    #show summarized totals throughout the simulated season
    if team1_wins > team1_losses:
        standings.update({team1:{"match wins":standings[team1]["match wins"]+1,"match losses":standings[team1]["match losses"],"game wins":standings[team1]["game wins"]+team1_wins,"game losses":standings[team1]["game losses"]+team1_losses}})
        standings.update({team2:{"match losses":standings[team2]["match losses"]+1,"match wins":standings[team2]["match wins"],"game wins":standings[team2]["game wins"]+team1_losses,"game losses":standings[team2]["game losses"]+team1_wins}})
        #print(f"{team1} Wins, {team2} Loses")
    if team1_losses >= team1_wins:
        standings.update({team2:{"match wins":standings[team2]["match wins"]+1,"match losses":standings[team2]["match losses"],"game wins":standings[team2]["game wins"]+team1_losses,"game losses":standings[team2]["game losses"]+team1_wins}})
        standings.update({team1:{"match losses":standings[team1]["match losses"]+1,"match wins":standings[team1]["match wins"],"game wins":standings[team1]["game wins"]+team1_wins,"game losses":standings[team1]["game losses"]+team1_losses}})
        #print(f"{team2} Wins, {team1} Loses")

#add game win % to standings
for team in standings:
    game_win_pct = round((standings[team]['game wins'] / (standings[team]['game wins'] + standings[team]['game losses'])),4)
    standings[team]["game win %"]= game_win_pct

#generate sorted list of team names, most wins first
sorted_standings = sorted(standings, key=lambda x: (standings[x]['match wins'], standings[x]['game wins']),reverse=True)
#sorted_standings

for team in sorted_standings:
    print(f"{team} | match({standings[team]['match wins']}-{standings[team]['match losses']}) game({standings[team]['game wins']}-{standings[team]['game losses']}) game win % ({standings[team]['game win %']})")