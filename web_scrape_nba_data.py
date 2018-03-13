# Written By: Niko Escanilla
# Goal: Extract NBA Standings stats and put into table

# Download all necessary packages
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# Get the web page
page = requests.get("http://www.espn.com/nba/standings/_/group/league")
soup = BeautifulSoup(page.content, 'html.parser')

# 0 = league names, 1 = league data
nbaTables = soup.find_all(class_= "Table2__tbody")

# get list of all team names (in current order)
teams = nbaTables[0].find_all(class_="hide-mobile")
teams = [t.get_text() for t in teams]

print(teams)

# create an empty dataframe to return
df = pd.DataFrame(index = teams, columns = ['W', 'L', 'PCT', 'GB', 
                                            'HOME','AWAY','DIV',
                                           'CONF','PPG', 'OPP PPG',
                                           'DIFF','STRK','L10'])
df = df.fillna(0)

# get stats per team
statsPerTeam = nbaTables[1].select(".Table2__tr")

# extract data from each column for each team
# notice that each team has its own idx (data-idx = "")
idx = np.arange(0,len(statsPerTeam))

# for each team
for teamIdx in idx:
    currTeam = statsPerTeam[teamIdx].select(".stat-cell")
    
    # get their stats
    stats = [s.get_text() for s in currTeam]
    statColIdx = np.arange(0,len(stats))
    
    # for each stat
    for i in statColIdx:
        # add to df
        #df.ix[teamIdx, df.columns[i]] = stats[i]
        df.iloc[teamIdx, df.columns.get_loc(df.columns[i])] = stats[i]

print(df)

# save to csv
df.to_csv("sportsData/nbaStandings.csv", index = True)