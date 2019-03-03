from scipy.spatial import distance
import data_parsing.utils as utils
from data_parsing.constants import *

USE_WEIGHTS = True
RECOMMENDATION_NUM = 10


# ------------------------------------------
# GENERAL:
# ------------------------------------------

def pre_process(df, features=PLAYER_FEATURES_VECTOR):
    """
    cleaning the pandas data frame by removing duplicates name, unwanted columns
    :param features:
    :param df: the data fram pandas object
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
    df = df[features]
    print('unique names: ' + str(len(df['Name'])))
    print('after droping null values: ' + str(len(df['ID'])))
    df.set_index('ID', drop=True, inplace=True)
    df = normalize_data(df)
    return df


def normalize_data(original_df: pd.DataFrame) -> pd.DataFrame:
    """
    Normalizes the data separately for every type of players
    Midfielders, attackers, defenders and goalkeepers players together will have std=1 and mean=0 for each group
    :param original_df:
    :return:
    """
    df_defenders = utils.get_rows_with_col_val(original_df, 'Position', DEFENDERS)
    df_midfielders = utils.get_rows_with_col_val(original_df, 'Position', MIDFIELDERS)
    df_forwards = utils.get_rows_with_col_val(original_df, 'Position', FORWARDS)
    df_gk = utils.get_rows_with_col_val(original_df, 'Position', GOALKEEPERS)
    df_list = [df_defenders, df_midfielders, df_forwards, df_gk]
    for i in range(len(df_list)):
        df_list[i] = utils.normalize_df(df_list[i].drop(['Name', 'Position'], axis=1))
    normalized_df = pd.concat(df_list)
    original_df = original_df[['Name', 'Position']].merge(normalized_df, left_index=True, right_index=True)
    return original_df


def get_players(df, lst) -> pd.DataFrame:
    return utils.get_rows_with_col_val(df, 'Name', lst)


def get_same_position(df, player_id) -> pd.DataFrame:
    """
    Gets players in same position of given id
    """
    pos = df.loc[player_id]['Position']
    if pos in DEFENDERS:
        return utils.get_rows_with_col_val(df, 'Position', DEFENDERS)
    elif pos in MIDFIELDERS:
        return utils.get_rows_with_col_val(df, 'Position', MIDFIELDERS)
    elif pos in FORWARDS:
        return utils.get_rows_with_col_val(df, 'Position', FORWARDS)
    elif pos in GOALKEEPERS:
        return utils.get_rows_with_col_val(df, 'Position', GOALKEEPERS)
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


def eval_euclidean_dist(player1, player2, w=None):
    return distance.euclidean(player1.values, player2.values, w=w)


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
        if USE_WEIGHTS:
            weights = generate_weights(player1)
        else:
            weights = None
        filterd_all_players = all_players
        if player1['Position'] != 'GK':
            filterd_all_players = all_players.drop(columns=GK_EXTRA_FEATURES, errors='ignore')
            player1 = player1.drop(labels=GK_EXTRA_FEATURES, errors='ignore')
        player1 = player1.drop(labels=['Position', 'Name']).dropna().astype('float64')
        for j, player2 in filterd_all_players.iterrows():
            if i != j:
                distance = distance_func(player1, player2, weights)
                player_distances[i][j] = distance
                # print(i, j, distance)
    return player_distances


def get_top_similarities_helper(player_distances: dict, all_players: pd.DataFrame, selected_player_id,
                                recommendations_num) -> pd.DataFrame:
    """
    Compares one player to all players by distances
    """
    top_df = pd.DataFrame.from_dict(player_distances, orient='index', columns=['distance'])
    top_df = top_df.merge(all_players, how='inner', left_index=True, right_index=True)[['distance', 'Name']]
    top_df['Selected Player'] = all_players.ix[selected_player_id]['Name']
    top_df = top_df.head(recommendations_num)
    return top_df


def get_top_similarities(df: pd.DataFrame, selected_players: pd.DataFrame, recommendations_num=5,
                         distance_func=eval_cosine_dist) -> pd.DataFrame:
    """
    :param df: Pool of players to compare to
    :param selected_players: Players to be similar to
    :param recommendations_num: Number of top similar players to selected players to show
    :param distance_func:
    :return: Top similar players to selected players comparison dataframe
    """
    if recommendations_num > len(df) - 1:
        recommendations_num = len(df) - 1
    # clean df to stay with numeric only:

    all_players = df.drop(columns=['Name', 'Position']).dropna()
    # compute:
    distances = compute_distance(all_players, selected_players, distance_func)
    top_similarities_list = []
    for selected_player_id in distances.keys():
        same_pos_players = get_same_position(df, selected_player_id)
        top_similarities_list.append(get_top_similarities_helper(distances[selected_player_id], same_pos_players,
                                                                 selected_player_id, recommendations_num))
    return pd.concat(top_similarities_list)


def generate_weights(player):
    """
    generate weights for the diffrant features of the the given player
    :param player: the player we want to generate weights
    :return: a vector of weights
    """
    player_pos = player['Position']
    axes = player.drop(labels=['Position', 'Name']).axes[0]
    axes_length = MAX_FEATURES_LEN
    weights = list()
    if player_pos in DEFENDERS:
        for feature in axes:
            index = DEFENDERS_WEIGHTS_SORT.index(feature)
            weight_val = axes_length - index
            weights.append(weight_val ** 5)
    elif player_pos in MIDFIELDERS:
        for feature in axes:
            index = MIDFIELDERS_WEIGHTS_SORT.index(feature)
            weight_val = axes_length - index
            weights.append(weight_val ** 4)
    elif player_pos in FORWARDS:
        for feature in axes:
            index = FORWARDS_WEIGHTS_SORT.index(feature)
            weight_val = axes_length - index
            weights.append(weight_val ** 4)
    elif player_pos in GOALKEEPERS:
        for feature in axes:
            axes_length += GK_EXTRA_LEN
            index = GOALKEPPER_WEIGHTS_SORT.index(feature)
            weight_val = axes_length - index
            weights.append(weight_val ** 4)
    else:
        return None
    return weights


# ------------------------------------------
# Usage example:
# ------------------------------------------


def find_similar_players(df, players, original_df, feature_vector, eval_dist_func=eval_cosine_dist):
    """
    find similar player to the list of players using the feature vector
    :param df: the dataframe of all the players
    :param players: the list of players
    :param original_df: the original df to merge and find other values
    :param feature_vector: the feature vector we want to calculate the distance
    :param eval_dist_func: the chosen distance function
    """
    df = pre_process(df, features=feature_vector)
    chosen_players = get_players(df, players)
    top_similiar = get_top_similarities(df, chosen_players, recommendations_num=RECOMMENDATION_NUM,
                                        distance_func=eval_dist_func)
    top_similiar = top_similiar.merge(original_df[['Release Clause', 'Overall']], how='left', left_index=True,
                                      right_index=True)
    top_similiar = top_similiar.sort_values(['Selected Player', 'distance'], ascending=False)
    return top_similiar
