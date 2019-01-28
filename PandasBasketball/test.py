import requests
import pandas as pd

from bs4 import BeautifulSoup, NavigableString, Comment
from selenium import webdriver

url = "https://www.basketball-reference.com/players/j/jamesle01.html"
r = requests.get(url)

soup = BeautifulSoup(r.text, "lxml")
comment_table = soup.find(text=lambda x: isinstance(x, NavigableString) and "per_poss" in x)
soup = BeautifulSoup(comment_table, "lxml")
table = soup.find("table", id="per_poss")

columns = []
seasons = []
stats = []
data = []

rows = table.find_all("tr")
    
# Getting the column names
heading = table.find("thead")
heading_row = heading.find("tr")

for x in heading_row.find_all("th"):
    columns.append(str(x.string))

columns.remove("None")

for row in rows:
    a = row.find_all("a")
    for season in a:
        if season.string[0] == "1" or season.string[0] == "2":
            seasons.append(season.string)
        else: 
            continue

# Getting the actual table values 
for row in rows:
    line = row.find_all("td", class_="right")
    for value in line:
        print(value)
        if value.string is None:
            break
        stats.append(value.string)
print(len(line))
# Joining all data into 'data'
for i in range(len(seasons)):
    data.append(seasons[i])
    for j in range(len(columns) - 1):
        try:
            data.append(stats[j])
        except IndexError:
            print("Hey")
    del(stats[:len(columns) - 1])


# Making a list of tuples
data = list(zip(*[iter(data)]*len(columns)))

# Builing the data frame
df = pd.DataFrame(data)
df.columns = columns

print(df)

