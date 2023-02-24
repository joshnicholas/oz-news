# %%
from functions import sender, already_done, remove_common
import requests
from bs4 import BeautifulSoup as bs
import datetime
import pytz

import random
import time

# from dateutil import parser
# import dateparser


scrape_time = datetime.datetime.now().astimezone(pytz.timezone("Australia/Brisbane"))

# %%

starter = 'https://www.sbs.com.au/news/collection/top-stories'

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
'Accept-Language': "en-GB,en-US;q=0.9,en;q=0.8",
"Referer": 'https://www.google.com',
"DNT":'1'}

r = requests.get(starter, headers=headers)

# %%

soup = bs(r.text, 'html.parser')

box = soup.find('main', attrs={'role': 'main'})


stories = box.find_all('a', class_='SBS_ShelfItem')

print("Num stories: ", len(stories))

# %%

# sent = already_done("SBS")
# sent = already_done("ABC")

# print(stories[0])

counter = 0

page_rank = 1
for story in stories[:12]:
    # print("Starting: ", page_rank)
    if 'sbs.com.au' not in story['href']:

        urlo = 'https://www.sbs.com.au' + story['href']
    else:
        urlo = story['href']

    # if urlo not in sent:
    # print("Starting: ", page_rank)
    # print(urlo)
    heado = story.h2.text.strip()
    # print(heado)

    r2 = requests.get(urlo, headers=headers)

    story_soup = bs(r2.text, 'html.parser')

    body = story_soup.find('div', id = 'article-body-more')
    
    if body is None:
        body = story_soup.find('div', class_='article__body column')
    
    if body is None:
        body = story_soup.find('main', attrs={'role': 'main'})

    body = body.getText()
    body = remove_common(body)

    # print(body)

    dicto = {"publication": "SBS",

    'scraped_datetime': scrape_time,

    'headline': heado,
    'url': r2.url,
    'body': body.strip(),
    'page_rank': page_rank
    }

    senters = sender(dicto)

    if senters == True:
        counter += 1

    page_rank += 1

    rando = 1 * random.random()
    time.sleep(rando)

print("Num sent:", counter)

data = [{
    "Time": scrape_time,
    "Publication": "SBS",
    "Sent": counter
}]

import pandas as pd
log_path = 'data/scrape_log.csv'
old = pd.read_csv(log_path)
log = pd.DataFrame.from_records(data)

new_log = old.append(log)


with open(log_path, 'w') as f:
    new_log.to_csv(f, index=False, header=True)

# print(new_log)

# # %%

# %%
