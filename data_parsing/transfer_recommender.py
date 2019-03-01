import pandas as pd
import os
from data_parsing.transfer_db_processing import get_player_attributes, get_team_attributes


"""
This module purpose is to rate transfer benefit for a player.
"""

# TODO: 1. Normalize and clean the Player_Attributes and Team_Attributes data.
# TODO: 2. Get feature vector V:
# TODO:     V := features of a player + features of its current team + features of its next team.
# TODO: 3. Find all transfers during 2008 - 2016 years and make the "truth" labeled data.
# TODO: 4. Think of a loss function.
# TODO: 5. Make prediction on transfer benefits using a predictor.
# TODO: 6. Because 1 - 5 tasks are ML neto (even though we're implementing an idea that Dafna said is interesting), I
# TODO:     think that maybe we should think about using something we learned in the course.

# ----------------------------------------------------------------------------------------------------------------------
# All of the SQL data in Pandas DataFrame for us to use:

TEAM_ROSTER_DF = pd.read_csv(os.path.join('csv', 'team_roster_table.csv'))
PLAYERS_DF = pd.read_csv(os.path.join('csv', 'player_team_table.csv'))
PLAYER_ATTRIBUTES_DF = get_player_attributes()
TEAM_ATTRIBUTES = get_team_attributes()
TRANSFERS = pd.read_csv(os.path.join('csv', 'transfers.csv'))


# ----------------------------------------------------------------------------------------------------------------------


def get_team(team_id, year):
    """
    Get the players of a team by its team_api_id followed by a year between 2008 - 2016
    Notes:
    1. For some of the teams the data is not available for some of the years.
    2. The players were found using the Matches table, so the team consists only of players that started at first 11
        during these matches, therefore not complete roster is available.
    :param team_id: team_api_id
    :param year: 2008 - 2016
    :return: list of players' player_api_id
    """
    roster = TEAM_ROSTER_DF[TEAM_ROSTER_DF['team_id'] == team_id][str(year)]
    if len(roster) == 0:
        print('No team data found!')
    return roster


def get_team_by_player(player_id, year):
    """
    Get the teammates of a player by his player_api_id followed by a year between 2008 - 2016
    Notes:
    1. Some of the players were not playing or retired during the 2008 - 2016, also maybe data their data is missing. If
        that's the case, then None is returned.
    2. Read the notes of get_team function.
    :param player_id: player_api_id
    :param year: 2008 - 2016
    :return: list of teammates of a player by their player_api_id
    """
    team_id = PLAYERS_DF[PLAYERS_DF['player_id'] == player_id][str(year)].item()
    if team_id != team_id:
        print('Sorry! No data about this player at this year!')
        return None
    return get_team(team_id, year)


if __name__ == "__main__":
    df = TRANSFERS
    print()
