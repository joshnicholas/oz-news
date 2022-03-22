# %%
from functions import sender, already_done
import requests
from bs4 import BeautifulSoup as bs
import datetime
import pytz

import random
import time

from dateutil import parser
import dateparser


scrape_time = datetime.datetime.now().astimezone(pytz.timezone("Australia/Brisbane"))

# %%

starter = 'https://www.theguardian.com/au'

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
r = requests.get(starter, headers=headers)

# %%

soup = bs(r.text, 'html.parser')

box = soup.find('div', attrs={'data-id': 'au-alpha/news/regular-stories'})

# print(box)

stories = box.find_all('div', class_='fc-item')

print("Num stories: ", len(stories))

# %%

sent = already_done("The Guardian")

# print(stories[0])

page_rank = 1
for story in stories[:20]:
    print("Starting: ", page_rank)
    urlo = story.a['href']
    # print(urlo)
    heado = story.a.text
    # print(heado)

    if urlo not in sent:

        print(urlo)
        print(heado)

        r2 = requests.get(urlo, headers=headers)

        story_soup = bs(r2.text, 'html.parser')

        body = story_soup.find('div', id = 'maincontent')

        body = body.getText()

        # print(body)

        dicto = {"publication": "The Guardian",

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
# # # %%

# # %%

# %%
