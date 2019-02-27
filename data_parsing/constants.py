from data_parsing.utils import *

# ------------------------------------------
# Constants
# ------------------------------------------

SIMPLE_PLAYER_VECTOR = ['Name', 'ID', 'Position', 'Height', 'Work Rate', 'Weak Foot', 'Skill Moves', 'Crossing',
                        'Finishing', 'HeadingAccuracy', 'ShortPassing', 'Volleys', 'Dribbling', 'Curve', 'FKAccuracy',
                        'LongPassing', 'BallControl', 'Acceleration', 'SprintSpeed', 'Agility', 'Reactions', 'Balance',
                        'ShotPower', 'Jumping', 'Stamina', 'Strength', 'LongShots', 'Aggression', 'Interceptions',
                        'Positioning', 'Vision', 'Penalties', 'Composure', 'Marking', 'StandingTackle', 'SlidingTackle']
SIMPLE_GK_PLAYER_VECTOR = ['Name', 'ID', 'Crossing', 'Finishing', 'HeadingAccuracy',
                           'ShortPassing', 'Volleys', 'Dribbling', 'Curve', 'FKAccuracy',
                           'LongPassing', 'BallControl', 'Acceleration', 'SprintSpeed', 'Agility', 'Reactions',
                           'Balance',
                           'ShotPower', 'Jumping', 'Stamina', 'Strength', 'LongShots', 'Aggression', 'Interceptions',
                           'Positioning', 'Vision', 'Penalties', 'Composure', 'Marking', 'StandingTackle',
                           'SlidingTackle', 'GKDiving'
                                            'GKHandling', 'GKKicking', 'GKPositioning', 'GKReflexes']

# ------------------------------------------
# Positions
# ------------------------------------------
# https://gaming.stackexchange.com/questions/167318/what-do-fifa-14-position-acronyms-mean

DEFENDERS = ['CB', 'LCB', 'RCB', 'LB', 'RB', 'LWB', 'RWB', 'LB']

MIDFIELDERS = ['CM', 'LDM', 'LAM', 'RDM', 'RAM', 'CDM', 'CAM', 'LM', 'RM', 'LCM', 'RCM']

FORWARDS = ['ST', 'CF', 'LW', 'RW', 'LS', 'RS', 'LF', 'RF']

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
                         'Finishing','ShortPassing', 'Volleys', 'Penalties', 'Crossing', 'Acceleration', 'Vision',
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

MONEY_FEATURES = ['Value', 'Release Clause', 'Wage']


def get_similarity_by_article(d, lst):
    # prints sorted difference between wanted rows used to calc weights
    d = get_rows_with_col_val(d, 'Name', lst).drop(columns=['Name', 'Position'])
    diff = d.diff(-1).abs().drop(d.index[1]).to_dict('records').pop()
    print(sorted(diff.items(), key=lambda kv: kv[1]))
