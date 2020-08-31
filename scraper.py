# coding: utf-8
# necessary libraries
import pandas as pd
import os
from pytrends.request import TrendReq
from datetime import datetime
from googletrans import Translator
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
# import rpy2.robjects as robjects
# import rpy2.robjects.packages as rpackages
# from rpy2.robjects.packages import importr
# from rpy2.robjects.vectors import StrVector

def directory(): # creates necessary directory for
    dir_loc = os.getcwdb().decode() # gets current directory
    dir_name = 'Database ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    dir = create_dir(dir_loc + '/' + dir_name) # sends name to create_dir() to create main directory that will store everything
    return dir

def chromeSetUp():
    chromeOptions = Options()
    chromeOptions.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chromeOptions.headless = True
    chromeOptions.add_argument("--disable-dev-shm-usage")
    chromeOptions.add_argument("--no-sandbox")
    return chromeOptions

def create_dir(dir):
    if not os.path.exists(dir): # checks to ensure no duplicate directories exist (shouldn't ever happen)
        os.makedirs(dir) # creates directory
    return dir

def trends_data(dir):
    dir = create_dir(dir + '/google_trends') # adds directory for google trends
    level = ['national', 'state', 'metropolitan']
    for area in level:
        trends_scrape(area, dir + '/' + area, pd.read_csv('data/{}.csv'.format(area))['Name'].tolist(), pd.read_csv('data/{}.csv'.format(area))['Code'].tolist(), pd.read_csv('data/{}.csv'.format(area))['Primary Language'].tolist())

def trends_scrape(area, dir, names, codes, language):
    time = 'today 5-y' # time period which google trends wants to extract data
    create_dir(dir) # adds directory for corresponding level
    # for area_count in range(0, 5): # for testing
    for area_count in range(0, len(codes)): # use range(0, len(codes) or len(names)) to cycle through all area codes; loops through all areas
        terms = ['flu', 'cough', 'fever', 'tamiflu'] # terms that will be used for scraping
        terms.sort() # sorts terms in alphabetical order (not necessary)
        en_terms = terms # save array of english
        search_count = 0 # tracks searches for given area
        if area != 'metropolitan': # checks if area isn't metro, which indicates a potential different language
            if language[area_count] != 'en': # checks if area is not predominantly english speaking area
                terms = fix_terms(language[area_count], terms) # sends terms to translating function, along with language code which terms need to translate to
        if bool(terms): # checks to make sure terms is note NoneType
            while(search_count < len(terms)): # cycles through search terms for given area
                try:
                    print('Extracting search term ' + terms[search_count % len(terms)] + ' from ' + names[area_count])
                    print(codes[area_count])
                    pytrends.build_payload(kw_list= [terms[search_count % len(terms)]], timeframe = time, geo = codes[area_count]) # sends parameters to google trends
                    ggl = pytrends.interest_over_time() # extracts google terms table
                    ggl = ggl.drop(columns = 'isPartial') # eliminates columns that are labeled 'isPartial'
                    area_dir = create_dir(dir + '/' + names[area_count]) # adds directory for area
                    ggl.to_csv(area_dir + '/GGL{}{}Weekly.csv'.format(codes[area_count], en_terms[search_count % len(terms)].replace(" ", ""))) # generating csv in area's directory
                    search_count += 1 # incrementing search count
                    print('Scraping successful')
                except Exception:
                    # increments search count to skip over failed search result.
                    # will occur when there is not sufficient google trends data
                    search_count += 1
                    print('Scraping unsuccessful; insufficient search data for given search term')
                    pass

def fix_terms(lang, terms):
    translator = Translator() # translate method
    try:
        terms = translator.translate(terms, dest=lang) # tries to translates terms to desired language, will be an object
    except Exception:
        return # returns NoneType if primary language of area is not supported by google trnaslate (there are a few like this)
    count = 0 # count for list indexing
    for trans in terms:
        terms[count] = trans.text # changes object to text
        count += 1
    return terms # returns translated terms

# def cdcwho(dir):


