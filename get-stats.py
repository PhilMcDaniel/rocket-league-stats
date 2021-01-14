from download import download_file
import pandas as pd
import numpy as np
import os

# all of my available replays
# https://ballchasing.com/?title=&player-name=pcmcd&season=&min-rank=&max-rank=&map=&replay-after=&replay-before=&upload-after=&upload-before=

#download single file location

urls = []
urls.append('37cb2c52-676a-4a07-a16f-3605e47beb6b')
urls.append('0f11948f-e73d-448d-9a14-bc687e77156c')
urls.append('09772d90-acc7-4692-8e2f-fbb81aaf110e')
urls.append('5d3a843a-62c8-46a7-9bd3-c86e754e5a7d')
urls.append('83518fa7-9bb7-41c0-b192-2c7f7e96ef40')
urls.append('70ef7a52-6014-4ec4-8f63-63dc526338e8')
urls.append('9d053ab6-fd45-4e29-bd90-bdba4dec0629')
urls.append('b399c2f1-14c1-4419-9b56-2dcba8038a63')

#initalize summary dataframes

for url in urls:
    #print(url)

    #download playerfile
    playerfile = 'stat_files/PLAYER_'+url+'.csv'
    fullplayerurl = 'https://ballchasing.com/dl/stats/players/'+url+'/'+url+'-players.csv'
    download_file(url=fullplayerurl,filename=playerfile)

    #find my row
    playerdata = pd.read_csv(playerfile, sep=';')
    
    myrows = playerdata[playerdata['player name'] == 'PCMcD']
    mycolor = myrows['color'].values[0]
    
    #add column to add team names for my team and opponents
    playerdata['Team'] = np.where(playerdata['color'] != mycolor,'Opponent','Rochester Riff')
    
    #add column that has guid for game
    playerdata['Game'] = url
    
    #write back to csv
    playerdata.to_csv(playerfile, sep=';', encoding='utf-8',index=False)


    #download team file
    teamfile = 'stat_files/TEAM_'+url+'.csv'
    fullteamurl = 'https://ballchasing.com/dl/stats/teams/'+url+'/'+url+'-team-stats.csv'
    download_file(url=fullteamurl,filename=teamfile)

    teamdata = pd.read_csv(teamfile, sep=';')

    #add column to add team names for my team and opponents
    teamdata['Team'] = np.where(teamdata['color'] != mycolor,'Opponent','Rochester Riff')

    #add column that has guid for game
    teamdata['Game'] = url

    #compare goals by each team to calculate winning team
    riffgoals = teamdata[teamdata['Team'] == 'Rochester Riff']
    riffgoals = riffgoals['goals'].values[0]

    opponentgoals = teamdata[teamdata['Team'] == 'Opponent']
    opponentgoals = opponentgoals['goals'].values[0]

    #compare the two values to calculate winning team
    if riffgoals > opponentgoals:
        winner = 'Rochester Riff'
    else:
        winner = 'Opponent'
    #print(winner)

    #set result column using winner from above
    teamdata['Result'] = ''
    teamdata.loc[teamdata['Team'] == winner, 'Result'] = 'Win'
    teamdata.loc[teamdata['Team'] != winner, 'Result'] = 'Loss'
    #teamdata

    #write back to csv
    teamdata.to_csv(teamfile, sep=';', encoding='utf-8',index=False)



directory = 'stat_files/'

playerli = []

# loop through player files and add to data frame
for filename in os.listdir(directory):
    if filename.startswith("PLAYER_"):
        #print(os.path.join(directory, filename))
        df = pd.read_csv('stat_files/'+filename, sep=';', index_col=None, header=0)
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
        df = pd.read_csv('stat_files/'+filename, sep=';', index_col=None, header=0)
        teamli.append(df)
    else:
        continue
teamsummary = pd.concat(teamli, axis=0, ignore_index=True)
teamsummary

#game summary
gameresults = teamsummary[['Team','Game','Result']]
#gameresults

playersummary = pd.merge(playersummary, gameresults, on=['Team', 'Game'])
playersummary