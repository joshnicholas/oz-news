import os
import time

print("\n\n Starting ABC \n\n")
os.system(f'python3 scrapers/abc_scraper.py')

time.sleep(1)

print("\n\n Starting SBS \n\n")
os.system(f'python3 scrapers/sbs_scraper.py')

time.sleep(1)

print("\n\n Starting Graun \n\n")
os.system(f'python3 scrapers/graun_scraper.py')

time.sleep(1)

print("\n\n Starting NewsCom \n\n")
os.system(f'python3 scrapers/newscom_scraper.py')