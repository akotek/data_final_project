import sqlite3
import pandas as pd
import os

"""
This module finds connections between players and clybs using database.sqlite Matches table.
"""


def get_db_connection() -> sqlite3.Connection:
    return sqlite3.connect('database.sqlite')


def get_data(query) -> pd.DataFrame:
    conn = get_db_connection()
    df = pd.read_sql(query, conn)
    return df


def get_player_attributes():
    query = """SELECT *
               FROM Player_Attributes
            """
    df = get_data(query)
    return df


def get_team_attributes():
    query = """SELECT *
                   FROM Team_Attributes
                """
    df = get_data(query)
    return df


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    df.dropna(inplace=True)
    return df


def get_match_rosters() -> pd.DataFrame:
    home_team_query = """ Select home_team_api_id as team_id, home_player_1 as player1, home_player_2 as player2, home_player_3 as player3,
                                 home_player_4 as player4, home_player_5 as player5, home_player_6 as player6, home_player_7 as player7,
                                 home_player_8 as player8, home_player_9 as player9, home_player_10 as player10, home_player_11 as player11,
                                 strftime('%Y', date) as year
                          From Match
                        """
    df_home_team = get_data(home_team_query)
    away_team_query = """ Select away_team_api_id as team_id, away_player_1 as player1, away_player_2 as player2, away_player_3 as player3,
                                     away_player_4 as player4, away_player_5 as player5, away_player_6 as player6, away_player_7 as player7,
                                     away_player_8 as player8, away_player_9 as player9, away_player_10 as player10, away_player_11 as player11,
                                     strftime('%Y', date) as year
                              From Match
                            """
    df_away_team = get_data(away_team_query)
    df = pd.concat([df_away_team, df_home_team])
    df = clean_data(df)
    return df


def get_player_teams_data_frame_row(player, teams: set) -> pd.DataFrame:
    player_timeline = {int(player): [None] * 9}
    for team in teams:
        player_timeline[player][int(team[1]) - 2008] = int(team[0])
    columns = ['2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015', '2016']
    player_timeline_df = pd.DataFrame.from_dict(player_timeline, orient='index', columns=columns)
    return player_timeline_df


def get_player_team_table(df: pd.DataFrame) -> pd.DataFrame:
    player_team_dict = dict()
    count = 1
    for index, row in df.iterrows():
        print(count)
        for i in range(1, 12):
            if row['player' + str(i)] not in player_team_dict.keys():
                player_team_dict[row['player' + str(i)]] = set()
            player_team_dict[row['player' + str(i)]].add((row['team_id'], row['year']))
        count = count + 1
    player_team_df = pd.concat([get_player_teams_data_frame_row(player, teams) for player, teams
                                in player_team_dict.items()])
    return player_team_df


def create_player_team_table_csv():
    df = get_match_rosters()
    df = get_player_team_table(df)
    df.to_csv(os.path.join('csv', 'player_team_table.csv'), index_label='player_id')


def create_team_roster_csv():
    players_df = pd.read_csv(os.path.join('csv', 'player_team_table.csv'))
    teams_query = """Select team_api_id as team_id
                     From Team"""
    team_df = get_data(teams_query)
    for year in range(2008, 2017):
        team_df[year] = None
    team_df.set_index('team_id', inplace=True)
    for index, row in team_df.iterrows():
        for year in range(2008, 2017):
            team_df.at[index, year] = list(set(players_df[players_df[str(year)] == index]['player_id']))
    team_df.to_csv(os.path.join('csv', 'team_roster_table.csv'), index_label='team_id')



