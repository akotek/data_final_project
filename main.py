from data_parsing.similarity import *
import data_parsing.clustering as clustering
import data_parsing.visualization as visualizer

NUM_OF_CLUSTERS = 4

# Similarity:
# ------------------------------------------
def run_similarity(df):
    pd.set_option('display.expand_frame_repr', False)
    eval_func, players = get_user_input()
    original_df = pd.DataFrame(df).set_index('ID')
    original_df = original_df.drop_duplicates(subset=['Name'])
    gk_players, other_players = split_player_type(original_df, players)
    if len(gk_players):
        player_type_df = df[df['Position'] == 'GK']
        player_type_df.is_copy = False
        find_similar_players(player_type_df, gk_players, original_df,
                             GK_PLAYER_FEATURES_VECTOR, eval_func)
    if len(other_players):
        player_type_df = df[df['Position'] != 'GK']
        player_type_df.is_copy = False
        find_similar_players(player_type_df, other_players, original_df,
                             PLAYER_FEATURES_VECTOR, eval_func)


def get_user_input():
    names = input("players you want to computer?, spare them by comma\n")
    names = names.split(",")
    players = list()
    for name in names:
        players.append(name.strip())
    func = input("which distance function you want to use: Cosine,"
                 " Manhattan or Euclidean?\n")
    func = func.strip().lower()
    if func == 'manhattan':
        eval_func = eval_manhatan_dist
        print("you chose Manhattan")
    elif func == 'euclidean':
        eval_func = eval_euclidean_dist
        print("you chose Euclidean")
    else:
        eval_func = eval_cosine_dist
        print("you chose Cosine")
    return eval_func, players


def split_player_type(original_df, players):
    """
    split a list of players to goalkeppers and other kind of players
    :return: 2 list of players sname
    """
    gk_players = list()
    other_players = list()
    for player in players:
        if original_df[original_df['Name'] == player]['Position'].eq('GK').any():
            gk_players.append(player)
        else:
            other_players.append(player)
    return gk_players, other_players


# Clustering
# ------------------------------------------
def run_pca(df):
    processed_df = clustering.pre_process(df)  # diff pre processing than similarity one
    norm_df = clustering.normalize(processed_df)
    transformed_df = clustering.pca(norm_df, 2)
    return processed_df, transformed_df


def plot_pca(df):
    prcss_df, trnsf_df = run_pca(df)
    visualizer.plot_pca(prcss_df, trnsf_df)


def run_clustering(df):
    # Builds data with cluster column and name column
    processed_df, transformed_df = run_pca(df)
    labels, C, clusters = clustering.cluster(transformed_df, NUM_OF_CLUSTERS)
    transformed_df['Cluster'] = clusters
    # transformed_df['Name'] = df['Name']
    print(transformed_df.head())
    return processed_df, transformed_df


def plot_clustering(df):
    prcss_df, clstr_df = run_clustering(df)
    visualizer.plot_clustering(clstr_df)

def run_tsne(df):
    pass
# ------------------------------------------

if __name__ == "__main__":
    fifa_df = pd.read_csv(utils.relpath('csv/players_f19_edited.csv'))
    # run_similarity(fifa_df)
    # plot_pca(fifa_df)
    # plot_clustering(fifa_df)
    # run_clustering(fifa_df)
