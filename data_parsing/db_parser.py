import sqlite3
import pandas as pd


def get_db_connection() -> sqlite3.Connection:
    return sqlite3.connect('database.sqlite')


def get_player_team_relationships():
    conn = get_db_connection()
    query = """SELECT date, home_team_api_id, away_team_api_id, home_player_1, home_player_2, home_player_3, home_player_4, home_player_5, home_player_6, home_player_7, home_player_8, home_player_9, home_player_10, home_player_11, away_player_1, away_player_2, away_player_3, away_player_4, away_player_5, away_player_6, away_player_7, away_player_8, away_player_9, away_player_10, away_player_11
               FROM Match
            """
    df = pd.read_sql(query, conn)
    df = df.dropna()
    team_player_linkage = dict()
    for index, row in df.iterrows():
        for i in range(3, 15):
            if row[i] in team_player_linkage:
                team_player_linkage[row[i]].append({'date': row[0], 'team_api_id': row[1]})
            else:
                team_player_linkage[row[i]] = []
        for i in range(15, len(row)):
            if row[i] in team_player_linkage:
                team_player_linkage[row[i]].append({'date': row[0], 'team_api_id': row[2]})
            else:
                team_player_linkage[row[i]] = []
    return team_player_linkage


def match_player_for_team(player_history: list, record_date):
    for item in player_history:
        pass


def get_players_df() -> pd.DataFrame:
    conn = get_db_connection()
    query = """SELECT a.*, c.height, c.weight, strftime('%Y', a.date) AS fifa_year, julianday(a.date) - julianday(c.birthday) AS player_age_in_days
               FROM Player_Attributes AS a
                INNER JOIN Player as c
                    ON a.player_api_id = c.player_api_id"""
    player_table = pd.read_sql(query, conn)
    player_table = player_table.drop(columns=['player_fifa_api_id'])
    player_table = player_table.dropna()
    team_player_linkage = get_player_team_relationships()
    player_table['team_api_id'] = player_table.apply(lambda row: match_player_for_team(team_player_linkage[row['player_api_id']], row['date']), axis=1)
    return player_table


def get_teams_df() -> pd.DataFrame:
    conn = get_db_connection()


get_players_df()
