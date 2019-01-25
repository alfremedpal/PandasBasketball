import pandas as pd
from bs4 import BeautifulSoup, NavigableString

from PandasBasketball.errors import TableNonExistent

def player_stats(request, stat):

    supported_tables = ["totals", "per_minute", "per_poss", "advanced",
                        "playoffs_per_game", "playoffs_totals", "playoffs_per_minute",
                        "playoffs_per_poss", "playoffs_advanced"]

    columns = []
    seasons = []
    stats = []
    data = []

    if stat == "per_game":
        soup = BeautifulSoup(request.text, "html.parser")
        table = soup.find("table", id="per_game")
    elif stat in supported_tables:
        soup = BeautifulSoup(request.text, "html.parser")
        comment_table = soup.find(text=lambda x: isinstance(x, NavigableString) and stat in x)
        soup = BeautifulSoup(comment_table, "html.parser")
        table = soup.find("table", id=stat)
    else:
        raise TableNonExistent

    rows = table.find_all("tr")
    
    # Getting the column names
    heading = table.find("thead")
    heading_row = heading.find("tr")

    for x in heading_row.find_all("th"):
        columns.append(x.string)
    
    if stat == "per_poss" or stat == "playoffs_per_poss": # Remove the extra empty columns on certain tables
        columns.remove(None)
    elif stat == "advanced" or stat == "playoffs_advanced":
        del(columns[19])
        del(columns[23])
        

    # Gettin the 'season' column values
    for row in rows:
        a = row.find_all("a")
        for season in a:
            if season.string[0] == "1" or season.string[0] == "2":
                seasons.append(season.string)
            else: 
                continue

    # Getting the actual table values 
    for row in rows:
        line = row.find_all("td")   
        for value in line:                          
            if value.string is None:    # Skips the empty columns
                continue
            stats.append(value.string)

    # Joining all data into 'data'
    for i in range(len(seasons)):
        data.append(seasons[i])
        for j in range(len(columns) - 1):
            data.append(stats[j])
        del(stats[:len(columns) - 1])

    # Making a list of tuples
    data = list(zip(*[iter(data)]*len(columns)))

    # Builing the data frame
    df = pd.DataFrame(data)
    df.columns = columns
    
    return df