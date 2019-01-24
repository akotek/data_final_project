import pandas as pd
import os

# Constants
# ------------------------------------------
SIMPLE_VECTOR_COLS = ['Overall', 'Potential', 'Crossing', 'Finishing', 'HeadingAccuracy',
                      'ShortPassing', 'Volleys', 'Dribbling', 'Curve', 'FKAccuracy',
                      'LongPassing', 'BallControl', 'Acceleration', 'SprintSpeed', 'Agility', 'Reactions', 'Balance',
                      'ShotPower', 'Jumping', 'Stamina', 'Strength', 'LongShots', 'Aggression', 'Interceptions',
                      'Positioning', 'Vision', 'Penalties', 'Composure', 'Marking', 'StandingTackle', 'SlidingTackle']

COMPLEX_VECTOR_COLS = ['Age', 'Wage', 'International Reputation', 'Work Rate', 'Time In Club', 'Height',
                       'Weight', 'Release Clause']


# ------------------------------------------

# Utils methods:
# ------------------------------------------
def relpath(path):
    return os.path.join(os.path.dirname(__file__), path)


# asserts data_frame and string, this will be useful
# in later process of our coding for debugging
def assert_df(df, string):
    assert isinstance(string, str) and isinstance(df, pd.core.frame.DataFrame)


# ------------------------------------------


# returns rows (== players) of given club
def get_players_from_club(df, club):
    assert_df(df, club)
    return df.loc[df['Club'] == club]


def get_club_simple_vector(df, club):
    pass

def get_player_simple_vector(df, player):
    assert_df(df, player)
    return get_player(df, player)[SIMPLE_VECTOR_COLS]


# returns simple vector of a single player,
# simple is NUMERIC with scaling of [1, 100]
def get_player(df, name):
    assert_df(df, name)
    return df.loc[df['Name'] == name]


# returns more complex vector of single player,
# this will include VALUE, hieght, weight transformed to [1, 100] scale:
def get_player_complex_vector(df, player):
    #  move all to scale [1,100]
    pass


# returns all defenders of a team
# defender can be CB, LD, LR, etc..
def get_defenders(df, team):
    DEF_POSITIONS = []
    pass


# goalkeepers has different data, need to think on this
def get_goalkeeper_vector(df, gk):
    pass


def pre_process():
    df = pd.read_csv(relpath('players_f19_edited.csv'))
    print(get_players_from_club(df, "FC Barcelona").head)
    print(get_player_simple_vector(df, 'L. Messi'))

    # TODO :: read on categorical values


pre_process()
