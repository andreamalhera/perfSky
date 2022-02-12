import pandas as pd
import pytest
from perfSky.preprocessing.catter import run_catter

# TODO: Move this path to a config file
LUIGI_LOG_PATH = './tests/data/input_test_catter.csv'

def test_run_catter():
    expected_columns = ['case', 'activity', 'start_time', 'end_time']
    df = pd.read_csv(LUIGI_LOG_PATH, index_col=0)
    catt = run_catter(df)
    assert not catt.empty
    assert set(catt.columns) == set(expected_columns)
    assert (len(open(LUIGI_LOG_PATH).readlines())-1)/2 >= len(catt)