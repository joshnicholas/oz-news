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

starter = 'https://www.news.com.au/national'

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
r = requests.get(starter, headers=headers)

# %%

soup = bs(r.text, 'html.parser')

# stories = soup.find_all('article',attrs={'data-nca-asset-type': 'story'})
stories = soup.find_all('article',class_='storyblock')

print("Num stories: ", len(stories))

# %%

sent = already_done("News")

# print(stories[0])

page_rank = 1
for story in stories[:10]:
    # print("Starting: ", page_rank)
    urlo = story.find("a", class_='storyblock_title_link')['href']
    # print(urlo)
    heado = story.h4.text
    # print(heado)

    if urlo not in sent:
        print("Starting: ", page_rank)
        # print(urlo)
        # print(heado)

        r2 = requests.get(urlo, headers=headers)

        story_soup = bs(r2.text, 'html.parser')

        body = story_soup.find('div', id = 'story-body')

        body = body.getText()

        # print(body)

        dicto = {"publication": "News",

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
# # # # %%

# # # %%

# # %%
