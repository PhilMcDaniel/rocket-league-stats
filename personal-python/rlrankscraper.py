import requests
from bs4 import BeautifulSoup
import json
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
import pyodbc
import azure_config
from datetime import datetime
import uuid
import time


start = time.perf_counter()

driver = azure_config.driver
server = azure_config.server
database = azure_config.database
username = azure_config.username
password = azure_config.password

def form_url(platform,platformid):
    """Get the URL that needs to be parsed"""
    url = f"http://api.tracker.gg/api/v2/rocket-league/standard/profile/{platform}/{platformid}"
    return url
#form_url('steam','76561198040589211')

def get_rank_from_api(url):
    """sends request to API URL, returns data about player rank"""
    #read from chrome devtools network details
    headers = {
    'Accept': 'application/json, text/plain, */*'
    ,'Accept-Language': 'en'
    ,'DNT': '1'
    ,'Referer': 'https://rocketleague.tracker.network/'
    ,'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36'
    }
    api_response = requests.get(url,headers=headers)
    api_response = api_response.json()
    
    #get user info
    username = api_response['data']['platformInfo']['platformUserHandle']
    platform = api_response['data']['platformInfo']['platformSlug']
    platformid = api_response['data']['platformInfo']['platformUserIdentifier']
    user_info = [platform,platformid,username]
    response_list=[]
    response_list.append(user_info)
    for key in api_response['data']['segments']:
        #lifetime doesn't have normal keys
        if key['metadata']['name']=='Lifetime':
            pass
        else:
            playlist = key['metadata']['name']
            rank = key['stats']['tier']['metadata']['name']
            division = key['stats']['division']['metadata']['name']
            mmr = key['stats']['rating']['value']
            matchesplayed = key['stats']['matchesPlayed']['value']
            response_list.append([playlist,rank,division,mmr,matchesplayed])
    
    return  response_list
#get_rank_from_api(form_url('steam','76561198040589211'))


#load csv to list
with open('personal-python/league_player_ids.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)
#remove index = 0 (headers)
data.pop(0)

#loop through player id to scrape ranks
player_ratings=[]
for player in data:
    url=form_url(player[0],player[1])
    #print(url)
    try:
        player_ratings.append(get_rank_from_api(url))
    except:
        print(f"{player[0]}-{player[1]} was not found")

#load ranks to dataframe
#platform
#player_ratings[0][0][0]

#username
#player_ratings[0][0][2]
#flatten data so import to dataframe is smooth
flat_player_ratings = []
for player in player_ratings:
    #skip index 0 because it has player detail
    for playlist in player[1:]:
        flat_player_ratings.append([player[0][0],player[0][1],player[0][2],playlist[0],playlist[1],playlist[2],playlist[3],playlist[4]])


df = pd.DataFrame(flat_player_ratings,columns = ['platform','platformplayerid','player','playlist','rank','division','mmr','matches'])
#audit checking how many were scraped
#players = df['player'].unique()
#len(players)
#df['playlist'].unique()

# uuid for batch_id
batch_id = uuid.uuid4()

#write data to database
with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
    with conn.cursor() as cursor:
        cursor.execute("UPDATE [dbo].[PlayerRank] SET [IsLatest] = 'N' WHERE [IsLatest] = 'Y'")
        conn.commit()
        for index, row in df.iterrows():
            cursor.execute("INSERT INTO [dbo].[PlayerRank] ([ETL_DTM],[Platform],[PlatformPlayer_Id],[Player_Name],[Playlist],[Rank],[Division],[MMR],[IsLatest],[Batch_Id],[MatchesPlayed]) values(?,?,?,?,?,?,?,?,?,?,?)",datetime.now(),row['platform'],row['platformplayerid'],row['player'],row['playlist'],row['rank'],row['division'],row['mmr'],'Y',batch_id,row['matches'])
        conn.commit()

end = time.perf_counter()
print(f"Total execution time: {round((end - start),2)} seconds")

twosdf = df[df['playlist']=='Ranked Doubles 2v2'].sort_values(by='mmr', ascending=False)
threesdf = df[df['playlist']=='Ranked Standard 3v3'].sort_values(by='mmr', ascending=False)

#dataviz
ax = threesdf[['player','mmr']].head(50).plot.barh(x='player',y='mmr')
#invert so that y axis descends
ax.invert_yaxis()
plt.show()

