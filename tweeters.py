import twint
import pandas as pd 
import datetime 
import time 
import random

today = datetime.datetime.now()
yest = today - datetime.timedelta(days=1)
yest = datetime.datetime.strftime(yest, "%Y-%m-%d")

dicto = {"abcnews": "ABC", "GuardianAus": "guardian", "newscomauHQ": "newdotcom",
"SBSNews": "SBS", "smh": "smh"}

for keyo in dicto.keys():

  # Configure
  c = twint.Config()
  c.Username = keyo
  c.Since = yest
  # c.Limit = 3000

  c.Store_csv = True
  c.Output = f"news_tweets/{dicto[keyo]}_tweets.csv"

  twint.run.Search(c)

  wait = random.random() * 3

  print("Wait: ", wait)

  time.sleep(wait)