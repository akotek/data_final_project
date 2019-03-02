import pandas as pd
import os
from predictor.transfer_db_processing import get_player_attributes

PLAYER_ATTRIBUTES_DF = get_player_attributes()


def clean_player_attributes(df: pd.DataFrame) -> pd.DataFrame:
    df = df[df['year'] != '2007']
    bad_player_ids = df[df.isnull().any(axis=1)]['player_api_id'].unique()
    df = df[~df['player_api_id'].isin(bad_player_ids)]
    df = df.drop(['attacking_work_rate', 'defensive_work_rate', 'id', 'player_fifa_api_id'], axis=1)
    df['year'] = df['year'].astype(int)
    return df


def players_mean_by_year_helper(df: pd.DataFrame) -> pd.DataFrame:
    df = df.groupby(df.index).mean()
    return df


def players_mean_by_year(df: pd.DataFrame) -> pd.DataFrame:
    df_year_list = []
    for year in range(2008, 2017):
        df_year_list.append(df[df['year'] == year])
    for i in range(len(df_year_list)):
        df_year_list[i] = players_mean_by_year_helper(df_year_list[i])
    df = pd.concat(df_year_list)
    return df


def create_player_attributes_csv():
    df = PLAYER_ATTRIBUTES_DF
    df = clean_player_attributes(df)
    df = pd.get_dummies(df, columns=['preferred_foot'])
    df = df.set_index('player_api_id')
    df = players_mean_by_year(df)
    df.to_csv(os.path.join('csv', 'player_attributes_yearly.csv'), index_label='player_api_id')


if __name__ == "__main__":
    create_player_attributes_csv()
