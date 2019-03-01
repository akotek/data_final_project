from sklearn.cluster import KMeans

from data_parsing.constants import *
import data_parsing.utils as utils
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE


def pre_process(df):
    df = df[CLUSTERING_PLAYER_FEATURES_VECTOR]
    df.set_index('ID', drop=True, inplace=True)
    df = df.dropna(how='all')
    df = df.fillna(df.mean())
    return df


def normalize(df):
    # standardize data before running pca/k-means
    return utils.normalize_df(df.drop(['Name', 'Position'], axis=1))


def pca(df, dim):
    """
    Dimension reduction to given param using PCA algorithm
    Returns transformed num_of_features/dim data frame
    """
    print("Starting PCA of dim {} for {} features".format(dim, df.shape[0]))
    p = PCA(n_components=dim)
    reduced = p.fit_transform(df)
    transformed_df = pd.DataFrame(data=reduced, index=df.index.values, columns=['PCA1', 'PCA2'])
    return transformed_df


def cluster(df, k):
    """
    Clustering using k-means,
    """
    print("Starting clustering for: {} num of players and {} clusters".format(df.shape[0], k))
    kmeans = KMeans(n_clusters=k)
    kmeans = kmeans.fit(df)
    labels = kmeans.predict(df)
    C = kmeans.cluster_centers_
    clusters = kmeans.labels_.tolist()  # save this to original df
    return labels, C, clusters

def tsne(df, n):
    ts = TSNE(n_components=n)
    return ts.fit_transform(df)