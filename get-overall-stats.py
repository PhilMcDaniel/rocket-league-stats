import pandas as pd
import numpy as np
import os
import requests
import time


directory = 'C:/Users/phil_/OneDrive/Documents/GitHub/rocket-league-stats/stat_files/'
#directory = 'C:/Users/mcdan/OneDrive/Documents/GitHub/rocket-league-stats/stat_files/'

playerli = []

# loop through player files and add to data frame
for filename in os.listdir(directory):
    if filename.startswith("PLAYER_"):
        #print(os.path.join(directory, filename))
        df = pd.read_csv(directory+filename, sep=';', index_col=None, header=0)
        playerli.append(df)
    else:
        continue
playersummary = pd.concat(playerli, axis=0, ignore_index=True)
#playersummary


teamli = []

# loop through team files and add to data frame
for filename in os.listdir(directory):
    if filename.startswith("TEAM_"):
        #print(os.path.join(directory, filename))
        df = pd.read_csv(directory+filename, sep=';', index_col=None, header=0)
        teamli.append(df)
    else:
        continue
teamsummary = pd.concat(teamli, axis=0, ignore_index=True)
teamsummary['Count'] = 1
teamsummary
#write overall to csv
teamsummary.to_csv('C:/Users/phil_/OneDrive/Documents/GitHub/rocket-league-stats/stat_files/summary/CLMNTeamSummary.csv', sep=';', encoding='utf-8',index=False)

#game summary
gameresults = teamsummary[['color','Game','Result','team name','Week Number','Series Number','Count']]

#get unique combinations
series_matchup = gameresults[['color','team name','Week Number','Series Number']].value_counts().reset_index(name='Games In Series')

#calculate wins for each combination
blue_wins = gameresults[['color','team name','Week Number','Series Number']].loc[(gameresults["Result"]=="Win") & (gameresults["color"]=="blue")].value_counts().reset_index(name='Blue Match Wins')
orange_wins = gameresults[['color','team name','Week Number','Series Number']].loc[(gameresults["Result"]=="Win") & (gameresults["color"]=="orange")].value_counts().reset_index(name='Orange Match Wins')
#join back to store result 
series_matchup = pd.merge(series_matchup,blue_wins,how="left" ,on=['Week Number','Series Number'])
series_matchup = pd.merge(series_matchup,orange_wins,how="left" ,on=['Week Number','Series Number'])

#fill in NaN with 0
series_matchup['Blue Match Wins'] = series_matchup['Blue Match Wins'].fillna(0)
series_matchup['Orange Match Wins'] = series_matchup['Orange Match Wins'].fillna(0)

#add column for color of series winner
series_matchup['Series Color Winner'] = np.where(series_matchup['Blue Match Wins'] > series_matchup['Orange Match Wins'],'blue','orange')
#add count column for series winner
series_matchup['Series Win Count'] = np.where(series_matchup['color_x'] == series_matchup['Series Color Winner'],1,0)
#add count column for series loser
series_matchup['Series Loss Count'] = np.where(series_matchup['color_x'] != series_matchup['Series Color Winner'],1,0)
series_matchup = series_matchup.loc[series_matchup["Week Number"]!="Week 0"].groupby("team name_x").sum().reset_index()
series_matchup

#write overall to csv
series_matchup.to_csv('C:/Users/phil_/OneDrive/Documents/GitHub/rocket-league-stats/stat_files/summary/CLMNSeriesRecord.csv', sep=';', encoding='utf-8',index=False)


playersummary = pd.merge(playersummary, gameresults, on=['color', 'Game'])
playersummary['Count'] = 1
#playersummary[playersummary['Game']=='af5b73e4-322f-43f2-9df9-7b160bfed936']

#take only wins for MVP calculation
playerwins = playersummary[playersummary['Result'] == 'Win']
playerwins = playerwins[['color','score','Game']]

#find max score per color, game
mvpbygame = playerwins.groupby(['color','Game']).max()
#mvpbygame

#join back to playersummary on game, color, maxscore
playersummary = pd.merge(playersummary, mvpbygame,how='left', on=['color', 'Game'])
#add column for MVP where the score matches the max score from winning team
playersummary['MVP'] = np.where(playersummary['score_x'] == playersummary['score_y'],'Yes','No')

#drop column score_y
playersummary = playersummary.drop(columns='score_y')
#rename column score_x to score
playersummary.rename(columns={'score_x':'score'},inplace=True)

#drop column team name_x
playersummary = playersummary.drop(columns='team name_x')
#rename column team name_y to team name
playersummary.rename(columns={'team name_y':'team name'},inplace=True)
playersummary
#write overall to csv
playersummary.to_csv('C:/Users/phil_/OneDrive/Documents/GitHub/rocket-league-stats/stat_files/summary/CLMNPlayerSummary.csv', sep=';', encoding='utf-8',index=False)