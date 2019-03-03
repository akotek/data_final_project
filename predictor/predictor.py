import pandas as pd
import os
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
from catboost import CatBoostClassifier


def get_accuracy_vector(preds, truth):
    number_of_wrong_guesses = 0
    error = [0] * len(preds)
    for i in range(len(preds)):
        if preds[i] != truth[i]:
            number_of_wrong_guesses = number_of_wrong_guesses + 1
        error[i] = 1 - number_of_wrong_guesses / (i + 1)
    return error


def plot_test_acc(baseline_preds, model_preds, truth):
    baseline_acc = get_accuracy_vector(baseline_preds, truth)
    model_acc = get_accuracy_vector(model_preds, truth)
    test_samples = list(range(1, len(baseline_preds) + 1))
    plt.xlabel = 'test samples'
    plt.ylabel = 'accuracy'
    plt.title = 'Test Accuracy'
    plt.plot(test_samples, baseline_acc, label='Baseline accuracy')
    plt.plot(test_samples, model_acc, label='CatBoostClassifier accuracy')
    plt.show()


def make_predictions():
    data = pd.read_csv(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'csv', 'prediction_data.csv'))
    X = data.drop(['recommend_to_go'], axis=1)
    Y = data['recommend_to_go']
    X_train, X_test, y_train, y_test = train_test_split(X, Y, test_size=0.1)

    classifier = CatBoostClassifier()
    classifier.fit(X_train, y_train)
    y_score = classifier.predict(X_test)
    print('Our model accuracy score:')
    print(accuracy_score(y_test, y_score))
    print('Baseline model accuracy score:')
    print(accuracy_score(y_test, [1] * len(y_test)))
    print(classifier.get_feature_importance(prettified=True))
    plot_test_acc([1] * len(y_test), y_score, y_test.to_list())


if __name__ == "__main__":
    make_predictions()

