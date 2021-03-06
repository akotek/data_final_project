from data_parsing.utils import *

# ------------------------------------------
# Constants
# ------------------------------------------
# main features are one which are given to csv with [1, 100] scale
FIFA_MAIN_FEATURES = ['Crossing', 'Finishing', 'HeadingAccuracy', 'ShortPassing', 'Volleys', 'Dribbling', 'Curve', 'FKAccuracy',
                          'LongPassing', 'BallControl', 'Acceleration', 'SprintSpeed', 'Agility', 'Reactions', 'Balance',
                          'ShotPower', 'Jumping', 'Stamina', 'Strength', 'LongShots', 'Aggression', 'Interceptions',
                          'Positioning', 'Vision', 'Penalties', 'Composure', 'Marking', 'StandingTackle', 'SlidingTackle']

PLAYER_FEATURES_VECTOR = ['Name', 'ID', 'Position', 'Height', 'Work Rate', 'Weak Foot', 'Skill Moves'] + FIFA_MAIN_FEATURES

GK_EXTRA_FEATURES = ['GKDiving', 'GKHandling', 'GKKicking', 'GKPositioning', 'GKReflexes']

GK_PLAYER_FEATURES_VECTOR = ['Name', 'ID', 'Position', 'Height', 'Weak Foot', 'Crossing',
                             'Finishing', 'HeadingAccuracy', 'ShortPassing', 'Volleys', 'Dribbling', 'Curve',
                             'FKAccuracy','LongPassing', 'BallControl', 'Acceleration', 'SprintSpeed', 'Agility',
                             'Reactions', 'Balance','ShotPower', 'Jumping', 'Stamina', 'Strength', 'LongShots',
                             'Aggression', 'Interceptions', 'Positioning', 'Vision', 'Penalties', 'Composure', 'Marking',
                             'StandingTackle', 'SlidingTackle'] + GK_EXTRA_FEATURES

CLUSTERING_PLAYER_FEATURES_VECTOR = ['Name', 'ID', 'Position'] + FIFA_MAIN_FEATURES + GK_EXTRA_FEATURES
# ------------------------------------------
# Positions
# ------------------------------------------
# https://gaming.stackexchange.com/questions/167318/what-do-fifa-14-position-acronyms-mean

DEFENDERS = ['LCB', 'CB', 'RCB']

MIDFIELDERS = ['LB', 'LCM', 'LDM', 'LF', 'CDM', 'CM', 'LWB', 'RB', 'RCM', 'RDM', 'RWB']

FORWARDS = ['LAM', 'CAM', 'CF', 'LM', 'LS', 'LW', 'RAM', 'RF', 'RM', 'RS', 'RW', 'ST']

GOALKEEPERS = ['GK']

# ------------------------------------------
# Weights metrics: (from high sim to low)
# ------------------------------------------
# L. Modric vs Iniesta:
MIDFIELDERS_WEIGHTS_SORT = ['Dribbling', 'Strength', 'Volleys', 'Positioning', 'ShortPassing', 'LongPassing',
                            'BallControl', 'HeadingAccuracy', 'Vision', 'Reactions', 'Finishing', 'Aggression',
                            'Potential', 'Curve', 'SprintSpeed', 'Composure', 'Marking', 'Stamina', 'Height',
                            'FKAccuracy', 'Crossing', 'Acceleration', 'Balance', 'LongShots', 'Penalties', 'Agility',
                            'ShotPower', 'Interceptions', 'SlidingTackle', 'StandingTackle', 'Jumping', 'Weak Foot',
                            'defensive work rate', 'attacking work rate', 'Skill Moves']
# Cristiano Ronaldo vs Neymar Jr:
FORWARDS_WEIGHTS_SORT = ['LongPassing', 'BallControl', 'SprintSpeed', 'Composure', 'Marking', 'Reactions',
                         'Finishing', 'ShortPassing', 'Volleys', 'Penalties', 'Crossing', 'Acceleration', 'Vision',
                         'Positioning', 'Curve', 'Stamina', 'Aggression', 'Interceptions', 'StandingTackle',
                         'Dribbling', 'Agility', 'SlidingTackle', 'FKAccuracy', 'LongShots',
                         'Balance', 'ShotPower', 'Height', 'HeadingAccuracy', 'Strength', 'Jumping',
                         'attacking work rate', 'Skill Moves', 'defensive work rate', 'Weak Foot']
# Sergio Ramos vs Piqué:
DEFENDERS_WEIGHTS_SORT = ['Strength', 'Reactions', 'Vision', 'Interceptions', 'Positioning', 'ShortPassing',
                          'LongPassing', 'Composure', 'Marking', 'BallControl', 'defensive work rate',
                          'StandingTackle', 'SlidingTackle', 'HeadingAccuracy', 'LongShots', 'Penalties',
                          'Crossing', 'Volleys', 'SprintSpeed', 'Curve', 'Aggression', 'ShotPower', 'Balance',
                          'Jumping', 'Stamina', 'Height', 'Agility', 'Finishing', 'Dribbling', 'Skill Moves',
                          'Acceleration', 'Weak Foot', 'FKAccuracy', 'attacking work rate']

GOALKEPPER_WEIGHTS_SORT = ['GKDiving', 'GKHandling', 'GKKicking', 'GKPositioning', 'GKReflexes', 'Strength',
                           'Reactions', 'Vision', 'Interceptions', 'Positioning', 'ShortPassing',
                           'LongPassing', 'Composure', 'Marking', 'BallControl', 'defensive work rate',
                           'StandingTackle', 'SlidingTackle', 'HeadingAccuracy', 'LongShots', 'Penalties',
                           'Crossing', 'Volleys', 'SprintSpeed', 'Curve', 'Aggression', 'ShotPower', 'Balance',
                           'Jumping', 'Stamina', 'Height', 'Agility', 'Finishing', 'Dribbling', 'Skill Moves',
                           'Acceleration', 'Weak Foot', 'FKAccuracy', 'attacking work rate']
MAX_FEATURES_LEN = 34

GK_EXTRA_LEN = 5

MONEY_FEATURES = ['Value', 'Release Clause', 'Wage']


def get_similarity_by_article(d, lst):
    # prints sorted difference between wanted rows used to calc weights
    d = get_rows_with_col_val(d, 'Name', lst).drop(columns=['Name', 'Position'])
    diff = d.diff(-1).abs().drop(d.index[1]).to_dict('records').pop()
    print(sorted(diff.items(), key=lambda kv: kv[1]))
