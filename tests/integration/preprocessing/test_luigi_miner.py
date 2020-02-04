import pandas as pd
from processmining.preprocessing.luigi_miner import data_from_log, file_to_df, run_luigi_inductive_miner

LUIGI_LOG_PATH = './tests/data/daily.2019-09-01_09-29-01_head.log'


def test_file_to_df():
    inputfile = open(LUIGI_LOG_PATH, 'r')
    df = file_to_df(inputfile)
    assert not df.empty


def test_data_from_log():
    EXPECTED_NUM_OF_COLUMNS = 8
    EXPECTED_NUM_OF_ROWS = 4
    EXPECTED_FIRST_MESSAGE = 'Checking if RootTask('
    df = data_from_log(LUIGI_LOG_PATH)
    assert not df.empty
    assert df.shape == (EXPECTED_NUM_OF_ROWS, EXPECTED_NUM_OF_COLUMNS)
    assert set(['timestamp', 'mode',
                'line_in_code', 'message']).issubset(df.columns)
    assert df['message'][0].startswith(EXPECTED_FIRST_MESSAGE)
    # assert df.isnull().sum()==0

def test_run_luigi_inductive_miner():
    run_luigi_inductive_miner(LUIGI_LOG_PATH, '')
    assert not pd.read_csv(LUIGI_LOG_PATH.split('.log')[0]+'.csv').empty
