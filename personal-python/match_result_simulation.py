import numpy as np
import pandas as pd
import os,sys

#import team data
team_stats = pd.read_csv("personal-python/data.csv", sep=',')
#strip % and convert column to float
team_stats['Game Win %'] = team_stats['Game Win %'].str.replace('%','').astype(float)


teams = team_stats[['Team Name','League','Season']].values.tolist()

#generate dictionary to hold standings
standings = {}
for team in teams:
    standings.update({team[0]:{"match wins":0,"match losses":0,"game wins":0,"game losses":0}})

#generate a schedule of matches where everyone plays eachother twice
match_list = []
for team in teams:
    #print(team[0])
    for team2 in teams:
        #Do nothing for the following (same team playing itself, team playing team from different league, team playing team from different season)
        if((team2[0] == team[0]) or (team[1] != team2[1]) or (team[2] != team2[2])):
            pass
        else:
            match_list.append([team[0],team2[0]])
#print(match_list)

#override here for single game sim
#match_list=[['Minneapolis Prodigies','Burnsville Firestorm']]


#set number of games per match & weight for goals and goals allowed
number_of_sims = 1000000

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
    if (standings[team]['game wins'] + standings[team]['game losses']) == 0:
        standings[team]["game win %"] = 0
    else:
        game_win_pct = 100*round((standings[team]['game wins'] / (standings[team]['game wins'] + standings[team]['game losses'])),4)
        standings[team]["game win %"]= game_win_pct

#generate sorted list of team names, most wins first
sorted_standings = sorted(standings, key=lambda x: (standings[x]['match wins'], standings[x]['game wins']),reverse=True)
#sorted_standings

#printing sorted standings
#for team in sorted_standings:
#    print(f"{team} | match({standings[team]['match wins']}-{standings[team]['match losses']}) game({standings[team]['game wins']}-{standings[team]['game losses']}) game win % ({standings[team]['game win %']})")

#add simulated data to dataframe
#team_stats = team_stats.append(standings,ignore_index=True,sort=False)
sim_stats = pd.DataFrame.from_dict(standings,orient = 'index')
sim_stats["Team Name"] = sim_stats.index
sim_stats = sim_stats.rename(columns={"match wins":"Sim Match Wins","match losses":"Sim Match Losses","game wins":"Sim Game Wins","game losses":"Sim Game Losses","game win %":"Sim Game Win %"})

#combine original data with simulated data
combined_data = team_stats.merge(sim_stats,on="Team Name")

#calculate some deltas simmed vs actual
combined_data['Actual Minus Sim Game Win %'] = combined_data['Game Win %'] - combined_data['Sim Game Win %']
combined_data['Actual Minus Sim Match Wins'] = combined_data['Match Wins'] - combined_data['Sim Match Wins']

#order results
combined_data = combined_data[['League','Season','Team Name','Match Wins','Match Losses','Game Wins','Game Losses','Game Win %','Sim Match Wins','Sim Match Losses','Sim Game Wins','Sim Game Losses','Sim Game Win %','Actual Minus Sim Match Wins','Actual Minus Sim Game Win %']].sort_values(["League","Season","Match Wins","Game Win %"],ascending=[True,True,False,False])
combined_data
combined_data.to_csv('personal-python/simulateddata.csv', sep=',', encoding='utf-8',index=False)