from processmining.run import run_processmining
import pandas as pd
import os

def test_run_processmining():
    LUIGI_LOG_PATH = './tests/data'
    run_processmining(LUIGI_LOG_PATH)
    files = [file for file in os.listdir(LUIGI_LOG_PATH) if file.endswith('.log')]
    for i, filename in enumerate(files):
            log_path = LUIGI_LOG_PATH+'/'+filename
            csv_path = log_path.split('.log')[0]+'.csv'
    assert not pd.read_csv(csv_path).empty