# %%
from functions import sender, already_done, remove_common
import requests
from bs4 import BeautifulSoup as bs
import datetime
import pytz

import random
import time

# from dateutil import parser


scrape_time = datetime.datetime.now().astimezone(pytz.timezone("Australia/Brisbane"))

# %%

starter = 'https://www.abc.net.au/news/'

headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
r = requests.get(starter, headers=headers)

# %%

soup = bs(r.text, 'html.parser')

box = soup.find('main', id = 'content')


stories = box.find_all(attrs={'data-component': 'ListItem'})

print("Num stories: ", len(stories))

# %%

# sent = already_done("ABC")

page_rank = 1
counter = 0
for story in stories[:20]:

    urlo = 'https://www.abc.net.au' + story.a['href']
    heado = story.h3.text.strip()

    # if urlo not in sent:
    print("Starting: ", page_rank)

    r2 = requests.get(urlo, headers=headers)

    story_soup = bs(r2.text, 'html.parser')

    story_body = story_soup.find('div', id = 'body')

    # pub_time = story_body.find('time', attrs={'data-component': 'Timestamp'})
    # pub_time = parser.parse(pub_time['datetime']).astimezone(pytz.timezone("Australia/Brisbane"))

    pars = story_body.find_all('p')
    pars = [x.text for x in pars]

    body = ' '.join(pars)
    body = remove_common(body)

    dicto = {"publication": "ABC",

    # 'published_datetime': pub_time,
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
    "Publication": "ABC",
    "Sent": counter
}]

import pandas as pd
log_path = 'data/scrape_log.csv'
old = pd.read_csv(log_path)
log = pd.DataFrame.from_records(data)

new_log = old.append(log)


with open(log_path, 'w') as f:
    new_log.to_csv(f, index=False, header=True)
# %%
