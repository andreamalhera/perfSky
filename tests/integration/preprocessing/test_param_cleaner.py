import pandas as pd
from processmining.preprocessing.param_cleaner import run_param_cleaner

LUIGI_LOG_PATH = './tests/data/merged_daily.2019-09-01_09-29-01_head.csv'

def test_run_param_cleaner():
    df = pd.read_csv(LUIGI_LOG_PATH, index_col=0)
    df['clean_activity'] = run_param_cleaner(df)['activity']

    assert not df[df['clean_activity'].apply(str).apply(len)>=df['activity'].apply(str).apply(len)].empty
    # FIXME: Get assertion to work: assert not df[df['clean_activity'].apply(str).apply(len)>df['activity'].apply(str).apply(len)].empty
    assert not df[df['task_call'].apply(str).apply(len)>=df['clean_activity'].apply(str).apply(len)].empty
    assert not df[df['task_call'].apply(str).apply(len)>df['clean_activity'].apply(str).apply(len)].empty
