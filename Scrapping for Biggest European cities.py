from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import sqlalchemy

cities = ['Berlin', 'Hamburg', 'London', 'Manchester', 'Barcelona']

list_for_df = []

for city in cities:
   
    url = f'https://en.wikipedia.org/wiki/{city}'
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')

    response_dict = {}
    response_dict['city'] = soup.select(".firstHeading")[0].get_text()
    response_dict['country'] = soup.select(".infobox-data")[0].get_text()
    
    if soup.select_one('th.infobox-header:-soup-contains("Population")'):
        response_dict['population'] = soup.select_one('th.infobox-header:-soup-contains("Population")').parent.find_next_sibling().find(text=re.compile(r'\d+'))
    response_dict['lat'] = soup.select(".latitude")[0].get_text()
    response_dict['long'] = soup.select(".longitude")[0].get_text()
    
    list_for_df.append(response_dict)

cities_df = pd.DataFrame(list_for_df)

cities_df['lat'] = cities_df['lat'].str.split('″').str[0].str.replace('°', '.', regex=False).str.replace('′', '', regex=False).str.replace('N', '00', regex=False)
cities_df['long'] = cities_df['long'].str.split('″').str[0].str.replace('°', '.', regex=False).str.replace('′', '', regex=False).str.replace('E', '00', regex=False)

