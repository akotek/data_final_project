# Football Players Analysis, Similarity and Transfer Benefit Prediction

Authors: Artyom Abramovich, Aviv Kotek and Omer Jacobi

## Usage:
In the bottom of the module main.py uncomment the relevant function and run the file.
1. run_similarity - run the file and follow the instructions afterwards to get the most similar players for the player of your liking.
2. plot_similarity - run the file and follow the instructions afterwards to get the word cloud of most similar players for the player of your liking.
3. plot_pca - run the file and get the plot of the [Midfielders, Defenders, Attackers, Goalkeepers] clusters of our FIFA19 data.
4. plot_clustering - run the file and get the plot of our data clustered to 4 clusters.
5. run_clustering - run the file and get output of main PCA components for PC-1 and PC-2.
6. clusters_distribution - run the file and get the clusters distribution per every player position.
7. determine_num_of_clusters - run the file and get the elbow plor for k-means.
8. make_predictions - run our Transfer Benefit Prediction model.

## Files:
Description of project files:
Our project has 2 main directories:
1. data_parsing directory:
This directory holds all the files relevant to data analysis, clustering and Player Similarities part of the project.
a. csv directory:
This directory contains our FIFA19 dataset, one of the csvs is the original dataset and the other is processed and changed             by us for project use.
b. clustering.py - Code responsible for data clustering tasks.
c. constants.py - Different constants (e.g column names) that were used in different .py files in our project.
d. processed.csv - FIFA19 processed csv for Players Similarity use.
e. similarity.py - Code responsible for Player Similarity tasks.
f. utils.py - Different function for use in different .py files throughout our project.
g. visualization.py - Code responsilbe for some of our project visualizations.
2. predictor directory:
a. predictor.py - The file with the our Transfer Benefit Prediction model.
c. csv directory:
            1. prediction_data.csv - The input data for our Transfer Benefit Prediction model.
            2. transfers.csv - All of the transfers we managed to find using the available data.
            3. The rest of the csv files were middle points between raw-data and transfer.csv creation.
d. The rest of the .py files were used just to process FIFA08-FIFA16 dataset and create prediction_data.csv.

## Notes:
1. If you wish to run the project please take a look at requirements.txt that lists all the package dependencies.
2. The csvs for Transfer Benefit Prediction part were created using database.sql file which is not present in the repository. If you     wish to get it, please download it from [here](https://www.kaggle.com/hugomathien/soccer).
            
        
         
