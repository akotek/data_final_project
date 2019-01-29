import pandas as pd
import numpy as np
import os

# Constants
# ------------------------------------------
SIMPLE_PLAYER_VECTOR = ['Overall', 'Potential', 'Crossing', 'Finishing', 'HeadingAccuracy',
                        'ShortPassing', 'Volleys', 'Dribbling', 'Curve', 'FKAccuracy',
                        'LongPassing', 'BallControl', 'Acceleration', 'SprintSpeed', 'Agility', 'Reactions', 'Balance',
                        'ShotPower', 'Jumping', 'Stamina', 'Strength', 'LongShots', 'Aggression', 'Interceptions',
                        'Positioning', 'Vision', 'Penalties', 'Composure', 'Marking', 'StandingTackle', 'SlidingTackle']

COMPLEX_PLAYER_VECTOR = ['Age', 'Wage', 'International Reputation', 'Work Rate', 'Time In Club', 'Height',
                         'Weight', 'Release Clause']

UNWANTED_COLS = ['ID', 'Value', 'Wage', 'Special', 'Preferred Foot', 'Weak Foot', 'Skill Moves', 'Body Type']

AVERAGE_COLS = ['Age', 'Value', 'Wage', 'Overall']

# TODO
SIMPLE_CLUB_VECTOR = []
COMPLEX_CLUB_VECTOR = []


# ------------------------------------------

# Utils methods:
# ------------------------------------------

def relpath(path):
    return os.path.join(os.path.dirname(__file__), path)


def assert_df(df, string):
    # asserts data_frame and string, this will be useful
    # in later process of coding for debugging purposes
    assert isinstance(string, str) and isinstance(df, pd.core.frame.DataFrame)

def add_average_col(df, col):
    pass

# ------------------------------------------

# Player methods:
# ------------------------------------------


def get_player_simple_vector(df, player):
    # returns simple vector of a single player,
    # simple is NUMERIC with scaling of [1, 100]
    return get_player(df, player)[SIMPLE_PLAYER_VECTOR]


def get_player(df, name):
    assert_df(df, name)
    return df.loc[df['Name'] == name]


def get_player_complex_vector(df, player):
    # returns more complex vector of single player,
    #     # this will include VALUE, hieght, weight transformed to [1, 100] scale:
    #  move all to scale [1,100]
    pass


def get_defenders(df, team):
    # returns all defenders of a team
    # defender can be CB, LD, LR, etc..
    DEF_POSITIONS = []
    pass


def get_goalkeeper_vector(df, gk):
    # goalkeepers has different data, need to think on this
    pass


# ------------------------------------------

# Club methods:
# ------------------------------------------
def get_club_simple_vector(df, club):
    pass


def get_players_from_club(df, club):
    # returns rows (== players) of given club
    assert_df(df, club)
    return df.loc[df['Club'] == club]


# ------------------------------------------


def pre_process(df):
    # pre-process given DataFrame,
    # edit col's, add and remove data and SCALE,
    df.drop(columns=UNWANTED_COLS, inplace=True)
    df.update(df.select_dtypes(include=[np.number]).fillna(0)) # NaN -> 0 and round to int
    df.astype(int) #TODO need to move all to int
    # add_average_col(AVERAGE_COLS)

    # Scaling is chosen as [1,100] and all other numeric values are transformed
    # to this scaling type:



def run_example(df):
    pre_process(df)



    # df['avgOverall'] = df['Overall'].mean(axis=1)

    # uncomment to run various examples of API's:
    # --------------------------------------------
    # barca_players = get_players_from_club(df, 'FC Barcelona')
    # print(barca_players)
    player_vec = get_player_simple_vector(df, 'L. Messi')
    print(player_vec)


# ------------------------------------------
# Usage example:
# ------------------------------------------
data = pd.read_csv(relpath('players_f19_edited.csv'))
run_example(data)


