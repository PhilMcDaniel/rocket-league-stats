import pandas as pd
import numpy as np
import os
import requests
import time
from download import download_file
import ast

# all of my available replays
# https://ballchasing.com/?title=&player-name=pcmcd&season=&min-rank=&max-rank=&map=&replay-after=&replay-before=&upload-after=&upload-before=

urls = []
#read file with games
with open("games.txt",encoding="utf8") as file_object:
    lines = file_object.readlines()
for line in lines:
    line = line.rstrip()
    if line[0:1] =='#':
        pass
    else:
        #append row to list of lists
        urls.append(ast.literal_eval(line))
#print(urls)


#initalize summary dataframes

for url in urls:
    #print(url)

    #download playerfile
    #playerfile = 'C:/Users/mcdan/OneDrive/Documents/GitHub/rocket-league-stats/stat_files/PLAYER_'+url[0][0]+'.csv'
    playerfile = 'C:/Users/phil_/OneDrive/Documents/GitHub/rocket-league-stats/stat_files/PLAYER_'+url[0][0]+'.csv'
    fullplayerurl = 'https://ballchasing.com/dl/stats/players/'+url[0][0]+'/'+url[0][0]+'-players.csv'
    download_file(url=fullplayerurl,filename=playerfile)

    #find my row
    playerdata = pd.read_csv(playerfile, sep=';')
    
    #override player names for consistency
    playerinputs = [
         playerdata['player name'].str.upper() == "ZIM"
         ,playerdata['player name'].str.upper() == "DICEY #WE<3ZBRUH"
         ,playerdata['player name'].str.upper() == "TARR_RL DEMOS ONLY"
         ,playerdata['player name'].str.upper() == "M8ITSNATE"
         ,playerdata['player name'].str.upper() == "KING WASTEE"
         ,playerdata['player name'].str.upper() == "EL BLOOP :D"
         ,playerdata['player name'].str.upper() == "TIBBLE TOT"
         ,playerdata['player name'].str.upper() == "TIBBLE THOT"
         ,playerdata['player name'].str.upper() == "CZCHR."
         ,playerdata['player name'].str.upper() == "KHARON (JUST DRANK REDBULL)"
         ,playerdata['player name'].str.upper() == "KHARON"
         ,playerdata['player name'].str.upper() == "KHARON (DRANK REDBULL)"
         ,playerdata['player name'].str.upper() == "ANGELMXB"
         ,playerdata['player name'].str.upper() == "DCURT-"
         ,playerdata['player name'].str.upper() == "NOHEADTOAST"
         ,playerdata['player name'].str.upper() == "PACE. 1/10"
         ,playerdata['player name'].str.upper() == "MN | PACE."
         ,playerdata['player name'].str.upper() == "DAL | TKD247"
         ,playerdata['player name'].str.upper() == "FANTASTIC MR AMBROSIA"
         ,playerdata['player name'].str.upper() == "DJCJ (NEW CONTROLLER)"
         ,playerdata['player name'].str.upper() == "JEDI PADAWAN TIBBLE THOT"
         ,playerdata['player name'].str.upper() == "AMBROSIA277"
         ,playerdata['player name'].str.upper() == "CHIK'NDINONUGGIEZ"
         ,playerdata['player name'].str.upper() == "CALSTER | POWER WASHED"
         ,playerdata['player name'].str.upper() == "CALSTER | SPACE HEATER"
         ,playerdata['player name'].str.upper() == "VELTREE"
         ,True
    ]
    playeroutputs = [
        "iChaotic"
        ,"Dicey"
        ,"Tarr_RL"
        ,'ItsNate'
        ,'RAPTOR Wastee'
        ,'El Bloop'
        ,'tibbles'
        ,'tibbles'
        ,'CzechR.'
        ,'Kharon'
        ,'Kharon'
        ,'Kharon'
        ,'XBAgent1'
        ,'DcuRt'
        ,'ToastSlow'
        ,'Pace.'
        ,'Pace.'
        ,'Tkd247'
        ,'ambrosia'
        ,'DJCJ.'
        ,'tibbles'
        ,'ambrosia'
        ,"Chik'n"
        ,'Calster'
        ,'Calster'
        ,'Veltri'
        ,playerdata['player name']
    ]
    
    playerdata['player name'] = np.select(playerinputs,playeroutputs)
    #playerdata
    
    #add column that has guid for game
    playerdata['Game'] = url[0][0]
    
    #add column for season match type
    playerdata['Match Type'] = url[2][0]

    #add column for week number
    playerdata['Week Number'] = url[1][0]
    
    #add column for game date
    playerdata['Game Date'] = url[4][0]

    #add column for league
    playerdata['League'] = url[5][0]
    
    #write back to csv
    playerdata.to_csv(playerfile, sep=';', encoding='utf-8',index=False)


    #download team file
    #teamfile = 'C:/Users/mcdan/OneDrive/Documents/GitHub/rocket-league-stats/stat_files/TEAM_'+url[0][0]+'.csv'
    teamfile = 'C:/Users/phil_/OneDrive/Documents/GitHub/rocket-league-stats/stat_files/TEAM_'+url[0][0]+'.csv'
    fullteamurl = 'https://ballchasing.com/dl/stats/teams/'+url[0][0]+'/'+url[0][0]+'-team-stats.csv'
    download_file(url=fullteamurl,filename=teamfile)

    teamdata = pd.read_csv(teamfile, sep=';')

    #add column to add team names for my team and opponents
    #teamdata['Team'] = np.where(teamdata['color'] != mycolor,'Opponent','Rochester Riff')


    #override team names for consistency
    teaminputs = [
         teamdata['team name'].str.upper() == "DULUTH", teamdata['team name'].str.upper() == 'SPIRIT', teamdata['team name'].str.upper() == 'SPIRITS'
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
        "SPIRIT","SPIRIT","SPIRIT"
        ,"RIFF","RIFF"
        ,"BONZERS","BONZERS"
        ,"WARDENS","WARDENS"
        ,"PRODIGIES","PRODIGIES"
        ,"SOAR","SOAR","SOAR"
        ,"KINGPINS","KINGPINS","KINGPINS"
        ,"URSAS","URSAS","URSAS"
        ,"FIRESTORM","FIRESTORM"
        ,"BEAVERS","BEAVERS"
        ,teamdata['team name']
    ]
    
    teamdata['team name'] = np.select(teaminputs,teamoutputs)
    
    #Create franchise name column to allow rollups across leagues
    teaminputs = [
         teamdata['team name'].str.upper() == "DULUTH", teamdata['team name'].str.upper() == 'SPIRIT', teamdata['team name'].str.upper() == 'SPIRITS'
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
        "DULUTH","DULUTH","DULUTH"
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
    
    teamdata['franchise name'] = np.select(teaminputs,teamoutputs)


    #add column that has guid for game
    teamdata['Game'] = url[0][0]

    #add column for season match type
    teamdata['Match Type'] = url[2][0]

    #add column for week number
    teamdata['Week Number'] = url[1][0]

    #add column for game date
    teamdata['Game Date'] = url[4][0]

    #add column for league
    teamdata['League'] = url[5][0]

    #add column for week number
    teamdata['Series Number'] = url[3][0]
    #teamdata

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