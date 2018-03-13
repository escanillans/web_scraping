# Written By: Niko Escanilla
# Goal: Extract NFL Standings and put into a table

# Download all necessary packages
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np

# get the web page
page = requests.get("http://www.espn.com/nfl/standings/_/group/league")
soup = BeautifulSoup(page.content, 'html.parser')

# 0 = league names, 1 = league data
nflTables = soup.find_all(class_= "Table2__tbody")

# get list of all team names (in current order)
teams = nflTables[0].find_all(class_="hide-mobile")
teams = [t.get_text() for t in teams]

print(teams)

# get column standing names (first = team name, remove this)
colNames = soup.find_all(class_="Table2__th")
colNames = [n.get_text() for n in colNames]
colNames.pop(0)
print(colNames)

# create an empty dataframe to return 
df = pd.DataFrame(index = teams, columns = colNames)

# get stats per team
statsPerTeam = nflTables[1].select(".Table2__tr")

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
df.to_csv("sportsData/nflStandings.csv", index = True)