import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from requests import api

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
    
    return(api_response)
result = get_rank_from_api(form_url('steam','76561198040589211'))

result['data'].keys()

result['data']['segments'][3].keys()
result['data']['segments'][3]['metadata']['name']


result['data']['segments'][3]['stats'].keys()
result['data']['segments'][3]['stats']['rating']['value']


df = pd.DataFrame.from_dict(result['data']['segments'])
df.head()