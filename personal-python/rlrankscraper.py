import requests
from bs4 import BeautifulSoup
import json
import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
import pyodbc
import azure_config
from datetime import datetime,date
import uuid
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

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
    try:
        api_response = requests.get(url,headers=headers)
        api_response = api_response.json()
    except requests.exceptions.RequestException as e:
        print(e)
    
    #get user info
    try:
        username = api_response['data']['platformInfo']['platformUserHandle']
        platform = api_response['data']['platformInfo']['platformSlug']
        platformid = api_response['data']['platformInfo']['platformUserIdentifier']
        user_info = [platform,platformid,username]
        response_list=[]
        response_list.append(user_info)
    except:
        print(f'error getting platform info from JSON response for:{url}')
    
    for key in api_response['data']['segments']:
        #lifetime doesn't have normal keys
        try:
            if key['metadata']['name']=='Lifetime':
                pass
            else:
                playlist = key['metadata']['name']
                rank = key['stats']['tier']['metadata']['name']
                division = key['stats']['division']['metadata']['name']
                mmr = key['stats']['rating']['value']
                matchesplayed = key['stats']['matchesPlayed']['value']
                response_list.append([playlist,rank,division,mmr,matchesplayed])
        except:
            print(f'error getting player rank data for:{url}')

    return  response_list
#get_rank_from_api(form_url('steam','76561198040589211'))


#load csv to list
with open('personal-python/league_player_ids.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)
#remove index = 0 (headers)
data.pop(0)

#fully form URLs
url_list = []
for player in data:
    url=form_url(player[0],player[1])
    url_list.append(url)

#use threading to submit get requests and scrape data for all urls list of urls. store results in list of lists
player_ratings=[]
def runner():
    threads= []
    with ThreadPoolExecutor(max_workers=20) as executor:
        for url in url_list:
            try:
                threads.append(executor.submit(get_rank_from_api, url))
            except:
                print("failed adding thread")
        for task in as_completed(threads):
            try:
                player_ratings.append(task.result())
            except:
                print(f'failed storing thread result for:{url}')

runner()


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
end = time.perf_counter()
duration = round((end-start),4)
print(f"Total execution time: {duration} seconds")

#write data to database
#playerrank table
with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
    with conn.cursor() as cursor:
        cursor.execute("UPDATE [dbo].[PlayerRank] SET [IsLatest] = 'N' WHERE [IsLatest] = 'Y'")
        conn.commit()
        for index, row in df.iterrows():
            cursor.execute("INSERT INTO [dbo].[PlayerRank] ([ETL_DTM],[Platform],[PlatformPlayer_Id],[Player_Name],[Playlist],[Rank],[Division],[MMR],[IsLatest],[Batch_Id],[MatchesPlayed]) values(?,?,?,?,?,?,?,?,?,?,?)",datetime.now(),row['platform'],row['platformplayerid'],row['player'],row['playlist'],row['rank'],row['division'],row['mmr'],'Y',batch_id,row['matches'])
        conn.commit()

#insert row into batch table
with pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password) as conn:
    with conn.cursor() as cursor:
        cursor.execute("INSERT INTO [dbo].[Batch] ([Batch_Id],[BatchDate],[ETL_DTM],[BatchDurationSeconds]) values(?,?,?,?)",batch_id,date.today(),datetime.now(),duration)
        conn.commit()


#twosdf = df[df['playlist']=='Ranked Doubles 2v2'].sort_values(by='mmr', ascending=False)
#threesdf = df[df['playlist']=='Ranked Standard 3v3'].sort_values(by='mmr', ascending=False)

#dataviz
#ax = threesdf[['player','mmr']].head(50).plot.barh(x='player',y='mmr')
#invert so that y axis descends
#ax.invert_yaxis()
#plt.show()

