
import requests
import pandas as pd 
from bs4 import BeautifulSoup as bs 
import pytz
import datetime

from functions import top_sendo

csv_path = 'top_stuff/scrapes/abc/'


utc_now = pytz.utc.localize(datetime.datetime.utcnow())
brissie = utc_now.astimezone(pytz.timezone("Australia/Brisbane"))
bris_reverse_date = brissie.strftime('%Y-%m-%d')
bris_hour = brissie.strftime('%H')

scrape_time = datetime.datetime.now().astimezone(pytz.timezone("Australia/Brisbane"))

r = requests.get("https://www.abc.net.au/news/")
soup = bs(r.text, 'html.parser')
div = soup.find("div", {"data-uri":"recommendation://collection/abc-news-homepage-sidebar"})
# recommendation://collection/abc-news-homepage-sidebar
items = div.find_all("a", {"data-component":"Link"})



counter = 1

sent = 0

for thing in items:

    # print(thing)

    heado = thing.text

    urlo = thing['href']

    dicto = {"publication": "ABC",

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



items = [{"ABC most viewed":f"{x.text.strip()}"} for x in items]

df = pd.DataFrame(items)

df = df.T.reset_index()
headers = [f"{x}" for x in range(0,5)]
headers.insert(0, "What")
df.columns = headers

df['Date'] = bris_reverse_date
df['Hour'] = bris_hour



with open(f"{csv_path}{bris_reverse_date}.csv", "w") as f:
    df.to_csv(f, index=False)