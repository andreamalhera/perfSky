from processmining.luigi_miner import data_from_log, file_to_df

LUIGI_LOG_PATH = './data/minilogs/daily.2019-09-01_09-29-01.log'


def test_file_to_df():
    inputfile = open(LUIGI_LOG_PATH, 'r')
    df = file_to_df(inputfile)
    assert not df.empty


def test_data_from_log():
    df = data_from_log(LUIGI_LOG_PATH)
    assert set(['timestamp', 'number', 'mode',
                'line_in_code', 'message']).issubset(df.columns)
    assert df['timestamp'][0] == '2019-09-01 09:29:23'
