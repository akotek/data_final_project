import pandas as pd
import numpy as np
import os
import re
from sklearn.metrics.pairwise import cosine_similarity, manhattan_distances
import math

# Constants
# ------------------------------------------
UNWANTED_COLS = [ 'Special','International Reputation', 'Jersey Number', 'Joined', 'Release Clause']

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
    in_ = float(ht_[1].replace("\"", ""))
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

def normalize(score, max_value, min_value,max_score=100):

    return max_score * (score - min_value) / (max_value - min_value)
# ------------------------------------------
# Player methods:
# ------------------------------------------


def pre_process(df, goalkeeper=False, features = SIMPLE_PLAYER_VECTOR):
    """
    cleaning the pandas data frame by removing duplicates name, unwanted columns
    :param df: the data fram pandas object
    :param goalkeeper: if true returns only goalkeepers, otherwise return other player type
    :return: the data frame after cleaning it up
    """
    df.drop(columns=UNWANTED_COLS, inplace=True)
    df.drop(columns=REMOVE_WAGES)
    if 'Weak Foot' in features:
        df['Weak Foot'] = df['Weak Foot'].apply(lambda x:normalize(x,5,1))
    if 'Skill Moves' in features:
        df['Skill Moves'] = df['Skill Moves'].apply(lambda x:normalize(x,5,1))
    if 'Height' in features:
        df["Height"] = df["Height"].apply(lambda x:parse_height(x))
        max_value = df['Height'].max()
        min_value = df['Height'].min()
        df["Height"] = df['Height'].apply(lambda x:normalize(x,max_value,min_value))
    if 'Weight' in features:
        df['Weight'] = df["Weight"].apply(lambda x:parse_weight(x))
        max_value = df['Weight'].max()
        min_value = df['Weight'].min()
        df['Weight'] = df['Weight'].apply(lambda x: normalize(x, max_value, min_value))
    print('max: ', df['Height'].max(), ' min: ', df['Height'].min())
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
    """
    SKLearn cosine distance
    :param player1:
    :param player2:
    :return:
    """
    return cosine_similarity([player1], [player2])[0][0]


def eval_manhatan_dist(player1, player2):
    """
    SKLearn manhattan distance
    :param player1:
    :param player2:
    :return:
    """
    return manhattan_distances([player1], [player2])[0][0]


def compute_distance(all_players: pd.DataFrame, selected_players: pd.DataFrame, distance_func=eval_cosine_dist)-> dict:
    """
    :param all_players: All players
    :param selected_players: Players of interest
    :param distance_func:
    :return: dictionary of dictionaries:
                To access the distance of player1 from player2 do:
                player_distances[player1_id][player2_id]
    """
    all_players = all_players.drop(columns=['Name']).dropna()
    selected_players = selected_players.drop(columns=['Name']).dropna()
    player_distances = dict()
    for i, player1 in selected_players.iterrows():
        player_distances[i] = dict()
        for j, player2 in all_players.iterrows():
            if i != j:
                distance = distance_func(player1, player2)
                player_distances[i][j] = distance
                print(i, j, distance)
    return player_distances


def get_top_similarities_helper(player_distances: dict, all_players: pd.DataFrame, selected_player_id,
                                recommendations_num) -> pd.DataFrame:
    """
    Compares one player to all players by distances
    :param player_distances:
    :param all_players:
    :param selected_player_id:
    :param recommendations_num:
    :return:
    """
    top_df = pd.DataFrame.from_dict(player_distances, orient='index', columns=['distance'])
    top_df = top_df.merge(all_players, how='inner', left_index=True, right_index=True)[['distance', 'Name']]
    top_df['Selected Player'] = all_players.ix[selected_player_id]['Name']
    top_df = top_df.sort_values('distance', ascending=False)
    top_df = top_df.head(recommendations_num)
    return top_df


def get_top_similarities(all_players: pd.DataFrame, selected_players: pd.DataFrame, recommendations_num=5,
                         distance_func=eval_cosine_dist) -> pd.DataFrame:
    """

    :param all_players: 5
    :param selected_players:
    :param recommendations_num:
    :param distance_func:
    :return:
    """
    if recommendations_num > len(all_players) - 1:
        recommendations_num = len(all_players) - 1
    distances = compute_distance(all_players, selected_players, distance_func)
    top_similarities_list = []
    for selected_player_id in distances.keys():
        top_similarities_list.append(get_top_similarities_helper(distances[selected_player_id], all_players,
                                                                 selected_player_id, recommendations_num))
    return pd.concat(top_similarities_list)


def run_example(df):
    df = pre_process(df)
    chosen_players = df[(df['Name'] == 'A. Griezmann') | (df['Name'] == 'Cristiano Ronaldo')]
    top_similiar = get_top_similarities(df, chosen_players, recommendations_num=20)
    print(top_similiar)
    print()


# ------------------------------------------
# Usage example:
# ------------------------------------------
fifa_df = pd.read_csv(relpath('csv/players_f19_edited.csv'))
run_example(fifa_df)
