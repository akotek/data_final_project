import pandas as pd
import os


PLAYERS_DF = pd.read_csv(os.path.join('csv', 'player_team_table.csv'))
TRANSFER_COLUMNS = ['player_id', 'previous_team_id', 'next_team_id', 'start_year_previous_team', 'last_year_next_team',
                    'end_year_next_team']


def is_nan(value):
    return value != value


def player_timeline_has_hole(player: pd.Series) -> bool:
    player = player.dropna().drop('player_id')
    for i in range(len(player.index) - 1):
        if int(player.index[i + 1]) - int(player.index[i]) != 1:
            return True
    return False


def count_num_of_teams(player: pd.Series):
    player = player.dropna().drop('player_id')
    current_team = player[0]
    team_counter = 1
    for team in player:
        if current_team != team:
            team_counter = team_counter + 1
            current_team = team
    return team_counter


def start_end_activity(player: pd.Series):
    start_year = -1
    for year in range(2008, 2017):
        if not is_nan(player[str(year)]):
            start_year = year
            break
    end_year = -1
    for year in range(start_year + 1, 2017):
        if is_nan(player[str(year)]):
            end_year = year - 1
            break
    if end_year == -1:
        end_year = 2016
    return start_year, end_year


def get_player_timeline(player: pd.Series, start_year, end_year, num_of_teams) -> pd.DataFrame:
    years_spent_list = [0] * num_of_teams
    team_list = [None] * num_of_teams
    start_year_list = [-1] * num_of_teams
    years_spent_list[0] = 1
    team_list[0] = player[str(start_year)]
    start_year_list[0] = start_year
    last_index = 0
    year_count = 1
    for year in range(start_year + 1, end_year + 1):
        if team_list[last_index] != player[str(year)]:
            years_spent_list[last_index] = year_count
            last_index = last_index + 1
            team_list[last_index] = player[str(year)]
            start_year_list[last_index] = year
            year_count = 1
        else:
            year_count = year_count + 1
    years_spent_list[last_index] = year_count
    df = pd.DataFrame()
    for i in range(num_of_teams - 1):
        df_other = pd.DataFrame(([[player['player_id'], team_list[i], team_list[i + 1], start_year_list[i],
                                  start_year_list[i + 1], start_year_list[i + 1] + years_spent_list[i + 1] - 1]]),
                                columns=TRANSFER_COLUMNS)
        df = pd.concat([df, df_other])
    return df


def get_transfers_of_player(player: pd.Series):
    num_of_teams = count_num_of_teams(player)
    if player_timeline_has_hole(player) or num_of_teams <= 1:
        return None
    start_year, end_year = start_end_activity(player)
    df = get_player_timeline(player, start_year, end_year, num_of_teams)
    return df


def create_all_transfers_csv():
    """
    Creates a csv that looks like this:
    player_id, previous_team_id, next_team_id, start_year_previous_team, start_year_next_team, last_year_next_team
    :return:
    """
    df_transfers = pd.DataFrame()
    for index, player in PLAYERS_DF.iterrows():
        df = get_transfers_of_player(player)
        df_transfers = pd.concat([df, df_transfers])
    df_transfers.to_csv(os.path.join('csv', 'transfers.csv'), index=False)


if __name__ == "__main__":
    create_all_transfers_csv()
