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
urls.append('147ef616-0ce1-4097-97dd-20b8b5f8f066')
urls.append('c7009825-6208-45c0-8be4-231625ec1a73')
urls.append('40d8ed32-f4dc-4d45-8230-634835369496')
urls.append('2193f1f1-7c8b-4af0-a56e-0c9be4a05122')
urls.append('979105a3-d736-41e2-b86f-fc8f95a78b05')
urls.append('c79da405-a413-47ca-8d39-d6c28e44842a')
urls.append('a6fd63d3-fd4e-4773-b728-8febac13ab85')
urls.append('d576c305-6485-47c8-9113-a26d2b431608')
urls.append('6acfc176-430b-4d99-b3f4-d3f720cf6f52')
urls.append('aa3a6016-4cea-4f11-9689-4f9c33abd2f0')
urls.append('1f6b28b4-11d1-49da-93aa-6d15141fdb45')
urls.append('d81ed040-9554-4932-b211-045d6a4a7b18')
urls.append('71175c21-caf3-4214-8db7-54840f352e29')
urls.append('5569316f-f11a-4973-abbd-164dca191abb')
urls.append('ccde16ef-58cc-4602-a932-dd9d2ec7cae6')
urls.append('f10724a3-156c-427c-8ec7-d0aea776555c')
urls.append('af5b73e4-322f-43f2-9df9-7b160bfed936')
urls.append('ba0f0aa7-3d7c-42b6-aa0d-2955b9e24b39')



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
    #mycolor = myrows['color'].values[0]
    
    #add column to add team names for my team and opponents
    #playerdata['Team'] = np.where(playerdata['color'] != mycolor,'Opponent','Rochester Riff')
    
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
    #teamdata['Team'] = np.where(teamdata['color'] != mycolor,'Opponent','Rochester Riff')

    #add column that has guid for game
    teamdata['Game'] = url

    #compare goals by each team to calculate winning team
    bluegoals = teamdata[teamdata['color'] == 'blue']
    bluegoals = bluegoals['goals'].values[0]

    orangegoals = teamdata[teamdata['color'] == 'orange']
    orangegoals = orangegoals['goals'].values[0]

    #compare the two values to calculate winning team
    if bluegoals > orangegoals:
        winner = 'blue'
    else:
        winner = 'orange'
    #print(winner)

    #set result column using winner from above
    teamdata['Result'] = ''
    teamdata.loc[teamdata['color'] == winner, 'Result'] = 'Win'
    teamdata.loc[teamdata['color'] != winner, 'Result'] = 'Loss'
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
gameresults = teamsummary[['color','Game','Result']]
#gameresults

playersummary = pd.merge(playersummary, gameresults, on=['color', 'Game'])
playersummary['Count'] = 1
playersummary