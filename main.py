from data_parsing.similarity import *
import data_parsing.clustering as clustering
import data_parsing.visualization as visualizer
import matplotlib.pyplot as plt
from data_parsing.clustering import determine_num_of_clusters


NUM_OF_CLUSTERS = 4


# Similarity:
# ------------------------------------------

def plot_similarity(df):
    sim, players = run_similarity(df)
    freq_dict = sim.set_index('Name').to_dict()['distance']
    for p in players:
        freq_dict[p] = 1
    visualizer.plot_tag_clouds(freq_dict)


def run_similarity(df):
    pd.set_option('display.expand_frame_repr', False)
    eval_func, players = get_user_input()
    eval_func = eval_cosine_dist
    original_df = pd.DataFrame(df).set_index('ID')
    original_df = original_df.drop_duplicates(subset=['Name'])
    gk_players, other_players = split_player_type(original_df, players)
    sim = pd.DataFrame()
    if len(gk_players):
        player_type_df = df[df['Position'] == 'GK']
        player_type_df.is_copy = False
        sim = find_similar_players(player_type_df, gk_players, original_df,
                                   GK_PLAYER_FEATURES_VECTOR, eval_func)
    if len(other_players):
        player_type_df = df[df['Position'] != 'GK']
        player_type_df.is_copy = False
        sim = find_similar_players(player_type_df, other_players, original_df,
                                   PLAYER_FEATURES_VECTOR, eval_func)
    print(sim)
    return sim, players


def get_user_input():
    names = input("Enter player/s name you want to compute, spare them by comma\n")
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
    print(transformed_df.head())
    return processed_df, transformed_df


def plot_clustering(df):
    prcss_df, clstr_df = run_clustering(df)
    df = pd.merge(prcss_df, clstr_df['Cluster'], )
    visualizer.plot_clustering(clstr_df)


def clusters_distribution(df: pd.DataFrame):
    processed_df, transformed_df = run_clustering(df)
    clustered_df = pd.merge(transformed_df['Cluster'], processed_df, left_index=True, right_index=True, how='inner')
    num_of_positions = len(df['Position'].dropna().unique())
    clusters = [clustered_df[clustered_df['Position'] == position] for position in df['Position'].dropna().unique()]
    for position, position_name, number in zip(clusters, df['Position'].dropna().unique(), range(1, num_of_positions + 1)):
        position['Cluster'].value_counts().plot(kind='bar', rot=0)
        plt.title('Histogram of clusters of for position ' + position_name + ':')
        plt.xlabel('Cluster Number')
        plt.xticks(rotation=0)
        plt.ylabel('Number of Players')
        plt.show()


# ------------------------------------------

if __name__ == "__main__":
    fifa_df = pd.read_csv(utils.relpath('csv/players_f19_edited.csv'))
    run_similarity(fifa_df)
    # plot_similarity(fifa_df)
    # plot_pca(fifa_df)
    # plot_clustering(fifa_df)
    # run_clustering(fifa_df)
    clusters_distribution(fifa_df)
    # determine_num_of_clusters(fifa_df)
