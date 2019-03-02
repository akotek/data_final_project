from matplotlib import pyplot as plt
from data_parsing.constants import *
import data_parsing.utils as utils
from wordcloud import WordCloud

# ------------------------------------------
# Constants to configure plotting
# ------------------------------------------
COLORS = ['r', 'g', 'b', 'y']
DOTS_SIZE = 3


# ------------------------------------------
def plot_pca(orig_df, pc_df):
    position = [GOALKEEPERS, DEFENDERS, MIDFIELDERS, FORWARDS]
    for target, color in zip(position, COLORS):
        # in each iteration - get indices of specific position
        # && plot with different color
        indices = utils.get_rows_with_col_val(orig_df, 'Position', target).index.values
        plt.scatter(pc_df.loc[indices, 'PCA1'], pc_df.loc[indices, 'PCA2'], c=color, s=DOTS_SIZE)
    plt.title("PCA graph")
    plt.legend(['Goalkeepers', 'Defenders', 'Midfielders', 'Forwards'], loc=4)
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.show()


def plot_clustering(clst_df):
    clusters = ['0', '1', '2', '3']
    for clst, color in zip(clusters, COLORS):
        indices = utils.get_rows_with_col_val(clst_df, 'Cluster', [clst]).index.values
        plt.scatter(clst_df.loc[indices, 'PCA1'], clst_df.loc[indices, 'PCA2'], c=color, s=DOTS_SIZE)
    plt.title("Clustering graph")
    plt.legend(["Cluster 0", "Cluster 1", "Cluster 2", "Cluster 3"], loc=4)
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.show()


def plot_tag_clouds(freq_dict):
    wcloud = WordCloud(relative_scaling=1)  # rel scaling between 0,1
    wcloud = wcloud.generate_from_frequencies(frequencies=freq_dict)
    plt.imshow(wcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()
