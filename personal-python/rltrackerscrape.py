import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from requests import api
from datetime import datetime

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

    platform = api_response['data']['platformInfo']['platformSlug']
    platform_handle = api_response['data']['platformInfo']['platformUserHandle']
    platform_handle_id = api_response['data']['platformInfo']['platformUserIdentifier']
    
    data = {}
    for row in api_response['data']['segments']:
        stat_type = [row][0]['type']
        #this row has different keys so skip it
        if stat_type == 'overview':
            continue
        season = [row][0]['attributes']['season']
        playlist_name = [row][0]['metadata']['name']
        rank = [row][0]['stats']['tier']['metadata']['name']
        division_name = [row][0]['stats']['division']['metadata']['name']
        season_matches_played = [row][0]['stats']['matchesPlayed']['value']
        win_streak = int([row][0]['stats']['winStreak']['displayValue'])
        rating_value = int([row][0]['stats']['rating']['value'])
        dt = str(datetime.now())
           
        data[(platform_handle_id,playlist_name,dt)] = {"platform_handle_id":platform_handle_id,"platform_handle":platform_handle,"datetime":dt,"platform":platform,"platform_handle":platform_handle,"stat_type":stat_type,"season":season,"playlist_name":playlist_name,"rank":rank,"division_name":division_name,"season_matches_played":season_matches_played,"win_streak":win_streak,"rating_value":rating_value}
    
    return(data)

result = get_rank_from_api(form_url('steam','76561198040589211'))


#result[('76561198040589211', 'Snowday', '2022-12-30 12:07:56.773688')]

df = pd.DataFrame.from_dict(result,orient='index' )
df.head()

#write to csv

#read file of platform / platform id

#main program to run these methods

#dag