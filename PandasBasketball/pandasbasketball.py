import requests
from bs4 import BeautifulSoup

from PandasBasketball.stats import player_stats, team_stats, player_gamelog, n_days
from PandasBasketball.errors import StatusCode404, TableNonExistent 

BASE_URL = "https://www.basketball-reference.com"

def generate_code(player):
    first, last = player.split(" ")
    
    first = first[:2]
    last = last[:5]
    
    return (last + first + "01").lower()


def get_player(player, stat, numeric=False, s_index=False):
    """
    Returns a pandas dataframe with the player's stats.
    \tKeyword arguments:
    \t\tcode -- the player's url code
    \t\tstat -- the stat table
    \tOptional arguments:
    \t\tnumeric -- boolean
    \t\ts_index -- boolean\n
    """

    # Building the url and making the request
    url = BASE_URL + f"/players/{player[0]}/{player}.html"
    r = requests.get(url)

    # If the page is not found, raise the error
    # else, return the data frame
    if r.status_code == 404:
        raise StatusCode404
    else:
        return player_stats(r, stat, numeric=numeric, s_index=s_index)

def get_player_gamelog(player, season, playoffs=False):
    """
    Returns all of the player's ganes in specified season as a data frame
    \tKeyword arguments:
    \t\tplayer -- the player's url code
    \t\tseason -- the season (e.g. 2018 for the 2017-18 season)
    """

    url = BASE_URL + f"/players/{player[0]}/{player}/gamelog/{season}"
    r = requests.get(url)

    if r.status_code == 404:
        raise StatusCode404
    else:
        return player_gamelog(r, playoffs=playoffs)

def get_team(team):
    """
    Returns a pandas dataframe with the team's stats.
    \tKeyword arguments:
    \t\tteam -- the team's three-letter abbreviation
    """

    url = BASE_URL + f"/teams/{team}"
    r = requests.get(url)

    if r.status_code == 404:
        raise StatusCode404
    else:
        return team_stats(r, team)

def get_n_days(days, player="all"):
    """
    Returns a pandas data frame with all the current 
    season's (avalaible) players ordered by their GmSc 
    over the last n days. Returns a pandas series if a 
    single player is specified
    \tKeyword arguments:
    \t\tdays -- number of days (1-60)
    """
    if days < 1 or days > 60:
        raise TableNonExistent
    else:
        url = BASE_URL + f"/friv/last_n_days.fcgi?n={days}"
        r = requests.get(url)
        return n_days(r, days, player=player)


    