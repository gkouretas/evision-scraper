import pandas as pd
import translators as ts
import time
import random

from datetime import datetime

from directory_setup import create_dir

def trends_data(dir, pytrends):
    dir = create_dir(dir + '/google_trends') # adds directory for google trends
    levels = ['national', 'state', 'metropolitan']
    column_names = []
    ggl_complete = pd.DataFrame() # complete frame for search terms of given area

    start_time = time.time()

    for area in levels:
        print("Scraping " + area + " level data")

        column_names, ggl_complete = trends_scrape(
            pytrends=pytrends,
            area=area, 
            dir=dir + '/' + area, 
            names=pd.read_csv(f'data/{area}.csv')['Name'].tolist(), 
            codes=pd.read_csv(f'data/{area}.csv')['Code'].tolist(), 
            language=pd.read_csv(f'data/{area}.csv')['Primary Language'].tolist(), 
            column_names=column_names, 
            ggl_complete=ggl_complete
        )

        print(area + " level data scraping complete")
    
    print(f'Google Trends data scraped. Time elapsed: {str(round((time.time() - start) * 60.0, 1))} minutes')

    ggl_complete.columns = column_names # column names
    pd.DataFrame(ggl_complete).to_csv('dataframe.csv')

    # pd.DataFrame(column_names).to_csv('column_names.csv')
    # google_data = ggl_complete.to_numpy() # numpy for given area
    # dates = ggl_complete.index.to_numpy()
    # pd.DataFrame(google_data).to_csv('google_search_data.csv')
    # pd.DataFrame(dates).to_csv('dates.csv')

def trends_scrape(pytrends, area, dir, names, codes, language, column_names, ggl_complete, date_range='today 5-y'):
    
    # pytrends -> object for data scraping
    # area -> level being searched (either national, state, or metropolitan)
    # dir -> root directory
    # names -> list of all subareas within main area
    # codes -> google trends codes for subareas
    # language -> primary languages for subareas
    # column_names -> list of areas and search terms (for database sorting)
    # ggl_complete -> google trends extracted data
    # date_range -> date range being searched (today 5-y is 5 years ago to current date) 

    create_dir(dir) # adds directory for corresponding level
    for area_count in range(0, len(codes)): # use range(0, len(codes) or len(names)) to cycle through all area codes; loops through all areas
        terms = ['flu', 'cough', 'fever', 'tamiflu', 'sore throat'] # terms that will be used for scraping
        terms.sort() # sorts terms in alphabetical order (not necessary)
        
        en_terms = terms # save array of english
        
        search_count = 0 # tracks searches for given area
       
        if area != 'metropolitan': # checks if area isn't metro, which indicates a potential different language
            if language[area_count] != 'en': # checks if area is not predominantly english speaking area
                
                print('Translating')
                terms = trans(language[area_count], terms) # sends terms to translating function, along with language code which terms need to translate to
       
        if bool(terms): # checks to make sure terms is not NoneType
            while(search_count < len(terms)): # cycles through search terms for given area
                try:
                    time.sleep(random.randrange(1,3))
                    print('Extracting search term ' + terms[search_count % len(terms)] + ' from ' + names[area_count] + ' at ' + datetime.now().strftime('%H:%M:%S'))
                    start = time.time()
                    pytrends.build_payload(kw_list= [terms[search_count % len(terms)]], timeframe = date_range, geo = codes[area_count]) # sends parameters to google trends
                    column_names.append((names[area_count] + '_' + terms[search_count % len(terms)]).replace(" ", "_"))
                    ggl = pytrends.interest_over_time() # extracts google terms table
                except Exception:
                    print('Google translate not working')
                    exit()
                try:
                    ggl = ggl.drop(columns = 'isPartial') # eliminates columns that are labeled 'isPartial'
                    area_dir = create_dir(dir + '/' + names[area_count]) # adds directory for area
                    ggl_complete = pd.concat([ggl_complete, ggl], axis = 1)
                    ggl.to_csv(area_dir + f'/GGL{codes[area_count]}{en_terms[search_count % len(terms)].replace(" ", "")}Weekly.csv') # generating csv in area's directory
                    print('Scraping finished (Time elapsed: ' + str(round(time.time() - start, 1)) + ' sec.)')
                    # success['Success Rate'][area_count - flag] += 1
                    # success[en_terms[search_count % len(terms)]][area_count - flag] = 'Success'
                    search_count += 1 # incrementing search count
                except Exception:
                    # increments search count to skip over failed search result.
                    # will occur when there is not sufficient google trends data
                    print('Scraping failed; insufficient search data for given search term')
                    column_names.pop() # remove name of area with insufficient search data
                    search_count += 1 # incrementing search count

        else:
            print('Primary language incompatible with Google Translate')

    return column_names, ggl_complete

def trans(lang, terms):
    translations = []

    for term in terms:
        translations.append(ts.google(term, to_language=lang)) 

    print(translations)
    return translations # returns translated terms