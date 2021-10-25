import os
import zipfile
import time
import pandas as pd

from selenium.webdriver.support.ui import Select
from datetime import datetime

from directory_setup import *
from selenium_setup import refresh

def who_nrevss(dir, driver):
    print("Scraping WHO and NREVSS Data")
    dir = create_dir(dir + '/cdc_who_data' + '/United States') # creates directory for cdc/who data
    
    start = time.time()
    start_national = start
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

    download_data = driver.find_element_by_xpath("//button[@aria-label='Click to download the data and leave the data download panel.']")
    download_data.click()
    print("National data downloading")
    dir_exists(nat_dir + '/FluViewPhase2Data.zip')
    print("Download for national data complete (Time elapsed: " + str(round(time.time() - start_national)) + " sec.)")
    
    start_state = time.time()
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
    print("State data downloading")
    dir_exists(state_dir + '/FluViewPhase2Data.zip')
    print("Download for state data complete (Time elapsed: " + str(round(time.time() - start_state)) + " sec.)")      
    print("WHO/NRVESS data scraped (Time elapsed: " + str(round(time.time() - start)) + " sec.)")
    driver.close()
    
    print('Extracting .zip file')
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

def flumart(dir, driver):
    # reads list of countries that who flnet data exists for countries
    country_list = pd.read_csv('data/flumartcountrylist.csv')['Countries'].tolist()

    dir = create_dir(dir + '/cdc_who_data' + '/International')
    driver.get("https://apps.who.int/flumart/Default?ReportNo=12")
    # scraping data
    # count = 0
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
            year_from.select_by_visible_text("2016") # selects start year
            week_from = Select(driver.find_element_by_id("ctl_list_WeekFrom")) # finds html element where start week is
            week_from.select_by_visible_text("1") # selects start week
            year_to = Select(driver.find_element_by_id("ctl_list_YearTo")) # finds html element where end year is
            year_to.select_by_visible_text("2021") # finds html area where end year is
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