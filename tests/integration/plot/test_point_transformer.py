import pandas as pd
from processmining.plot.point_transformer import run_point_transformer

# TODO: Move this path to a config file
LUIGI_LOG_PATH = './tests/data/input_test_run_point_transformer.csv'

def test_point_transformer():
    EXPECTED_CASES=1
    EXPECTED_ACTIVITIES=29
    df = pd.read_csv(LUIGI_LOG_PATH, index_col=0)
    result = run_point_transformer(df)
    assert len(result['case'].unique().tolist())==EXPECTED_CASES
    assert len(result['activity'].unique().tolist())==EXPECTED_ACTIVITIES