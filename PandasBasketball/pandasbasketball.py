import requests
from bs4 import BeautifulSoup

from PandasBasketball.stats import player_stats
from PandasBasketball.errors import StatusCode404

BASE_URL = "https://www.basketball-reference.com"

def get_player(code, stat):
    """
    Returns a pandas dataframe with the player's stats
    \tKeyword arguments:
    \t\tcode -- the player's url code
    \t\tstat -- the stat table\n
    """

    #Building the url and making the request
    url = BASE_URL + f"/players/{code[0]}/{code}.html"
    r = requests.get(url)

    # If the page is not found, raise the error
    # else, return the data frame
    if r.status_code == 404:
        raise StatusCode404
    else:
        return player_stats(r, stat)


    """
    supported tables:
        - per_game    
        - totals      
        - per_minute  
        - per_poss    
        - advanced
        - playoffs_per_game    
        - playoffs_totals      
        - playoffs_per_minute  
        - playoffs_per_poss    
        - playoffs_advanced    
    """