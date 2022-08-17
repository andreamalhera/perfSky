import pandas as pd
from perfSky.preprocessing.param_cleaner import filter_out_activity_params

# TODO: Move this path to a config file
LUIGI_LOG_PATH = './tests/data/input_test_run_point_transformer.csv'

def test_point_transformer():
    EXPECTED_CASES=1
    EXPECTED_ACTIVITIES=29
    df = pd.read_csv(LUIGI_LOG_PATH, index_col=0)
    result = filter_out_activity_params(df)
    assert len(result['case'].unique().tolist())==EXPECTED_CASES
    assert len(result['activity'].unique().tolist())==EXPECTED_ACTIVITIES