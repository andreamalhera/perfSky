import pandas as pd
import pytest
from processmining.preprocessing.catter import run_catter

LUIGI_LOG_PATH = './tests/data/daily.2019-09-01_09-29-01_head_backup.csv'

def test_run_catter():
    expected_columns = ['case', 'activity', 'start_time', 'end_time']
    df = pd.read_csv(LUIGI_LOG_PATH, index_col=0)
    catt = run_catter(df)
    assert not catt.empty
    assert set(catt.columns) == set(expected_columns)
    assert (len(open(LUIGI_LOG_PATH).readlines())-1)/2 >= len(catt)