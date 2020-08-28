Introduction
------------

This project allows for the scraping of all necessary eVision datasets.  These include Google Trends data, CDC ILI data, and WHO data.

This was developed using Python 3.7.x on MacOS, so no guarantees that it works on anything more outdated.

Requirements
------------

The libraries that are required for this module are:

* pandas
* pytrends
* googletrans
* selenium
* rpy2

The libraries that are recommended for this module (and are used in the source code):

* os
* datetime

Your computer will also require an installation of Google Chrome in order for selenium to work.  For the chrome driver attached to the file, your Google Chrome will need to be Version 85.x.  Information on your Chrome's version can be found under:

Customize and control Google Chrome --> Help --> About Google Chrome

If you have a version < 85.x, you can update it or download the corresponding version of the chrome driver at this link: https://chromedriver.chromium.org/. You will also need to download a different chromedriver to replace with the existing one in this folder if you do not have MacOS.

Installation
------------

If you do not have these packages currently installed, they can easily be installed using the pip install <insert library> command on your console (requires package like anaconda).

Notes
-----

If using WindowsOS, you will need to change "`/`" characters to "`\`" characters to account for the difference in paths with Windows and Mac.  Also, as mentioned earlier, download a new version of chromedriver if using Windows or Linux.  Then, simply repalce it with the chromedriver that exists in the "evision_scraper" folder.
