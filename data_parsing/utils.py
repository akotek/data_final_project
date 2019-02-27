import numpy as np
import pandas as pd
import os, re
# ------------------------------------------

# Utils methods:
# ------------------------------------------

WORK_RATE = {'Medium': 50, 'Low': 0, 'High': 100}

def relpath(path):
    return os.path.join(os.path.dirname(__file__), path)


def parse_height(ht_string):
    """
    convert height string to float
    :param ht_string: the string we want to convert
    :return: height in inches as a number
    """
    # format: 7' 0.0"
    if ht_string is np.nan:
        return ht_string
    ht_ = ht_string.split("'")
    ft_ = float(ht_[0])
    in_ = float(ht_[1].replace("\"", ""))
    return (12 * ft_) + in_


def parse_weight(wt_string):
    """
    remove all char in the string and return a float
    :param wt_string: the string we wnat to remove chars
    :return: a float number
    """
    if wt_string is np.nan:
        return wt_string
    num = re.findall(r'\d+', wt_string)
    return float(num[0])


def split_work_rate(x):
    if x is np.nan:
        defensive = 0
        attacking = 0
    else:
        s = x.split('/ ')
        defensive = float(WORK_RATE[s[0]])
        attacking = float(WORK_RATE[s[1]])
    return pd.Series([defensive, attacking], index=['defensive work rate', 'attacking work rate'])


def normalize(score, max_value, min_value, max_score=100):
    return max_score * (score - min_value) / (max_value - min_value)


def get_rows_with_col_val(df, col, lst_val) -> pd.DataFrame:
    """
    Returns rows with values that fit for given column
    e.g: gets all players from DF with Position (col) of DF, RB, CD (lst_val)
    """
    return df.loc[df[col].isin(lst_val)]