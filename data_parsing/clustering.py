from sklearn.cluster import KMeans
from data_parsing.constants import *
import data_parsing.utils as utils
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt


def pre_process(df):
    """
    Pre process data before clustering
    """
    df = df.dropna(how='all')
    df = df[CLUSTERING_PLAYER_FEATURES_VECTOR]
    df.set_index('ID', drop=True, inplace=True)
    df = df.fillna(df.mean())
    return df


def normalize(df):
    """
    Standardize data before running pca/k-means
    """
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


def determine_num_of_clusters(df: pd.DataFrame):
    """
    Plots num of clusters to be used by elbow method
    """
    df = pre_process(df).drop(['Name', 'Position'], axis=1)
    Sum_of_squared_distances = []
    K = range(1, 15)
    for k in K:
        km = KMeans(n_clusters=k)
        km = km.fit(df)
        Sum_of_squared_distances.append(km.inertia_)
    plt.plot(K, Sum_of_squared_distances, 'bx-')
    plt.xlabel('k')
    plt.ylabel('Sum_of_squared_distances')
    plt.title('Elbow Method For Optimal k')
    plt.show()
