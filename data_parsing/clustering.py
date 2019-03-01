from data_parsing.constants import *
import data_parsing.utils as utils
from sklearn.decomposition import PCA


def pre_process(df):
    print("Starting pre-process for clustering")
    df = df[CLUSTERING_PLAYER_FEATURES_VECTOR]
    df.set_index('ID', drop=True, inplace=True)
    df = df.dropna(how='all')
    df = df.fillna(df.mean())
    norm_df = utils.normalize_df(df.drop(['Name'], axis=1))
    # df = norm_df.merge(df['Name'], left_index=True, right_index=True)
    print("Ended pre-process")
    return norm_df


def cluster(df, k):
    print("Starting clustering for: {} num of players and {} clusters".format(df.shape[0], k))


def pca(df, dim):
    """
    Dimension reduction to given param using PCA algorithm
    """
    p = PCA(n_components=dim)
    reduced = p.fit_transform(df)
    transformed_df = pd.DataFrame(data=reduced, columns=['PCA1', 'PCA2'])
    print(transformed_df.head())
    return transformed_df
