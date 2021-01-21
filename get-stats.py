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
urls.append('7dc98c4e-6406-495c-9a3b-65c8a3e6b506')
urls.append('8bf10bbe-9a9b-43c3-988d-d6c5c9187b16')
urls.append('774e81d0-7875-4b98-94ba-e65ebe98391e')
urls.append('c313b774-aef0-4a4d-ba58-b7722f8697f5')
urls.append('a1e6175c-435c-4a10-aa13-354745b96ff2')




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


    #override team names for consistency
    inputs = [
         teamdata['team name'].str.upper() == "DULUTH", teamdata['team name'].str.upper() == 'SPIRIT'
        ,teamdata['team name'].str.upper() == "ROCHESTER", teamdata['team name'].str.upper() == 'RIFF'
        ,teamdata['team name'].str.upper() == "MINNETONKA", teamdata['team name'].str.upper() == 'BONZERS'
        ,teamdata['team name'].str.upper() == "HIBBING", teamdata['team name'].str.upper() == 'WARDENS'
        ,teamdata['team name'].str.upper() == "MINNEAPOLIS", teamdata['team name'].str.upper() == 'PRODIGIES'
        ,teamdata['team name'].str.upper() == "ST. CLOUD", teamdata['team name'].str.upper() == "ST CLOUD", teamdata['team name'].str.upper() == 'SOAR'
        ,teamdata['team name'].str.upper() == "ST. PAUL", teamdata['team name'].str.upper() == "ST PAUL", teamdata['team name'].str.upper() == 'KINGPINS'
        ,teamdata['team name'].str.upper() == "BLOOMINGTON", teamdata['team name'].str.upper() == 'URSAS'
        ,teamdata['team name'].str.upper() == "BURNSVILLE", teamdata['team name'].str.upper() == 'FIRESTORM'
        ,teamdata['team name'].str.upper() == "BEMIDJI", teamdata['team name'].str.upper() == 'BEAVERS'
    ]
    outputs = [
        "DULUTH","DULUTH"
        ,"ROCHESTER","ROCHESTER"
        ,"MINNETONKA","MINNETONKA"
        ,"HIBBING","HIBBING"
        ,"MINNEAPOLIS","MINNEAPOLIS"
        ,"ST. CLOUD","ST. CLOUD","ST. CLOUD"
        ,"ST. PAUL","ST. PAUL","ST. PAUL"
        ,"BLOOMINGTON","BLOOMINGTON"
        ,"BURNSVILLE","BURNSVILLE"
        ,"BEMIDJI","BEAVERS"
    ]
    

    teamdata['team name'] = np.select(inputs,outputs)
    teamdata

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
#playersummary[playersummary['Game']=='af5b73e4-322f-43f2-9df9-7b160bfed936']

#take only wins
playerwins = playersummary[playersummary['Result'] == 'Win']
playerwins = playerwins[['color','score','Game']]

#find max score per color, game
mvpbygame = playerwins.groupby(['color','Game']).max()
#mvpbygame

#join back to playersummary on game, color, maxscore
playersummary = pd.merge(playersummary, mvpbygame,how='left', on=['color', 'Game'])
#add column for MPV where the score matches the max score from winning team
playersummary['MVP'] = np.where(playersummary['score_x'] == playersummary['score_y'],'Yes','No')

#drop column score_y
playersummary = playersummary.drop(columns='score_y')
#rename column score_x to score
playersummary.rename(columns={'score_x':'score'},inplace=True)
playersummary