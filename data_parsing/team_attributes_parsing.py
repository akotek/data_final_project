import pandas as pd
import os
from data_parsing.transfer_db_processing import get_team_attributes


TEAM_ATTRIBUTES = get_team_attributes()
CATEGORICAL_COLUMNS = ['buildUpPlaySpeedClass', 'buildUpPlayDribblingClass', 'buildUpPlayPassingClass',
                       'buildUpPlayPositioningClass', 'chanceCreationPassingClass', 'chanceCreationCrossingClass',
                       'chanceCreationShootingClass', 'chanceCreationPositioningClass', 'defencePressureClass',
                       'defenceAggressionClass', 'defenceTeamWidthClass', 'defenceDefenderLineClass']


def clean_team_attributes(df: pd.DataFrame) -> pd.DataFrame:
    df = df.drop(['buildUpPlayDribbling', 'id', 'team_fifa_api_id'], axis=1)
    return df


def create_team_attributes_csv():
    df = TEAM_ATTRIBUTES
    df = clean_team_attributes(df)
    df = df.set_index('team_api_id')
    df = pd.get_dummies(df, columns=CATEGORICAL_COLUMNS)
    df.to_csv(os.path.join('csv', 'team_attributes.csv'), index_label='team_api_id')


if __name__ == "__main__":
    create_team_attributes_csv()

