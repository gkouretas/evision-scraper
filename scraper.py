# coding: utf-8
# necessary libraries
import pandas as pd
import os
import time
import random
import zipfile
from pytrends.request import TrendReq
from datetime import datetime
from googletrans import Translator
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

def create_dir(dir):
    if not os.path.exists(dir): # checks to ensure no duplicate directories exist (shouldn't ever happen)
        os.makedirs(dir) # creates directory
    return dir

def dir_exists(dir): # checks to see if file downloaded before resuming
    while(True):
        if os.path.exists(dir): # resumes when .csv is downloaded to desired directory
            break

def chromeSetUp():
    chromeOptions = Options()
    if bool(os.environ.get("GOOGLE_CHROME_BIN")): chromeOptions.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chromeOptions.headless = True
    chromeOptions.add_argument("--disable-dev-shm-usage")
    chromeOptions.add_argument("--no-sandbox")
    # webdriver executes chrome and goes to flunet app
    try:
        PATH = os.getcwdb().decode() + '/chromedriver'
        driver = webdriver.Chrome(PATH, options=chromeOptions)
    except Exception:
        driver = webdriver.Chrome(os.environ.get("CHROMEDRIVER_PATH"), options=chromeOptions)
    return driver

def directory(): # creates necessary directory for
    dir_loc = os.getcwdb().decode() # gets current directory
    dir_name = 'Database ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    dir = create_dir(dir_loc + '/' + dir_name) # sends name to create_dir() to create main directory that will store everything
    return dir

def trends_data(dir):
    dir = create_dir(dir + '/google_trends') # adds directory for google trends
    level = ['national', 'state', 'metropolitan']
    for area in level:
        print("Scraping " + area + " level data")
        trends_scrape(area, dir + '/' + area, pd.read_csv('data/{}.csv'.format(area))['Name'].tolist(), pd.read_csv('data/{}.csv'.format(area))['Code'].tolist(), pd.read_csv('data/{}.csv'.format(area))['Primary Language'].tolist())
        print(area + " level data scraping complete")

def trends_scrape(area, dir, names, codes, language):
    date_range = 'today 5-y' # time period which google trends wants to extract data
    create_dir(dir) # adds directory for corresponding level
    for area_count in range(0, 5): # for testing
    # for area_count in range(0, len(codes)): # use range(0, len(codes) or len(names)) to cycle through all area codes; loops through all areas
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
                    print('Extracting search term ' + terms[search_count % len(terms)] + ' from ' + names[area_count] + ' at ' + datetime.now().strftime('%H:%M:%S'))
                    print(codes[area_count])
                    start = time.time()
                    pytrends.build_payload(kw_list= [terms[search_count % len(terms)]], timeframe = date_range, geo = codes[area_count]) # sends parameters to google trends
                    ggl = pytrends.interest_over_time() # extracts google terms table
                    ggl = ggl.drop(columns = 'isPartial') # eliminates columns that are labeled 'isPartial'
                    area_dir = create_dir(dir + '/' + names[area_count]) # adds directory for area
                    ggl.to_csv(area_dir + '/GGL{}{}Weekly.csv'.format(codes[area_count], en_terms[search_count % len(terms)].replace(" ", ""))) # generating csv in area's directory
                    search_count += 1 # incrementing search count
                    print('Scraping finished (Time elapsed: ' + str(round(time.time() - start, 1)) + ' sec.)')
                except Exception:
                    # increments search count to skip over failed search result.
                    # will occur when there is not sufficient google trends data
                    search_count += 1
                    print('Scraping failed; insufficient search data for given search term')
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

def cdcwho(dir):
    print("Scraping CDC ILI and WHO NREVSS Data")
    dir = create_dir(dir + '/cdc_who_data' + '/United States') # creates directory for cdc/who data
    driver = chromeSetUp()
    start = time.time()
    driver.get("https://gis.cdc.gov/grasp/fluview/fluportaldashboard.html")
    while(True):
        try:
            disclaimer = driver.find_element_by_xpath("//button[@aria-label='Click to run the application.']")
            break
        except Exception:
            pass
    disclaimer.click()
    get_to_download(driver)
    nat_dir = create_dir(dir + '/National')
    params = {'behavior': 'allow', 'downloadPath': nat_dir}
    driver.execute_cdp_cmd('Page.setDownloadBehavior', params) # changes download path to chosen directory
    # download_data = driver.find_element_by_xpath("//button[@title='Download Data']")
    download_data = driver.find_element_by_xpath("//button[@aria-label='Click to download the data and leave the data download panel.']")
    download_data.click()
    print("National data downloaded")
    dir_exists(nat_dir + '/FluViewPhase2Data.zip')
    state_dir = create_dir(dir + '/State')
    params = {'behavior': 'allow', 'downloadPath': state_dir}
    driver.execute_cdp_cmd('Page.setDownloadBehavior', params) # changes download path to chosen directory
    get_to_download(driver)
    select_state = driver.find_element_by_id("5")
    select_state.click()
    select_all_regions = driver.find_element_by_xpath("//input[@ng-model='isAllRegions']")
    select_all_regions.click()
    download_data = driver.find_element_by_xpath("//button[@aria-label='Click to download the data and leave the data download panel.']")
    download_data.click()
    print("State data downloaded")
    dir_exists(state_dir + '/FluViewPhase2Data.zip')
    print("CDC/WHO data scraped (Time elapsed: " + str(round(time.time() - start)) + " sec.)")
    driver.close()
    extract_zip([nat_dir + '/FluViewPhase2Data.zip', state_dir + '/FluViewPhase2Data.zip'])

