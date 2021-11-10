import pandas as pd
import numpy as np

# path = '/Users/georgekouretas/Documents/GitHub/evision-scraper/Database 2021-11-02 11:58:21/cdc_who_data/International/Afghanistan/FluNetInteractiveReport.csv'

# df = pd.read_csv(path, header=2)

# cases = df[['Country', 'Year', 'Week', 'SDATE', 'EDATE', 'SPEC_PROCESSED_NB', 
# 'AH1', 'AH1N12009', 'AH3', 'AH5', 'ANOTSUBTYPED', 'INF_A', 
# 'BYAMAGATA', 'BVICTORIA', 'BNOTDETERMINED', 'INF_B', 
# 'ALL_INF', 'ALL_INF2']]

# test = dict.fromkeys(pd.read_csv('data/national.csv').Code)
# test['AD'] = cases
# print(test)

path = 'Database 2021-11-02 11:42:16/cdc_who_data/United States/State/ILINet.csv'

df = pd.read_csv(path, header=1)
cases = df[['REGION', 'YEAR', 'WEEK', 'ILITOTAL']]

dict_data = dict.fromkeys(cases['REGION'][-55:-1])

idx = 0
inc = 52

while(True):
    if(cases['REGION'].iloc[idx] == cases['REGION'].iloc[idx+inc]):
        if not idx:
            for i in range(idx, idx+inc):
                dict_data[cases['REGION'].iloc[i]] = cases[['YEAR', 'WEEK', 'ILITOTAL']].iloc[i]
            idx += inc
        else:
            for i in range(idx, idx+inc):
                dict_data[cases['REGION'].iloc[i]] = pd.concat([dict_data[cases['REGION'].iloc[i]], cases[['YEAR', 'WEEK', 'ILITOTAL']].iloc[i]])            
            idx += inc
            if((idx + inc) == len(cases)): 
                for i in range(idx, idx+inc):
                    dict_data[cases['REGION'].iloc[i]] = pd.concat([dict_data[cases['REGION'].iloc[i]], cases[['YEAR', 'WEEK', 'ILITOTAL']].iloc[i]], ignore_index=True)
                break
    else:
        inc += 1
