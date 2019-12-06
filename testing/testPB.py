from PandasBasketball import pandasbasketball as pb
import pandas as pd
from bs4 import BeautifulSoup as soup

df = pb.get_player("jamesle01", "per_game")

df.head()