def get_to_download(driver):
    while(True):
        try:
            download = driver.find_element_by_xpath("//button[@aria-label='Click to download the flu data for the selected season.']")
            download.click()
            break
        except Exception:
            pass
    while(True):
        try:
            select_all_seasons = driver.find_element_by_xpath("//input[@ng-model='isAllSeasons']")
            select_all_seasons.click()
            break
        except Exception:
            pass

def extract_zip(list):
    for zip in list:
        with zipfile.ZipFile(zip, "r") as zip_ref:
            zip_ref.extractall(zip.split('/FluViewPhase2Data.zip')[0])
            os.remove(zip)

def whoflunet(dir):
    # reads list of countries that who flnet data exists for
    country_list = pd.read_csv('data/flunetcountrylist.csv')['Countries'].tolist()
    dir = create_dir(dir + '/cdc_who_data' + '/International')
    driver = chromeSetUp()
    # PATH = os.getcwdb().decode() + '/chromedriver'
    # # webdriver executes chrome and goes to flunet app
    # try:
    #     driver = webdriver.Chrome(PATH, options=chromeOptions)
    # except Exception:
    #     driver = webdriver.Chrome(os.environ.get("CHROMEDRIVER_PATH"), options=chromeOptions)
    driver.get("https://apps.who.int/flumart/Default?ReportNo=12")
    # scraping data
    count = 0
    prev_name = ''
    for name in country_list: # loops through list of countries
        if name == 'Montserrat': continue # montserrat is not compatible for some reason
        DOWNLOAD_PATH = create_dir(dir + '/' + name) # adds a directory for given country
        params = {'behavior': 'allow', 'downloadPath': DOWNLOAD_PATH}
        driver.execute_cdp_cmd('Page.setDownloadBehavior', params) # changes download path to chosen directory
        filter = Select(driver.find_element_by_id("lstSearchBy")) # finds html element where countries are
        filter.select_by_visible_text(name) # selects country for given iteration of loop
        if prev_name != '':
            filter.deselect_by_visible_text(prev_name) # deselects previous country used
        else: # selects date range for the first iteration (isn't needed after first time)
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
        print("Downloading data from " + name + " at " + datetime.now().strftime('%H:%M:%S'))
        # print(DOWNLOAD_PATH)
        start = time.time() # setting the time when the download starts
        while(True):
            try: # continually attempts while loading; will execute when spreadsheet gets loaded. time varies depending on how much data you're attempting to extract
                find_download = driver.find_element_by_id("ctl_ReportViewer_ctl05_ctl04_ctl00_ButtonLink") # finds dropdown element that allows for desired download format
                find_download.click() # selects dropdown
                download = driver.find_element_by_xpath("//a[@title='CSV (comma delimited)']") # finds element of desired download format (CSV in this case)
                download.click() # click button to download data
                break
            except Exception:
                end = time.time() # sets time of failure (failure meaning the page is still loading)
                if end - start > 300: # if page is still buffering after 5 minutes, it refreshes page
                    refresh(driver)
                    start = time.time() # resets start time to correspond with the page getting refreshed
                pass
        dir_exists(DOWNLOAD_PATH + '/FluNetInteractiveReport.csv')
        prev_name = name # stores value of name to deselect for next iteration
        print(name + "'s data has downloaded (Time elapsed: ~" + str(round(time.time() - start, 1)) + " sec.)")
        # count += 1
        # if count == 5:
        #     print('bye')
        #     break
    driver.close()

def refresh(driver): # refreshes webpage
    try:
        cancel = driver.find_element_by_link_text('Cancel')
        cancel.click()
    except Exception:
        pass
    print("Cancelled download: Process frozen. Refreshing page in five seconds.")
    time.sleep(5)
    driver.refresh()
    print("Refreshed")

dir = directory() # creates base directory
pytrends = TrendReq(hl='en-US', tz=360) # makes request to scrape google trends
trends_data(dir) # scrapes google trends data
cdcwho(dir) # scrapes cdc/who data
whoflunet(dir) # scrapes flunet data

# if [ "$(date +%u)" = 1 ]; then python scraper.py; fi
# this will run the program every monday
