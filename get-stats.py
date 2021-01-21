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
#1/11 boosty boys scrim
urls.append('b399c2f1-14c1-4419-9b56-2dcba8038a63')
urls.append('9d053ab6-fd45-4e29-bd90-bdba4dec0629')
urls.append('70ef7a52-6014-4ec4-8f63-63dc526338e8')
urls.append('83518fa7-9bb7-41c0-b192-2c7f7e96ef40')
urls.append('5d3a843a-62c8-46a7-9bd3-c86e754e5a7d')
urls.append('09772d90-acc7-4692-8e2f-fbb81aaf110e')
urls.append('0f11948f-e73d-448d-9a14-bc687e77156c')
urls.append('37cb2c52-676a-4a07-a16f-3605e47beb6b')
#1/11 firestorm scrim
urls.append('d5559778-1a20-4388-9d9b-a7770573d4cd')
urls.append('fabd2bf6-8a6b-4921-a7a8-c545e408df94')
urls.append('93007698-f2b4-4d23-958f-4438153a2570')
urls.append('8db975aa-4ea9-4e65-a8b8-0a9c6b34ce31')
#1/13 firestorm scrim
urls.append('b76a4b9b-4ee5-4acf-932c-0fa552d3df07')
urls.append('4ba80221-4a36-4b3d-a11d-d808c3f51836')
urls.append('3c1bede4-0449-42ed-b4e6-9a20cb3cdc23')
urls.append('bfc92b44-3310-4bf1-99da-e4018b958f33')

#1/15 week 0 scrims (only our games)
urls.append('708f160c-bd3b-435f-aeb9-ac9c7eb618c9')
urls.append('b7b86822-30df-4652-b4d4-26df4b564e7e')
urls.append('02bcc596-2b0e-43d3-b594-086e1f689952')


#1/19 duluth scrim
urls.append('8646c892-b61c-4508-85ed-ea84debea4f6')
urls.append('9d379e43-1fa7-4dee-9fa4-b401cd7386ce')
urls.append('b40638dc-6b6f-4ca3-b904-33022cf33037')
urls.append('be52e085-e6df-4061-8931-af293f306da2')
urls.append('a75dd6d3-0d88-4da9-aea3-661207b2137e')
urls.append('e5baf9d9-499a-44a8-9063-39771bbe060b')
urls.append('a4dc8bec-643a-4cdc-8956-e0fdb39a87c6')
urls.append('f6a11545-62f6-474c-b92a-8da7a1e2d6f4')

#1/20 minneapolis scrim
urls.append('a1e6175c-435c-4a10-aa13-354745b96ff2')
urls.append('c313b774-aef0-4a4d-ba58-b7722f8697f5')
urls.append('774e81d0-7875-4b98-94ba-e65ebe98391e')
urls.append('8bf10bbe-9a9b-43c3-988d-d6c5c9187b16')
urls.append('7dc98c4e-6406-495c-9a3b-65c8a3e6b506')

#initalize summary dataframes

for url in urls:
    #print(url)

    #download playerfile
    playerfile = 'C:/Users/phil_/OneDrive/Documents/GitHub/rocket-league-stats/stat_files/PLAYER_'+url+'.csv'
    fullplayerurl = 'https://ballchasing.com/dl/stats/players/'+url+'/'+url+'-players.csv'
    download_file(url=fullplayerurl,filename=playerfile)

    #find my row
    playerdata = pd.read_csv(playerfile, sep=';')
    
    #override player names for consistency
    playerinputs = [
         playerdata['player name'].str.upper() == "ZIM"
         ,playerdata['player name'].str.upper() == "DICEY #WE<3ZBRUH"
         ,playerdata['player name'].str.upper() == "TARR_RL DEMOS ONLY"
         ,True
    ]
    playeroutputs = [
        "iChaotic"
        ,"Dicey"
        ,"Tarr_RL"
        ,playerdata['player name']
    ]
    
    playerdata['player name'] = np.select(playerinputs,playeroutputs)
    #playerdata
    
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
    teaminputs = [
         teamdata['team name'].str.upper() == "DULUTH", teamdata['team name'].str.upper() == 'SPIRIT'
        ,teamdata['team name'].str.upper() == "ROCHESTER", teamdata['team name'].str.upper() == 'RIFF'
        ,teamdata['team name'].str.upper() == "MINNETONKA", teamdata['team name'].str.upper() == 'BONZERS'
        ,teamdata['team name'].str.upper() == "HIBBING", teamdata['team name'].str.upper() == 'WARDENS'
        ,teamdata['team name'].str.upper() == "MINNEAPOLIS", teamdata['team name'].str.upper() == 'PRODIGIES'
        ,teamdata['team name'].str.upper() == "ST. CLOUD", teamdata['team name'].str.upper() == "ST CLOUD", teamdata['team name'].str.upper() == 'SOAR'
        ,teamdata['team name'].str.upper() == "ST. PAUL", teamdata['team name'].str.upper() == "ST PAUL", teamdata['team name'].str.upper() == 'KINGPINS'
        ,teamdata['team name'].str.upper() == "BLOOMINGTON", teamdata['team name'].str.upper() == 'URSAS', teamdata['team name'].str.upper() == 'BOOSTY BOYS' 
        ,teamdata['team name'].str.upper() == "BURNSVILLE", teamdata['team name'].str.upper() == 'FIRESTORM'
        ,teamdata['team name'].str.upper() == "BEMIDJI", teamdata['team name'].str.upper() == 'BEAVERS'
        ,True
    ]
    teamoutputs = [
        "DULUTH","DULUTH"
        ,"ROCHESTER","ROCHESTER"
        ,"MINNETONKA","MINNETONKA"
        ,"HIBBING","HIBBING"
        ,"MINNEAPOLIS","MINNEAPOLIS"
        ,"ST. CLOUD","ST. CLOUD","ST. CLOUD"
        ,"ST. PAUL","ST. PAUL","ST. PAUL"
        ,"BLOOMINGTON","BLOOMINGTON","BLOOMINGTON"
        ,"BURNSVILLE","BURNSVILLE"
        ,"BEMIDJI","BEMIDJI"
        ,teamdata['team name']
    ]
    
    teamdata['team name'] = np.select(teaminputs,teamoutputs)
    #teamdata

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
gameresults = teamsummary[['color','Game','Result','team name']]
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

#drop column team name_x
playersummary = playersummary.drop(columns='team name_x')
#rename column team name_y to team name
playersummary.rename(columns={'team name_y':'team name'},inplace=True)
playersummary