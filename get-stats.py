import pandas as pd
import numpy as np
import os
import requests



#download method
def download_file(url, filename):
    ''' Downloads file from the url and save it as filename '''
    # check if file already exists
    if not os.path.isfile(filename):
        print('Downloading File')
        response = requests.get(url)
        # Check if the response is ok (200)
        if response.status_code == 200:
            # Open file and write the content
            with open(filename, 'wb') as file:
                # A chunk of 128 bytes
                for chunk in response:
                    file.write(chunk)
    else:
        print('File exists')

# all of my available replays
# https://ballchasing.com/?title=&player-name=pcmcd&season=&min-rank=&max-rank=&map=&replay-after=&replay-before=&upload-after=&upload-before=

#download single file location

urls = []
urls.append('708f160c-bd3b-435f-aeb9-ac9c7eb618c9')
urls.append('b7b86822-30df-4652-b4d4-26df4b564e7e')
urls.append('02bcc596-2b0e-43d3-b594-086e1f689952')



#initalize summary dataframes

for url in urls:
    #print(url)

    #download playerfile
    playerfile = 'C:/Users/phil_/OneDrive/Documents/GitHub/rocket-league-stats/stat_files/PLAYER_'+url+'.csv'
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
    teamfile = 'C:/Users/phil_/OneDrive/Documents/GitHub/rocket-league-stats/stat_files/TEAM_'+url+'.csv'
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
teamsummary


#game summary
gameresults = teamsummary[['Team','Game','Result']]
#gameresults

playersummary = pd.merge(playersummary, gameresults, on=['Team', 'Game'])
playersummary['Count'] = 1
playersummary