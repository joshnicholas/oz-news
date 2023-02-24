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

starter = 'https://www.smh.com.au/national'

headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36",
'Accept-Language': "en-GB,en-US;q=0.9,en;q=0.8",
"Referer": 'https://www.google.com',
"DNT":'1'}

r = requests.get(starter, headers=headers)

# %%

soup = bs(r.text, 'html.parser')

stories = soup.find_all('div',attrs={'data-testid': 'story-tile'})
# stories = soup.find_all('testid',class_='story-tile')

print("Num stories: ", len(stories))

# %%


# print(stories[0])

counter = 0
page_rank = 0

for story in stories[:10]:
    page_rank += 1
    try:
        # print("Starting: ", page_rank)
        # urlo = story.find("a", class_='storyblock_title_link')['href']
        urlo = 'https://www.smh.com.au' + story.a['href']

        heado = story.h3.text


        # if urlo not in sent:
        print("Starting: ", page_rank)
        # print(urlo)
        # print(heado)

        r2 = requests.get(urlo, headers=headers)

        # print(r2.text)

        story_soup = bs(r2.text, 'html.parser')

        body = story_soup.find('div', attrs={'data-testid': 'body-content'})

        body = body.getText()
        body = remove_common(body)
        # print(body)

        dicto = {"publication": "SMH",

        'scraped_datetime': scrape_time,

        'headline': heado,
        'url': r2.url,
        'body': body.strip(),
        'page_rank': page_rank
        }

        senters = sender(dicto)

        if senters == True:
            counter += 1

        rando = 1 * random.random()
        time.sleep(rando)
    except:

        continue

# print("Num sent:", counter)

data = [{
    "Time": scrape_time,
    "Publication": "SMH",
    "Sent": counter
}]

import pandas as pd
log_path = 'data/scrape_log.csv'
old = pd.read_csv(log_path)
log = pd.DataFrame.from_records(data)

new_log = old.append(log)


with open(log_path, 'w') as f:
    new_log.to_csv(f, index=False, header=True)
# # %%

print(new_log)
