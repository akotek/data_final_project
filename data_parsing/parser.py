import pandas as pd
import numpy as np
import os

# Constants
# ------------------------------------------
UNWANTED_COLS = ['ID', 'Special', 'Preferred Foot', 'Weak Foot', 'Skill Moves', 'Body Type']

SIGNS_TO_CLEAN = ['€']

SIMPLE_PLAYER_VECTOR = ['Overall', 'Potential', 'Crossing', 'Finishing', 'HeadingAccuracy',
                        'ShortPassing', 'Volleys', 'Dribbling', 'Curve', 'FKAccuracy',
                        'LongPassing', 'BallControl', 'Acceleration', 'SprintSpeed', 'Agility', 'Reactions', 'Balance',
                        'ShotPower', 'Jumping', 'Stamina', 'Strength', 'LongShots', 'Aggression', 'Interceptions',
                        'Positioning', 'Vision', 'Penalties', 'Composure', 'Marking', 'StandingTackle', 'SlidingTackle']

COMPLEX_PLAYER_VECTOR = ['Age', 'Wage', 'International Reputation', 'Work Rate', 'Time In Club', 'Height',
                         'Weight', 'Release Clause']

SIMPLE_CLUB_VECTOR = ['Age', 'Wage', 'Value', 'Overall', 'Agility']  # generated from players

COMPLEX_CLUB_VECTOR = ['Wins Per Season', 'Loses Per Season', 'Coach Level', 'Team History']  # TODO get his data:


# ------------------------------------------

# Utils methods:
# ------------------------------------------

def relpath(path):
    return os.path.join(os.path.dirname(__file__), path)


# ------------------------------------------

# Player methods:
# ------------------------------------------


def get_player_simple_vector(df, player):
    # Returns simple vector of a single player, NUMERIC with scaling of [1, 100]
    # As chosen in constant SIMPLE_VECTOR_PLAYER
    return get_player(df, player)[SIMPLE_PLAYER_VECTOR].astype(int)


def get_player(df, name):
    return df.loc[df['Name'] == name]


def get_player_complex_vector(df, player):
    # returns more complex vector of single player,
    # this will include VALUE, height, weight transformed to [1, 100] scale:
    # TODO
    pass


# ------------------------------------------

# Club methods:
# ------------------------------------------
def get_players_from_club(df, club):
    # returns rows (== players) of given club
    return df.loc[df['Club'] == club]


def get_simple_club_vector(df, club):
    # Returns average of SIMPLE_CLUB_VECTOR values,
    # In a new data frame row=[Club] col=[Avg1, avg2,....] form
    assert set(SIMPLE_CLUB_VECTOR).issubset(df.columns)

    # Init new DF with 0 value and club name:
    data = np.array(np.zeros((1, len(SIMPLE_CLUB_VECTOR)), dtype=int))
    cb_df = pd.DataFrame(data, index=[0], columns=SIMPLE_CLUB_VECTOR)

    # Create avg's:
    players = get_players_from_club(df, club)
    for col in SIMPLE_CLUB_VECTOR:
        if col in ['Value', 'Wage'] : continue  # remove this after 'clean signs' is done
        cb_df[col] = int(players[col].mean())

    # Modify columns and add 'Club'
    cb_df.columns = "Avg " + cb_df.columns
    cb_df.insert(loc=0, column='Club', value=club)
    return cb_df


def get_complex_club_vector(df, club):
    # todo -- simpleVec + complexVec
    pass


# ------------------------------------------


def pre_process(df):
    # pre-process given DataFrame,
    # Edit col's, add, remove data and SCALE,
    df.drop(columns=UNWANTED_COLS, inplace=True)
    df.update(df.select_dtypes(include=[np.number]).fillna(0).astype(int))  # make NaN to 0 and make type int #todo not working proply

    # Clean Value && Wage € sign
    # for sign in SIGNS_TO_CLEAN:
    #     df.apply(lambda row: row.str.strip(sign))


def run_example(df):
    pre_process(df)
    # uncomment to run various examples of API's:
    # --------------------------------------------
    # barca_players = get_players_from_club(df, 'FC Barcelona')
    # print(barca_players.head)

    # player_vec = get_player_simple_vector(df, 'L. Messi')
    # print(player_vec)

    print(get_simple_club_vector(df, 'FC Barcelona'))
    # --------------------------------------------


# ------------------------------------------
# Usage example:
# ------------------------------------------
fifa_df = pd.read_csv(relpath('csv\players_f19_edited.csv'))
run_example(fifa_df)
