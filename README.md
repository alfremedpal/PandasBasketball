# PandasBasketball
PandasBasketball is a small module intended to scrape data from [basketball-reference](https://www.basketball-reference.com/) and convert it to useful pandas data structures, such as data frames, for future analytical purposes. The use of jupyter notebooks is encouraged.

# Installation
```
pip install PandasBasketball
```

After installation you can then import it to your environment like this:
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
## :basketball: Players
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
The `get_player()` method supports two optional arguments:
- `numeric` - returns the data frame with its columns alreay converted to numeric
- `s_index` - returns the data frame with its column 'Season' as the index

Both are set to `False` by deault.

### Considerations
- The resulting data frame **does not** include the table's footer.
- The resulting data frame will have the same column names as the table's header but it will not have a set index. To set the 'Season' column as index set the argument `s_index` to `True`. 
- The columns will be of type 'object', so in order to perform arithmetic functions on them you will need to convert them to numeric. You can do something like this:
```
lbj_pg = pb.get_player("jamesle01", "per_game")
lbj_pg[lbj_pg.columns] = lbj_pg[lbj_pg.columns].apply(pd.to_numeric, errors="ignore")
```
Or you cant set the optional argument `numeric` to `True`.

## :basketball: Player Game Logs
You can get all of a player's games in a season by calling `get_player_gamelog(player, season)`. The `season` argument must be the last year in which the season took place. 

### Example
To get all of Kawhi Leonard's games during the 2017-2018 season:
```
df = pb.get_player_gamelog("leonaka01", "2018")
```

### Optional Arguments
The function `get_player_gamelog` supports one optional argument:
- `playoffs` - returns **only** the playoffs games if set to `True`

Set to `False` by default.

### Considerations
- The resulting data frame will use the 'Rk' column as its index
- The data frame does not include those rows which are just the header again
- If the player missed a game, the row will be filled with blanks ("")

## :basketball: Last n days
Get a data frame with all the season's available players stats over the last n days by calling `get_n_days(days)`.

### Example
```
df = pb.get_n_days(10)
```
### Optional arguments
`get_n_days` supports one optional argument: 
- `player` - returns a pandas series with the stats of the specifed player

`player` is set to `all` by default.

### Considerations
- The resulting data frame will have the column 'Players' as its index by default
- The data frame is in descending order by GmSc

## :basketball: Teams
You can call a team's seasons table with `get_team(name)`. The argument `name` is the team's three-letter abbreviation (e.g. OKC, MAV).

### Example
To get OKC's table:
```
df = pb.get_team("OKC")
```

## :basketball: Generate player code
Baskteball-reference uses a special code to build each player's unique html page. As of now, *almost* all functions in `PandasBasketball` expect that code to get the stats for the specified athlete. If you don't want to copy and paste the code from the URL into the function you can try calling `pb.generate_code(player)`. 

**Note:** this is not fully tested, so it is possible to get an incorrect code.

### Example
To get the player code for LeBron James:
```
pb.generate_code("LeBron James")
```
This will output `'jamesle01'` 

Using it with other functions:
```
df = pb.get_player(pb.generate_code("Donovan Mitchell"), "per_game")
```

This function is **not** case-sensitive or accent-sensitive. For example, you can retrieve Nikola Jokić's player code with the following:
```
pb.generate_code("nikola jokic")
```
This will output `'jokicni01'`


# Future
- ~~Make this project pip-installable~~
- Add support for the rest of tables on a player's page
- Implement function to obtain team stats per season
- ~~Implement function to get the last n days stats~~
- Implement function to obtain game results by date

# Contributions & Known Issues
If you notice an issue or want to contribute open an issue over at the [issues section](https://github.com/alfremedpal/PandasBasketball/issues).
