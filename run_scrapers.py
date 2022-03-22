import os
import time

print("\n\n Starting ABC \n\n")
os.system(f'python3 abc_scraper.py')

time.sleep(1)

print("\n\n Starting SBS \n\n")
os.system(f'python3 sbs_scraper.py')

time.sleep(1)

print("\n\n Starting Graun \n\n")
os.system(f'python3 graun_scraper.py')