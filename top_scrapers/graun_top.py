import requests
import pandas as pd 
from bs4 import BeautifulSoup as bs 
import pytz
import datetime

from functions import top_sendo

today = datetime.datetime.now()

print(today)

csv_path = 'top_stuff/scrapes/graun/'

utc_now = pytz.utc.localize(datetime.datetime.utcnow())
brissie = utc_now.astimezone(pytz.timezone("Australia/Brisbane"))
bris_reverse_date = brissie.strftime('%Y-%m-%d')
bris_hour = brissie.strftime('%H')

scrape_time = datetime.datetime.now().astimezone(pytz.timezone("Australia/Brisbane"))

r = requests.get("https://www.theguardian.com/au")
soup = bs(r.text, 'html.parser')
items = soup.find_all("li", class_="most-popular__item")

counter = 1

sent = 0

for thing in items:

    print(thing)

    heado = thing.a.text

    urlo = thing.a['href']

    dicto = {"publication": "The Guardian",

    'scraped_datetime': scrape_time,
    'headline': heado,
    'url': urlo,
    'page_rank': counter
    }

    senters = top_sendo(dicto)
    counter += 1
    sent += 1
    # print(dicto)

print(f"{sent} sent.")

items = [{"Guardian Oz most viewed":f"{x.h3.text.strip()}"} for x in items]

df = pd.DataFrame(items)

df = df.T.reset_index()
headers = [f"{x}" for x in range(0,10)]
headers.insert(0, "What")
df.columns = headers

df['Date'] = bris_reverse_date
df['Hour'] = bris_hour


with open(f"{csv_path}{bris_reverse_date}.csv", "w") as f:
    df.to_csv(f, index=False)