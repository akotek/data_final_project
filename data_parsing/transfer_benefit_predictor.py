import pandas as pd
import os
from sklearn.model_selection import train_test_split


def split_to_train_and_test():
    data = pd.read_csv(os.path.join('csv', 'prediction_data.csv'))
    X = data.drop(['recommend_to_go'], axis=1)
    Y = data[['recommend_to_go']]
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.9)
    return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    split_to_train_and_test()

