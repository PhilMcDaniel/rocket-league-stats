from download import download_file
import pandas as pd
import numpy as np

# all of my available replays
# https://ballchasing.com/?title=&player-name=pcmcd&season=&min-rank=&max-rank=&map=&replay-after=&replay-before=&upload-after=&upload-before=

#download single file location
#https://ballchasing.com/dl/stats/teams/8aee5a29-7792-4c86-8534-dce570ef214a/8aee5a29-7792-4c86-8534-dce570ef214a-team-stats.csv

#download player file
url = 'https://ballchasing.com/dl/stats/players/8aee5a29-7792-4c86-8534-dce570ef214a/8aee5a29-7792-4c86-8534-dce570ef214a-players.csv'
file = 'stat_files/8aee5a29-7792-4c86-8534-dce570ef214a-player.csv'
gameguid = url[41:77]
download_file(url=url,filename=file)

#find my row
playerdata = pd.read_csv(file, sep=';')
myrows = playerdata[playerdata['player name'] == 'PCMcD']
mycolor = myrows['color'].values[0]
#mycolor

#add column to add team names for my team and opponents
playerdata['Team'] = np.where(playerdata['color'] != mycolor,'Opponent','Rochester Riff')
#playerdata

#add column that has guid for game
playerdata['Game'] = gameguid
#playerdata

#write back to csv
playerdata.to_csv(file, sep=';', encoding='utf-8',index=False)



#download team file
url = 'https://ballchasing.com/dl/stats/teams/8aee5a29-7792-4c86-8534-dce570ef214a/8aee5a29-7792-4c86-8534-dce570ef214a-team-stats.csv'
file = 'stat_files/8aee5a29-7792-4c86-8534-dce570ef214a-team.csv'
download_file(url=url,filename=file)

teamdata = pd.read_csv(file, sep=';')

#add column to add team names for my team and opponents
teamdata['Team'] = np.where(teamdata['color'] != mycolor,'Opponent','Rochester Riff')
#teamdata

#add column that has guid for game
teamdata['Game'] = gameguid
#teamdata

#write back to csv
teamdata.to_csv(file, sep=';', encoding='utf-8',index=False)