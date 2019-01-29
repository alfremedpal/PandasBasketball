# PandasBasketball
PandasBasketball is a small module intended to scrape data from [basketball-reference](https://www.basketball-reference.com/) and convert it to useful pandas data structures, such as data frames, for future analytical purposes. The use of jupyter notebooks is encouraged.

# Installation
There's really no installation per se, just download the folder named 'PandasBasketball' and place it on the directory where you will be using the jupyter notebook. That's it.
You can then import it to your jupyter environment:
```
from PandasBasketball import pandasbasketball as pb
```

## Requirements
Please make sure you meet the following rquirements:
- Python 3.6+
- requests
- pandas
- Beautiful Soup 4

All the requirements can easily be met with the installation of the [Anaconda](https://www.anaconda.com/download/) distribution.

# Usage
## Players
Inside a player's page on the basketball-reference website you can find several tables, and most of these tables can be obtained as a pandas data frame by calling `get_player(player, stat)`. The 'player' refers to the name of the html file used by basketball-reference inside the url, and the 'stat' means the type of table.

The currently supported tables are:
- Per Game (`per_game`)
- Totals (`totals`)
- Per 36 Minutes (`per_minute`)
- Per 100 Poss (`per_poss`)
- Advanced (`advanced`)
- Playoffs Per Game (`playoffs_per_game`)
- Playoffs Totals (`playoffs_totals`)
- Playoffs Per 36 Minutes (`playoffs_per_minute`)
- Playoffs Per 100 Poss (`playoffs_per_poss`)
- Playoffs Advanced (`playoffs_advanced`)

The rest of the tables will come in the future.

### Example
To get the 'Per Game' table for LeBron James you would do something like this:
```
df = pb.get_player("jamesle01", "per_game")
```

### Optional Arguments
The `get_team()` method supports two optional arguments:
- numeric -- boolean
- s_index -- boolean

### Considerations
- The resulting data frame **does not** include the table's footer.
- The resulting data frame will have the same column names as the table's header but it will not have a set index. To set the 'Season' column as index set the argument `s_index` to `True`. 
- The columns will be of type 'object', so in order to perform arithmetic functions on them you will need to convert them to numeric. You can do something like this:
```
lbj_pg = pb.get_player("jamesle01", "per_game")
lbj_pg[lbj_pg.columns] = lbj_pg[lbj_pg.columns].apply(pd.to_numeric, errors="ignore")
```
Or you cant set the optional argument `s_index` to True

## Player by season
You can get a player's stats by season by calling `get_player_season(player, season)`.
**NOTE:** Please read *Known Issues*

## Teams
You can call a team's seasons table with `get_team(name)`. The argument 'name' is the team's three-letter abbreviation (e.g. OKC, BKN).

### Example
To get OKC's table:
```
df = pb.get_team("OKC")
```

# Future
Fix known issues mainly

# Known Issues
- Players that did not play certain seasons for whatever reason (e.g. Michael Jordan, Magic Johnson) will get shifted values.
- `get_player_season` **wil not work** if a player missed a game.