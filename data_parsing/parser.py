import pandas as pd
import math, data_parsing.utils as utils
from scipy.spatial import distance

# Constants
# ------------------------------------------
UNWANTED_COLS = ['Special', 'International Reputation', 'Jersey Number', 'Joined', 'Release Clause']

SIMPLE_PLAYER_VECTOR = ['Name', 'ID', 'Position', 'Height', 'Work Rate', 'Weak Foot', 'Skill Moves', 'Crossing',
                        'Finishing', 'HeadingAccuracy', 'ShortPassing', 'Volleys', 'Dribbling', 'Curve', 'FKAccuracy',
                        'LongPassing', 'BallControl', 'Acceleration', 'SprintSpeed', 'Agility', 'Reactions', 'Balance',
                        'ShotPower', 'Jumping', 'Stamina', 'Strength', 'LongShots', 'Aggression', 'Interceptions',
                        'Positioning', 'Vision', 'Penalties', 'Composure', 'Marking', 'StandingTackle', 'SlidingTackle']

SIMPLE_GK_PLAYER_VECTOR = ['Name', 'ID', 'Crossing', 'Finishing', 'HeadingAccuracy',
                           'ShortPassing', 'Volleys', 'Dribbling', 'Curve', 'FKAccuracy',
                           'LongPassing', 'BallControl', 'Acceleration', 'SprintSpeed', 'Agility', 'Reactions',
                           'Balance',
                           'ShotPower', 'Jumping', 'Stamina', 'Strength', 'LongShots', 'Aggression', 'Interceptions',
                           'Positioning', 'Vision', 'Penalties', 'Composure', 'Marking', 'StandingTackle',
                           'SlidingTackle', 'GKDiving'
                                            'GKHandling', 'GKKicking', 'GKPositioning', 'GKReflexes']

# https://gaming.stackexchange.com/questions/167318/what-do-fifa-14-position-acronyms-mean
DEFENDERS = ['CB', 'LCB', 'RCB', 'LB', 'RB', 'LWB', 'RWB', 'LB']
MIDFIELDERS = ['CM', 'LDM', 'LAM', 'RDM', 'RAM', 'CDM', 'CAM', 'LM', 'RM', 'LCM', 'RCM']
FORWARDS = ['ST', 'CF', 'LW', 'RW', 'LS', 'RS', 'LF', 'RF']
GOALKEEPERS = ['GK']


# ------------------------------------------
# GENERAL:
# ------------------------------------------


def pre_process(df, goalkeeper=False, features=SIMPLE_PLAYER_VECTOR):
    """
    cleaning the pandas data frame by removing duplicates name, unwanted columns
    :param features:
    :param df: the data fram pandas object
    :param goalkeeper: if true returns only goalkeepers, otherwise return other player type
    :return: the data frame after cleaning it up
    """
    if 'Work Rate' in features:
        df[['defensive work rate', 'attacking work rate']] = df['Work Rate'].apply(utils.split_work_rate)
        df.drop(columns=['Work Rate'], inplace=True)
        features.remove('Work Rate')
        features.append('defensive work rate')
        features.append('attacking work rate')
    if 'Weak Foot' in features:
        df['Weak Foot'] = df['Weak Foot'].apply(lambda x: utils.normalize(x, 5, 1))
    if 'Skill Moves' in features:
        df['Skill Moves'] = df['Skill Moves'].apply(lambda x: utils.normalize(x, 5, 1))
    if 'Height' in features:
        df["Height"] = df["Height"].apply(lambda x: utils.parse_height(x))
        max_value = df['Height'].max()
        min_value = df['Height'].min()
        df["Height"] = df['Height'].apply(lambda x: utils.normalize(x, max_value, min_value))
    if 'Weight' in features:
        df['Weight'] = df["Weight"].apply(lambda x: utils.parse_weight(x))
        max_value = df['Weight'].max()
        min_value = df['Weight'].min()
        df['Weight'] = df['Weight'].apply(lambda x: utils.normalize(x, max_value, min_value))
    # print('max: ', df['Height'].max(), ' min: ', df['Height'].min())
    print('totals values: ' + str(len(df['Name'])))
    if goalkeeper:
        df = df[df["Position"] == 'GK']
        df = df[features]
    else:
        df = df[df["Position"] != 'GK']
        df = df[features]
    df = df.drop_duplicates(subset=['Name'])

    print('unique names: ' + str(len(df['Name'])))
    print('after droping null values: ' + str(len(df['ID'])))
    df.set_index('ID', drop=True, inplace=True)

    return df


