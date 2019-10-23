from processmining.luigiMiner import log_to_csv


LUIGI_LOG_PATH = './data/minilogs/head_daily.2019-09-01_09-29-01.log'


def test_log_to_csv():
    df = log_to_csv(LUIGI_LOG_PATH)
    assert df['timestamp'][0] == '2019-09-01 09:29:23'
