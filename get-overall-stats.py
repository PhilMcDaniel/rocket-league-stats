import pandas as pd
import numpy as np
import os
import requests
import time


directory = 'C:/Users/phil_/OneDrive/Documents/GitHub/rocket-league-stats/stat_files/'


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

#write overall to csv
teamsummary.to_csv('C:/Users/phil_/OneDrive/Documents/GitHub/rocket-league-stats/stat_files/summary/CLMNTeamSummary.csv', sep=';', encoding='utf-8',index=False)

#game summary
gameresults = teamsummary[['color','Game','Result','team name','Week Number','Series Number','Count','League']]

#get unique combinations
series_matchup = gameresults[['color','team name','Week Number','Series Number','League']].value_counts().reset_index(name='Games In Series')

#calculate wins for each combination
blue_wins = gameresults[['color','team name','Week Number','Series Number','League']].loc[(gameresults["Result"]=="Win") & (gameresults["color"]=="blue")].value_counts().reset_index(name='Blue Match Wins')
orange_wins = gameresults[['color','team name','Week Number','Series Number','League']].loc[(gameresults["Result"]=="Win") & (gameresults["color"]=="orange")].value_counts().reset_index(name='Orange Match Wins')
#join back to store result 
series_matchup = pd.merge(series_matchup,blue_wins,how="left" ,on=['Week Number','Series Number','League'])
series_matchup = pd.merge(series_matchup,orange_wins,how="left" ,on=['Week Number','Series Number','League'])

#fill in NaN with 0
series_matchup['Blue Match Wins'] = series_matchup['Blue Match Wins'].fillna(0)
series_matchup['Orange Match Wins'] = series_matchup['Orange Match Wins'].fillna(0)

#add column for color of series winner
series_matchup['Series Color Winner'] = np.where(series_matchup['Blue Match Wins'] > series_matchup['Orange Match Wins'],'blue','orange')
#add count column for series winner
series_matchup['Series Win Count'] = np.where(series_matchup['color_x'] == series_matchup['Series Color Winner'],1,0)
#add count column for series loser
series_matchup['Series Loss Count'] = np.where(series_matchup['color_x'] != series_matchup['Series Color Winner'],1,0)

#Add rows to account for forfeits. Each series forfeit needs two rows, 1 for winning team, 1 for losing team.
forfeits = []
forfeits.append(['blue','BLOOMINGTON','Week 3','Series 4','CLMN',0,'blue','BLOOMINGTON',0.0,'orange','ST. PAUL',0,'blue',1,0])
forfeits.append(['orange','ST. PAUL','Week 3','Series 4','CLMN',0,'orange','ST. PAUL',0.0,'blue','BLOOMINGTON',0,'blue',0,1])
forfeits.append(['blue','ST. CLOUD','Week 4','Series 1','CLMN',0,'blue','ST. CLOUD',0.0,'orange','HIBBING',0,'blue',1,0])
forfeits.append(['orange','HIBBING','Week 4','Series 1','CLMN',0,'orange','HIBBING',0.0,'blue','ST. CLOUD',0,'blue',0,1])

series_matchup = series_matchup.append(pd.DataFrame(forfeits, columns=series_matchup.columns),ignore_index=True)


#roll up to 1 row per team with sum of wins/losses
series_matchup = series_matchup.loc[series_matchup["Week Number"] !="Week 0"]

series_matchup = series_matchup.groupby("team name_x")['Series Win Count','Series Loss Count'].sum().sort_values(by=['Series Win Count'],ascending=False).reset_index()
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

#remove players who have retired, or been dropped from CLMN
players_to_remove = []
players_to_remove.append("Thermal")
#update dataframe to only include rows where the player name is not in the above list
playersummary = playersummary[~playersummary['player name'].isin(players_to_remove)]

playersummary
#write overall to csv
playersummary.to_csv('C:/Users/phil_/OneDrive/Documents/GitHub/rocket-league-stats/stat_files/summary/CLMNPlayerSummary.csv', sep=';', encoding='utf-8',index=False)

#get regular season rolled up player stats
regularseasonplayeroverallsummary = playersummary[['team name','player name','score','goals','assists','shots']].loc[playersummary['Match Type']=='Regular Season']
regularseasonplayeroverallsummary = regularseasonplayeroverallsummary.groupby(["team name","player name"])['score','goals','assists','shots'].mean().sort_values(by=['score','goals','assists','shots'],ascending=False).reset_index().round(2)
regularseasonplayeroverallsummary.to_csv('C:/Users/phil_/OneDrive/Documents/GitHub/rocket-league-stats/stat_files/summary/CLMNRegularSeasonOverallPlayerSummary.csv', sep=';', encoding='utf-8',index=False)
#regularseasonplayeroverallsummary

#get regular season rolled up team stats
regularseasonteamoverallsummary = teamsummary[['team name','score','goals','assists','shots']].loc[teamsummary['Match Type']=='Regular Season']
regularseasonteamoverallsummary = regularseasonteamoverallsummary.groupby(["team name"])['score','goals','assists','shots'].mean().sort_values(by=['score','goals','assists','shots'],ascending=False).reset_index().round(2)
regularseasonteamoverallsummary.to_csv('C:/Users/phil_/OneDrive/Documents/GitHub/rocket-league-stats/stat_files/summary/CLMNRegularSeasonOverallTeamSummary.csv', sep=';', encoding='utf-8',index=False)
regularseasonteamoverallsummary

#regular season games played
regularseasonplayergamesplayed = playersummary.loc[playersummary['Match Type']=='Regular Season']
#count distinct "game"
regularseasonplayergamesplayed = regularseasonplayergamesplayed.groupby(['player name']).Game.nunique().reset_index().sort_values(by=['player name'],ascending=True)
#name the new column
regularseasonplayergamesplayed.rename(columns={'Game':'Games Played'},inplace=True)
regularseasonplayergamesplayed
#write overall to csv
regularseasonplayergamesplayed.to_csv('C:/Users/phil_/OneDrive/Documents/GitHub/rocket-league-stats/stat_files/summary/CLMNRegularSeasonPlayerGamesPlayed.csv', sep=';', encoding='utf-8',index=False)