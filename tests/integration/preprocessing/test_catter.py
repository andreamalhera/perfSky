import pandas as pd
import pytest
from processmining.preprocessing.catter import run_catter

LUIGI_LOG_PATH = './tests/data/daily.2019-09-01_09-29-01_head.csv'

def test_run_catter():
    expected_columns = ['case', 'activity', 'start_time', 'end_time']
    df = pd.read_csv(LUIGI_LOG_PATH, index_col=0)
    run_catter(df)
    assert not df.empty
    #assert set(df.columns) == set(expected_columns)