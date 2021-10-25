import os

from datetime import datetime

def create_dir(dir):
    if not os.path.exists(dir): # checks to ensure no duplicate directories exist (shouldn't ever happen)
        os.makedirs(dir) # creates directory
    return dir

def dir_exists(dir): # checks to see if file downloaded before resuming
    while(True):
        if os.path.exists(dir): # resumes when .csv is downloaded to desired directory
            break

def directory(): # creates necessary directory for
    dir_loc = os.getcwdb().decode() # gets current directory
    dir_name = 'Database ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    dir = create_dir(dir_loc + '/' + dir_name) # sends name to create_dir() to create main directory that will store everything
    return dir