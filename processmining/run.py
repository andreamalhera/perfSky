import datetime
import os
from pm4pyExample import run_inductiveminer_example as pm4py_example
from preprocessing.luigi_miner import run_luigi_log_miner as luigi_miner


start = datetime.datetime.now()

TOY_CSV_PATH = './data/pm4pyexample/running-example-just-two-cases.csv'
TOY_XES_PATH = './data/pm4pyexample/running-example-just-two-cases.xes'
LUIGI_LOG_PATH = './data/minilogs/daily/logs'
OUTPUT_PATH = './data/minilogs/daily/graphs'

# pm4py_example(TOY_XES_PATH, OUTPUT_PATH+'/just_two_cases')
files = [file for file in os.listdir(LUIGI_LOG_PATH) if file.endswith('.log')]
for i, filename in enumerate(files):
    log_path = LUIGI_LOG_PATH+'/'+filename
    print('Preprocessing...', log_path, ' ', i+1, '/', len(files))
    luigi_miner(log_path)
    continue

finish = datetime.datetime.now()
print(finish-start)
