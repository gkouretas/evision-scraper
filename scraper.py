# coding: utf-8
# necessary libraries

from pytrends.request import TrendReq

from directory_setup import directory
from selenium_setup import chromeSetUp
from google_trends import trends_data
from case_data import who_nrevss, flumart

dir = directory() # creates base directory

pytrends = TrendReq(hl='en-US', tz=360) # makes request to scrape google trends
trends_data(dir, pytrends) # scrapes google trends data

driver = chromeSetUp()
# who_nrevss(dir, driver) # scrapes cdc/who data
flumart(dir, driver) # scrapes flunet data

# if [ "$(date +%u)" = 1 ]; then python scraper.py; fi
# this will run the program every monday
