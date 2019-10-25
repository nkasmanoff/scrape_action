#import dependencies 

import pandas as pd
from re import findall
import re


NBA = True
NFL = False
MLB = False

if NBA:
    sport = 'nba'
if MLB:
    sport = 'mlb'
if NFL:
    sport = 'nfl'

print("Getting Lines for ", sport)


todays_games = pd.read_html('https://www.actionnetwork.com/'+sport+'/public-betting')[0]



def get_teams(z,home=False,road=False):
    """
    Returns the home and away teams from the "ScheduledScheduled" column,
    which includes this weird code number that can be ignored. 
   
   """
    

    chars = findall('[A-Z]*',z) #finds all repititions of capitals letters, which would be a team abreviation. 
    
    teams = []

    for char in chars:
        if len(char)>1:
            teams.append(char)
        
    if road:
        road = teams[0]
        return road
    if home: 
        home = teams[1][0:-1]
        return home


todays_games.dropna(axis=1,inplace=True)
schedule_col = [col for col in todays_games.columns if 'Scheduled' in col][0]
pct_of_bets_col = [col for col in todays_games.columns if '% of Bets' in col][0]
todays_games['Road'] = todays_games[schedule_col].apply(lambda z: get_teams(z,road=True))
todays_games['Home'] = todays_games[schedule_col].apply(lambda z: get_teams(z,home=True))
for col in ['Open','Current',pct_of_bets_col]:
    #length = len(todays_games.Open.values[0])/2
    todays_games['Road ' + col] = todays_games[col].apply(lambda z: z[0:int(len(z)/2)])
  #  del todays_games[col]
    
todays_games['Home'] = todays_games[todays_games.columns[0]].apply(lambda z: get_teams(z,home=True))
for col in ['Open','Current',pct_of_bets_col]:
    #length = len(todays_games.Open.values[0])/2
    todays_games['Home ' + col] = todays_games[col].apply(lambda z: z[int(len(z)/2):])
    del todays_games[col]

todays_games = todays_games[todays_games.columns[1:]]

cols_clean = [col.split('Right')[0] for col in todays_games.columns]
todays_games.columns = cols_clean

#save today's data 
import datetime
today = datetime.datetime.now()
date = str(today.month)+'-'+ str(today.day)+'-'+str(today.year)
fname = sport+'lines'+date+'.xls'
todays_games.to_excel(fname,index=False)

print("Done! Check the folder where this file is run for today's ", sport, ' lines.')