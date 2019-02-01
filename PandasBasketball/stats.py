import pandas as pd
from bs4 import BeautifulSoup, NavigableString

from PandasBasketball.errors import TableNonExistent

def player_stats(request, stat, numeric=False, s_index=False):

    supported_tables = ["totals", "per_minute", "per_poss", "advanced",
                        "playoffs_per_game", "playoffs_totals", "playoffs_per_minute",
                        "playoffs_per_poss", "playoffs_advanced"]

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

    # Get the whole data frame
    df = get_data(table)

    if stat == "per_poss" or stat == "playoffs_per_poss":
        del df[None]
    elif stat == "advanced" or stat == "playoffs_advanced":
        del df["\xa0"]
    
    if numeric:
        df[df.columns] = df[df.columns].apply(pd.to_numeric, errors="ignore")
    if s_index:
        df.set_index("Season", inplace=True)

    return df

def player_gamelog(request):

    soup = BeautifulSoup(request.text, "html.parser")
    table = soup.find("table", class_="row_summable sortable stats_table")

    df = player_season_data(table)
    df.set_index("Rk", inplace=True)
    
    return df


def team_stats(request, team):
    
    soup = BeautifulSoup(request.text, "html.parser")
    table = soup.find("table", id=team)

    df = get_data(table)
    del df["\xa0"]

    return df

def player_season_data(table):

    columns = []
    heading = table.find("thead")
    heading_row = heading.find("tr")

    for x in heading_row.find_all("th"):
        columns.append(x.string)

    body = table.find("tbody")
    rows = body.find_all("tr")

    data = []
    for row in rows:
        temp = []
        th = row.find("th")
        td = row.find_all("td")
        temp.append(th.text)
        for v in td:
            # Fills the rest of the row with blanks
            if v.text == "Inactive" or v.text == "Did Not Play" or v.text == "Did Not Dress":
                temp.extend([""]*22)
                break
            else:
                temp.append(v.text)
        data.append(temp)
    
    # Get rids of the headers in the middle of the table
    for l in data:
        if len(l) != 30:
            data.remove(l)

    df = pd.DataFrame(data)
    df.columns = columns

    return df

def get_data(table):
    """
    It works, but it is kinda too much.
    Looks nicer in 'get_player_season_data',
    I'll change it when I have time, probably.
    """

    columns = []
    seasons = []
    stats = []
    data = []

    rows = table.find_all("tr")
    heading = table.find("thead")
    heading_row = heading.find("tr")

    for x in heading_row.find_all("th"):
            columns.append(x.string)
    for row in rows:
        a = row.find_all("a")
        for season in a:
            if season.string[0] == "1" or season.string[0] == "2":
                seasons.append(season.string)
            else: 
                continue
    for row in rows:
        line = row.find_all("td")   
        for value in line:             
            stats.append(value.text)    
    for i in range(len(seasons)): 
        data.append(seasons[i])         
        for j in range(len(columns) - 1):
            data.append(stats[j])
        del(stats[:len(columns) - 1])

    data = list(zip(*[iter(data)]*len(columns)))
    df = pd.DataFrame(data)
    df.columns = columns

    return df