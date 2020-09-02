Introduction
------------

This project allows for the scraping of all necessary eVision datasets.  These include Google Trends data, CDC ILI data, and WHO data.

This was developed using Python 3.7.x on MacOS, so no guarantees that it works on anything more outdated.

This code can be used both on your desktop, or deployed on a Heroku server.  

Requirements
------------

The libraries that are required for this module are:

* pandas
* pytrends
* googletrans
* selenium
* rpy2

Your computer will also require an installation of Google Chrome in order for selenium to work.  For the chrome driver attached to the file, your Google Chrome will need to be Version 85.x.  Information on your Chrome's version can be found under:

Customize and control Google Chrome -> Help -> About Google Chrome

If you have version < 85.x of Google Chrome, or are not on MacOS, you can download the version of the chromedriver that corresponds to your console <a href="https://chromedriver.chromium.org/">here</a>.  You will also need to download a different chromedriver to replace with the existing one in this folder if you do not have MacOS.  Once downloaded, simply replace the chromedriver provided in this repo with the one you downloaded.

Installation
------------

If you do not have these packages currently installed, they can easily be installed using the pip install -r requirements.txt command on your console.

Notes
-----

If you are not on MacOS, you may need to change the paths to find some of the files in the code (namely the spreadsheet paths, changing "`/`" characters to "`\`").

If you are deploying this scraper on Heroku, you need to add some necessary additions in order for compatibility with selenium.  Under "Config Vars" in your app's settings, you will need to add the following:

KEY: CHROMEDRIVER_PATH  VALUE: /app/.chromedriver/bin/chromedriver
KEY: GOOGLE_CHROME_BIN  VALUE: /app/.apt/usr/bin/google-chrome

You will also need to add the corresponding buildpacks, which can be done by entering the following links into your buildpacks:

https://github.com/heroku/heroku-buildpack-google-chrome
https://github.com/heroku/heroku-buildpack-chromedriver

More information on this can be found at <a href="https://www.youtube.com/watch?v=Ven-pqwk3ec">this</a> YouTube video