def get_players(df, lst) -> pd.DataFrame:
    return get_rows_with_col_val(df, 'Name', lst)


def get_rows_with_col_val(df, col, lst_val):
    """
    Returns rows with values that fit for given column
    e.g: gets all players from DF with Position (col) of DF, RB, CD (lst_val)
    """
    return df.loc[df[col].isin(lst_val)]


def get_same_position(df, player_id) -> pd.DataFrame:
    pos = df.loc[player_id]['Position']
    if pos in DEFENDERS:
        return get_rows_with_col_val(df, 'Position', DEFENDERS)
    elif pos in MIDFIELDERS:
        return get_rows_with_col_val(df, 'Position', MIDFIELDERS)
    elif pos in FORWARDS:
        return get_rows_with_col_val(df, 'Position', FORWARDS)
    elif pos in GOALKEEPERS:
        return get_rows_with_col_val(df, 'Position', GOALKEEPERS)
    else:
        raise Exception("Bad position given")


# ------------------------------------------
# DISTANCE METHODS:
# ------------------------------------------

def eval_cosine_dist(player1, player2, w=None):
    # w1, w2...wn represents v1, v2...vn
    return 1 - distance.cosine(player1.values, player2.values, w=w)  # sim == (1 - cos.dst)


def eval_manhatan_dist(player1, player2, w=None):
    return distance.cityblock(player1.values, player2.values, w=w)


# ------------------------------------------
# ALGORITHM:
# ------------------------------------------

def compute_distance(all_players: pd.DataFrame, selected_players: pd.DataFrame, distance_func=eval_cosine_dist) -> dict:
    """
    Computes distance for given data frames
    :return: dictionary of dictionaries: To access the distance of player1 from player2 do:
                player_distances[player1_id][player2_id]
    """
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
    """
    top_df = pd.DataFrame.from_dict(player_distances, orient='index', columns=['distance'])
    top_df = top_df.merge(all_players, how='inner', left_index=True, right_index=True)[['distance', 'Name']]
    top_df['Selected Player'] = all_players.ix[selected_player_id]['Name']
    top_df = top_df.sort_values('distance', ascending=False)
    top_df = top_df.head(recommendations_num)
    return top_df


def get_top_similarities(df: pd.DataFrame, selected_players: pd.DataFrame, recommendations_num=5,
                         distance_func=eval_cosine_dist) -> pd.DataFrame:
    if recommendations_num > len(df) - 1:
        recommendations_num = len(df) - 1
    # clean df to stay with numeric only:
    all_players = df.drop(columns=['Name', 'Position']).dropna()
    selected_players = selected_players.drop(columns=['Name', 'Position']).dropna()
    # compute:
    distances = compute_distance(all_players, selected_players, distance_func)
    top_similarities_list = []
    for selected_player_id in distances.keys():
        same_pos_players = get_same_position(df, selected_player_id)
        top_similarities_list.append(get_top_similarities_helper(distances[selected_player_id], same_pos_players,
                                                                 selected_player_id, recommendations_num))
    return pd.concat(top_similarities_list)


def generate_weights(player):
    pass


# ------------------------------------------
# Usage example:
# ------------------------------------------
def run_example(df):
    df = pre_process(df)
    players = ['Cristiano Ronaldo', 'A. Griezmann']
    chosen_players = get_players(df, players)
    top_similiar = get_top_similarities(df, chosen_players, recommendations_num=4, distance_func=eval_cosine_dist)

    print(top_similiar)
    print()


fifa_df = pd.read_csv(utils.relpath('csv/players_f19_edited.csv'))
run_example(fifa_df)
