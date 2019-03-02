import pandas as pd
import os
from predictor.player_attributes_parsing import players_mean_by_year_helper


def get_player_vector(player_years: list, player: pd.DataFrame):
    df = pd.concat([player[player['year'] == year] for year in player_years])
    df = players_mean_by_year_helper(df)
    return df.to_dict('records')


def get_team_vector(years: list, team: pd.DataFrame):
    df = pd.concat([team[team['year'] == year] for year in years])
    df = players_mean_by_year_helper(df)
    return df


def get_label(years, player):
    label = pd.concat([player[player['year'] == year] for year in years])['overall_rating'].mean()
    return label


def get_vector(transfer: pd.Series, player_attributes: pd.DataFrame, team_attributes: pd.DataFrame):
    player = player_attributes.ix[transfer['player_id']]
    previous_team_years = list(range(int(transfer['start_year_previous_team']), int(transfer['start_year_next_team'])))
    next_team_years = list(range(int(transfer['start_year_next_team']), int(transfer['end_year_next_team']) + 1))
    player_vector = get_player_vector(previous_team_years, player)
    previous_team = team_attributes.ix[transfer['previous_team_id']]
    next_team = team_attributes.ix[transfer['next_team_id']]
    previous_team_vector = get_team_vector(previous_team_years, previous_team).to_dict('records')
    next_team_vector = get_team_vector(next_team_years, next_team)
    next_team_vector.columns = [str(col) + '_2' for col in next_team_vector.columns]
    next_team_vector = next_team_vector.to_dict('records')
    if len(next_team_vector) == 0:
        return None
    label = get_label(next_team_years, player)
    vector = {**player_vector[0], **previous_team_vector[0], **next_team_vector[0],
              'overall_rating_after_transfer': label}
    return vector


def create_predictor_data():
    transfer_df = pd.read_csv(os.path.join('csv', 'transfers.csv'))
    player_attributes_df = pd.read_csv(os.path.join('csv', 'player_attributes_yearly.csv'))
    team_attributes_df = pd.read_csv(os.path.join('csv', 'team_attributes.csv'))
    player_attributes_df = player_attributes_df.set_index('player_api_id')
    team_attributes_df = team_attributes_df.set_index('team_api_id')
    X_vectors = [None] * len(transfer_df)
    for i, transfer in transfer_df.iterrows():
        X_vectors[i] = get_vector(transfer, player_attributes_df, team_attributes_df)
    final_vectors = []
    for vector in X_vectors:
        if vector is not None:
            final_vectors.append(vector)
    data = pd.DataFrame.from_records(final_vectors)
    data = data.drop(['year', 'year_2'], axis=1)
    data.to_csv(os.path.join('csv', 'prediction_data.csv'), index=False)


def get_binary_label(row: pd.Series):
    if row['overall_rating'] <= row['overall_rating_after_transfer']:
        return 1
    return 0


def edit_labels_to_binary():
    data = pd.read_csv(os.path.join('csv', 'prediction_data.csv'))
    data['recommend_to_go'] = data.apply(lambda x: get_binary_label(x), axis=1)
    data = data.drop(['overall_rating_after_transfer'], axis=1)
    data.to_csv(os.path.join('csv', 'prediction_data.csv'), index=False)


def check_predictor_data():
    data = pd.read_csv(os.path.join('csv', 'prediction_data.csv'))
    print(data.columns)
    print()

#
# if __name__ == "__main__":
    # create_predictor_data()
    # check_predictor_data()
