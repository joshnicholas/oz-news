# %%
from functions import sender, already_done
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

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
r = requests.get(starter, headers=headers)

# %%

soup = bs(r.text, 'html.parser')

box = soup.find('main', attrs={'role': 'main'})


stories = box.find_all('a', class_='SBS_ShelfItem')

print("Num stories: ", len(stories))

# %%

sent = already_done("SBS")

# print(stories[0])

page_rank = 1
for story in stories[:12]:
    # print("Starting: ", page_rank)
    if 'sbs.com.au' not in story['href']:

        urlo = 'https://www.sbs.com.au' + story['href']
    else:
        urlo = story['href']

    if urlo not in sent:
        print("Starting: ", page_rank)
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

        # print(body)

        dicto = {"publication": "SBS",

        'scraped_datetime': scrape_time,

        'headline': heado,
        'url': r2.url,
        'body': body.strip(),
        'page_rank': page_rank
        }

        sender(dicto)
        # print(dicto)

    page_rank += 1

    rando = 1 * random.random()
    time.sleep(rando)
# # %%

# %%
