import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

def chromeSetUp():
    chromeOptions = Options()
    if bool(os.environ.get("GOOGLE_CHROME_BIN")): chromeOptions.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    # chromeOptions.headless = True
    chromeOptions.headless = False
    chromeOptions.add_argument("--disable-dev-shm-usage")
    chromeOptions.add_argument("--no-sandbox")
    # webdriver executes chrome and goes to flunet app
    try:
        PATH = './chromedriver' # path to location of your chromedriver goes here
        driver = webdriver.Chrome(PATH, options=chromeOptions)
    except Exception:
        driver = webdriver.Chrome(os.environ.get("CHROMEDRIVER_PATH"), options=chromeOptions)
    return driver

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