# def cdcwho(dir):
#     base = rpackages.importr('base')  # setting up r environment and installing necessary packages
#     utils = rpackages.importr('utils')
#     utils.chooseCRANmirror(ind = 1)
#     packnames = ('cdcfluview', 'hrbrthemes', 'tidyverse') # list of packages needed
#     names = [x for x in packnames if not rpackages.isinstalled(x)] # checks if packages are installed
#     if len(names) > 0:
#         utils.install_packages(StrVector(names)) # installs necessary packages if they are not already installed
#     dir = create_dir(dir + '/cdc_who_data' + '/United States') # creates directory for cdc/who data
#     robjects.r('''
#     cdc_scrape <- function(dir) {
#         library(cdcfluview)
#         library(hrbrthemes)
#         library(tidyverse)
#
#         #Get National ILI CSV and latest WHO CSV
#         national_ili <- ilinet("national")
#         national_who <- who_nrevss("national", years = 2018)
#         dir1 = paste(dir, "/ILIData_USA.csv", sep = "")
#         write.csv(national_ili, file = dir1, na = "")
#         dir2 = paste(dir, "/WHOData_USA.csv", sep = "")
#         write.csv(national_who, file = dir2, na = "")
#
#         #Get State ILI CSV and latest WHO CSV
#         state_ili <- ilinet("state")
#         dir3 = paste(dir, "/ILIData_States.csv", sep = "")
#         write.csv(state_ili, file = dir3, na = "")
#         state_who <- who_nrevss("state", years = 2018)
#         dir4 = paste(dir, "/WHOData_States.csv", sep = "")
#         write.csv(state_who, file = dir4, na = "") }
#         ''')
#
#         # r function that scrapes cdc data
#         # creates function called "cdc_scrape" that takes in needed directory
#
#     cdc_scrape = robjects.r['cdc_scrape'] # stores r function
#     cdc_scrape(dir) # calls r function, passing directory to place data

def whoflunet(dir):
    # reads list of countries that who flnet data exists for
    country_list = pd.read_csv('data/flunetcountrylist.csv')['Countries'].tolist()

    dir = create_dir(dir + '/cdc_who_data' + '/International')
    # turn on option of headless chrome (meaning browser will not open)

    chromeOptions = chromeSetUp()

    # chromeOptions = Options()
    # chromeOptions.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    # chromeOptions.headless = True
    # chromeOptions.add_argument("--disable-dev-shm-usage")
    # chromeOptions.add_argument("--no-sandbox")
    # get path to location of chrome driver (needed for selenium)
    # PATH = os.getcwdb().decode() + '/chromedriver'
    # webdriver executes chrome and goes to flunet app
    # try:
    #     driver = webdriver.Chrome(PATH, options=chromeOptions)
    # except Exception:
    driver = webdriver.Chrome(os.environ.get("CHROMEDRIVER_PATH"), options=chromeOptions)
    driver.get("https://apps.who.int/flumart/Default?ReportNo=12")
    # scraping data
    # count = 0
    prev_name = ''
    for name in country_list: # loops through list of countries
        DOWNLOAD_PATH = create_dir(dir + '/' + name) # adds a directory for given country
        params = {'behavior': 'allow', 'downloadPath': DOWNLOAD_PATH}
        driver.execute_cdp_cmd('Page.setDownloadBehavior', params) # changes download path to chosen directory
        filter = Select(driver.find_element_by_id("lstSearchBy")) # finds html element where countries are
        filter.select_by_visible_text(name) # selects country for given iteration of loop
        if prev_name != '': filter.deselect_by_visible_text(prev_name) # deselects previous country used
        year_from = Select(driver.find_element_by_id("ctl_list_YearFrom")) # finds html element where start year is
        year_from.select_by_visible_text("2015") # selects start year
        week_from = Select(driver.find_element_by_id("ctl_list_WeekFrom")) # finds html element where start week is
        week_from.select_by_visible_text("1") # selects start week
        year_to = Select(driver.find_element_by_id("ctl_list_YearTo")) # finds html element where end year is
        year_to.select_by_visible_text("2020") # finds html area where end year is
        week_to = Select(driver.find_element_by_id("ctl_list_WeekTo"))  # finds html element where end week is
        week_to.select_by_visible_text("53") # selects end week (doing 53 will give you most recent year)
        display_report = driver.find_element_by_name("ctl_ViewReport") # finds html element for button that loads spreadsheet
        display_report.click() # click button
        print("Downloading data from " + name)
        while(True):
            try: # continually attempts while loading; will execute when spreadsheet gets loaded. time varies depending on how much data you're attempting to extract
                find_download = driver.find_element_by_id("ctl_ReportViewer_ctl05_ctl04_ctl00_ButtonLink") # finds dropdown element that allows for desired download format
                find_download.click() # selects dropdown
                download = driver.find_element_by_xpath("//a[@title='CSV (comma delimited)']") # finds element of desired download format (CSV in this case)
                download.click() # click button to download data
                break
            except Exception:
                # time.sleep(5)
                pass
        while(True):
            if os.path.exists(DOWNLOAD_PATH + '/FluNetInteractiveReport.csv'): # resumes when .csv is downloaded to desired directory
                break
        prev_name = name # stores value of name to deselect for next iteration
        print(name + "'s data has downloaded")
        # count += 1
        # if count == 5:
        #     print('bye')
        #     break

dir = directory() # creates base directory
# cdcwho(dir) # scrapes cdc/who data
# while(True):
#     if datetime.now().strftime("%H:%M:%S") == '00:00:00' # will run program at midnight every day
whoflunet(dir) # scrapes flunet data
pytrends = TrendReq(hl='en-US', tz=360) # makes request to scrape google trends
trends_data(dir) # scrapes google trends data
