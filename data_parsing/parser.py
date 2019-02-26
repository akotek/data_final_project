import pandas as pd
import numpy as np
import os
import re
from sklearn.metrics.pairwise import cosine_similarity, manhattan_distances
import math

# Constants
# ------------------------------------------
UNWANTED_COLS = ['Special', 'International Reputation', 'Jersey Number', 'Joined', 'Release Clause']

REMOVE_WAGES = ['Value','Wage']


SIGNS_TO_CLEAN = ['€']
SIMPLE_PLAYER_VECTOR = ['Name', 'ID','Crossing', 'Finishing', 'HeadingAccuracy',
                        'ShortPassing', 'Volleys', 'Dribbling', 'Curve', 'FKAccuracy',
                        'LongPassing', 'BallControl', 'Acceleration', 'SprintSpeed', 'Agility', 'Reactions', 'Balance',
                        'ShotPower', 'Jumping', 'Stamina', 'Strength', 'LongShots', 'Aggression', 'Interceptions',
                        'Positioning', 'Vision', 'Penalties', 'Composure', 'Marking', 'StandingTackle', 'SlidingTackle']
SIMPLE_GK_PLAYER_VECTOR = [ 'Name', 'ID', 'Crossing', 'Finishing', 'HeadingAccuracy',
                        'ShortPassing', 'Volleys', 'Dribbling', 'Curve', 'FKAccuracy',
                        'LongPassing', 'BallControl', 'Acceleration', 'SprintSpeed', 'Agility', 'Reactions', 'Balance',
                        'ShotPower', 'Jumping', 'Stamina', 'Strength', 'LongShots', 'Aggression', 'Interceptions',
                        'Positioning', 'Vision', 'Penalties', 'Composure', 'Marking', 'StandingTackle', 'SlidingTackle','GKDiving'
                             'GKHandling', 'GKKicking', 'GKPositioning' ,'GKReflexes']

SIMPLE_PLAYER_VECTOR_NUMS_RATING = [ 'Weak Foot','Skill Moves','Height','Weight']


# ------------------------------------------

# Utils methods:
# ------------------------------------------


def relpath(path):
    return os.path.join(os.path.dirname(__file__), path)


def parse_height(ht_string):
    """
    convert height string to float
    :param ht_string: the string we want to convert
    :return: height in inches as a number
    """
    # format: 7' 0.0"
    if ht_string is np.nan:
        return ht_string
    ht_ = ht_string.split("'")
    ft_ = float(ht_[0])
    in_ = float(ht_[1].replace("\"",""))
    return (12*ft_) + in_


def parse_weight(wt_string):
    """
    remove all char in the string and return a float
    :param wt_string: the string we wnat to remove chars
    :return: a float number
    """
    if wt_string is np.nan:
        return wt_string
    num = re.findall(r'\d+', wt_string)
    return float(num[0])
# ------------------------------------------
# Player methods:
# ------------------------------------------


def pre_process(df: pd.DataFrame, goalkeeper=False):
    """
    cleaning the pandas data frame by removing duplicates name, unwanted columes
    :param df: the data fram pandas object
    :param goalkeeper: if true returns only goalkeepers, otherwise return other player type
    :return: the data frame after cleaning it up
    """
    df.drop(columns=UNWANTED_COLS, inplace=True)
    df.drop(columns=REMOVE_WAGES)
    df["Height"].apply(lambda x:parse_height(x))
    df["Weight"].apply(lambda x:parse_weight(x))
    print('totals values: ' + str(len(df['Name'])))
    if goalkeeper:
        df = df[df["Position"] == 'GK']
        df = df[SIMPLE_GK_PLAYER_VECTOR]
    else:
        df = df[df["Position"] != 'GK']
        df = df[SIMPLE_PLAYER_VECTOR]
    df = df.drop_duplicates(subset=['Name'])

    print('unique names: ' + str(len(df['Name'])))
    # df = df[SIMPLE_PLAYER_VECTOR]
    # df = df.dropna()
    print('after droping null values: ' + str(len(df['ID'])))
    df.set_index('ID',drop=True,inplace=True)

    return df


# ------------------------------------------
# COSINE DISTANCE:
# ------------------------------------------

def eval_cosine_dist(player1, player2):
    return cosine_similarity([player1], [player2])[0][0]


def eval_manhatan_dist(player1, player2):
    return manhattan_distances([player1], [player2])[0][0]


def compute_distance(all_players: pd.DataFrame, chosen_players: pd.DataFrame, distance_function=eval_cosine_dist)\
        -> dict:
    """
    :param all_players: All players
    :param chosen_players: Plyers of interest
    :return: dictionary of dictionaries:
                To access the distance of player1 from player2 do:
                player_distances[player1_id][player2_id]
    """
    all_players = all_players.drop(columns=['Name', 'ID']).dropna()
    chosen_players = chosen_players.drop(columns=['Name', 'ID']).dropna()
    player_distances = dict()
    for i, player1 in all_players.iterrows():
        player_distances[i] = dict()
        for j, player2 in chosen_players.iterrows():
            distance = distance_function(player1, player2)
            player_distances[i][j] = distance
            print(i, j, distance)
    return player_distances


def run_example(df):
    df = pre_process(df)
    # compute_distance(df, df)


# ------------------------------------------
# Usage example:
# ------------------------------------------
fifa_df = pd.read_csv(relpath('csv/players_f19_edited.csv'))
run_example(fifa_df)
