import pandas as pd
import pytest
from processmining.preprocessing.catter import run_catter

LUIGI_LOG_PATH = './tests/data/daily.2019-09-01_09-29-01_head.csv'

@pytest.mark.skip(reason="Missing source_file column which should come from luigi_miner")
def test_run_catter():
    df = pd.read_csv(LUIGI_LOG_PATH, index_col=0)
    run_catter(df)
    assert True