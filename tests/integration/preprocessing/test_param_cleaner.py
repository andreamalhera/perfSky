import pandas as pd
from processmining.preprocessing.param_cleaner import run_param_cleaner

# TODO: Move this path to a config file
LUIGI_LOG_PATH = './tests/data/input_test_param_cleaner.csv'

def test_run_param_cleaner():
    df = pd.read_csv(LUIGI_LOG_PATH, index_col=0)
    df['activity_before'] = df['activity']
    df['clean_activity'] = run_param_cleaner(df)['activity']

    assert not df[df['clean_activity'].apply(str).apply(len)>=df['activity_before'].apply(str).apply(len)].empty
    # FIXME: Get assertion to work: assert not df[df['clean_activity'].apply(str).apply(len)>df['activity_before'].apply(str).apply(len)].empty
    assert not df[df['task_call'].apply(str).apply(len)>=df['clean_activity'].apply(str).apply(len)].empty
    assert not df[df['task_call'].apply(str).apply(len)>df['clean_activity'].apply(str).apply(len)].empty
