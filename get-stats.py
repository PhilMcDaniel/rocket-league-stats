# all of my available replays
# https://ballchasing.com/?title=&player-name=pcmcd&season=&min-rank=&max-rank=&map=&replay-after=&replay-before=&upload-after=&upload-before=

#download single file location
#https://ballchasing.com/dl/stats/teams/8aee5a29-7792-4c86-8534-dce570ef214a/8aee5a29-7792-4c86-8534-dce570ef214a-team-stats.csv
from download import download_file
url = 'https://ballchasing.com/dl/stats/teams/8aee5a29-7792-4c86-8534-dce570ef214a/8aee5a29-7792-4c86-8534-dce570ef214a-team-stats.csv'
file = '8aee5a29-7792-4c86-8534-dce570ef214a-team.csv'
download_file(url=url,filename=file)

url = 'https://ballchasing.com/dl/stats/players/8aee5a29-7792-4c86-8534-dce570ef214a/8aee5a29-7792-4c86-8534-dce570ef214a-players.csv'
file = '8aee5a29-7792-4c86-8534-dce570ef214a-player.csv'
download_file(url=url,filename=file)