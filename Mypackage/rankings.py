#import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import requests

# @st.cache
def get_team_rankings(url):
    req=requests.get(url)
    content = req.text

    soup = BeautifulSoup(content)

    first_data = soup.find('tr', class_='rankings-block__banner') 

    first_pos = first_data.find('td', class_="rankings-block__banner--pos")
    first_team = first_data.find('span',class_="u-hide-phablet")
    first_matches = first_data.find('td', class_="rankings-block__banner--matches")
    first_points = first_data.find('td', class_="rankings-block__banner--points")
    first_rating = first_data.find('td', class_="rankings-block__banner--rating u-text-right")


    positions = []
    teams = []
    matches = []
    points = []
    ratings = []

    for i in first_pos:
        positions.append(i)
    for i in first_team:
        teams.append(i)
    for i in first_matches:
        matches.append(i)
    for i in first_points:
        points.append(i)
    for i in first_rating:
        i = i.replace(" ", '')
        i = i.replace("\n",'')
        ratings.append(i)
        break
        
    all_pos = soup.find_all('td',class_="table-body__cell table-body__cell--position u-text-right")

    for i in all_pos:
        for d in i:
            positions.append(d)

    all_teams = soup.find_all('td', class_="table-body__cell rankings-table__team")
    for i in all_teams:
        x = i.find('span', class_="u-hide-phablet")
        for d in x:
            teams.append(d)
            
    all_matches = soup.find_all('td', class_="table-body__cell u-center-text")
    x = 1
    for i in all_matches:
        for d in i:
            if x ==1:
                matches.append(d)
            if x==2:
                points.append(d)
            x+=1
            if x>2:
                x =1
    all_ratings = soup.find_all('td', class_="table-body__cell u-text-right rating")

    for i in all_ratings:
        for d in i:
            ratings.append(d)

    current_standings = pd.DataFrame()
            
    current_standings['Position'] = positions
    current_standings['Team'] = teams
    current_standings['Matches'] = matches
    current_standings['Points'] = points
    current_standings['Ratings'] = ratings
    return current_standings

###################################################
#### Mens T20 Rankings 

#@st.cache
def get_player_ranking(url):
    req=requests.get(url)
    content = req.text

    soup = BeautifulSoup(content)

    positions = []
    players = []
    teams = []
    ratings = []

    first_pos = soup.find("span", class_ = "rankings-block__pos-number")
    positions.append(str(first_pos.get_text()))

    first_player = soup.find("div", class_ = "rankings-block__banner--name-large")
    players.append(first_player.get_text())

    first_team = soup.find("div", class_ = "rankings-block__banner--nationality")
    team = first_team.get_text()
    team = team.replace(" ", "")
    team = team.replace("\n", "")
    teams.append(team)

    first_rating = soup.find("div", class_ = "rankings-block__banner--rating")
    ratings.append(first_rating.get_text())

    
    all_positions = soup.find_all("span", class_ = "rankings-table__pos-number")
    for i in all_positions:
        pos = i.get_text()
        pos = pos.replace(" ", "")
        pos = pos.replace("\n", "")
        positions.append(str(pos))

    all_players = soup.find_all("td", class_ = "table-body__cell rankings-table__name name")
    for i in all_players:
        players.append(i.find("a").get_text())

    all_teams = soup.find_all("span", class_ = "table-body__logo-text")
    for i in all_teams:
        teams.append(i.get_text())

    all_ratings = soup.find_all("td", class_ = "table-body__cell rating")
    for i in all_ratings:
        ratings.append(i.get_text())

    player_ranking = pd.DataFrame()
    player_ranking["Ranking"] = positions
    player_ranking["Player"] = players
    player_ranking["Team"] = teams
    player_ranking["Ratings"] = ratings
    
    return player_ranking