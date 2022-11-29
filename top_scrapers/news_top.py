import pandas as pd 
from bs4 import BeautifulSoup as bs 
import pytz
import datetime
import requests 

from selenium import webdriver 
from selenium.webdriver.chrome.options import Options

csv_path = 'top_stuff/scrapes/news/'

chrome_options = Options()
chrome_options.add_argument("--headless")

csv_path = 'top_stuff/scrapes/news/'


utc_now = pytz.utc.localize(datetime.datetime.utcnow())
brissie = utc_now.astimezone(pytz.timezone("Australia/Brisbane"))
bris_reverse_date = brissie.strftime('%Y-%m-%d')
bris_hour = brissie.strftime('%H')


driver = webdriver.Chrome(options=chrome_options)
start_url = "https://www.news.com.au/"
driver.get(start_url)

soup = bs(driver.page_source.encode("utf-8"), 'html.parser')

container = soup.find("div", class_="most-popular-content")
items = container.find_all("li")
items = [{"News most viewed":f"{x.text.strip()}"} for x in items]

df = pd.DataFrame(items)

df = df.T.reset_index()
headers = [f"{x}" for x in range(0,10)]
headers.insert(0, "What")
df.columns = headers

df['Date'] = bris_reverse_date
df['Hour'] = bris_hour

with open(f"{csv_path}{bris_reverse_date}.csv", "w") as f:
    df.to_csv(f, index=False)