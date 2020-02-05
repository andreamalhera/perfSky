import pandas as pd
from processmining.preprocessing.luigi_miner import data_from_log, file_to_df, run_luigi_log_miner

LUIGI_LOG_PATH = './tests/data/daily.2019-09-01_09-29-01_head.log'


def test_file_to_df():
    inputfile = open(LUIGI_LOG_PATH, 'r')
    df = file_to_df(inputfile)
    assert not df.empty


def test_data_from_log():
    EXPECTED_NUM_OF_COLUMNS = 8
    EXPECTED_NUM_OF_ROWS = 8
    EXPECTED_FIRST_MESSAGE = 'Checking if RootTask('
    EXPECTED_COLUMNS = ['timestamp', 'task', 'state',
                        'message', 'mode', 'pid',
                        'number', 'line_in_code']

    df = data_from_log(LUIGI_LOG_PATH)
    assert not df.empty
    assert df.shape == (EXPECTED_NUM_OF_ROWS, EXPECTED_NUM_OF_COLUMNS)
    assert set(EXPECTED_COLUMNS) == set(df.columns.tolist())
    assert df['message'][0].startswith(EXPECTED_FIRST_MESSAGE)
    assert len(open(LUIGI_LOG_PATH).readlines()) >= len(df)
    # assert df.isnull().sum()==0

# TODO: Test other stuff than if file is getting written
def test_run_luigi_log_miner():
    result = run_luigi_log_miner(LUIGI_LOG_PATH)
    assert not result.empty
    assert not pd.read_csv(LUIGI_LOG_PATH.split('.log')[0]+'.csv').empty
