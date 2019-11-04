import datetime
import os
from pm4pyExample import run_inductiveminer_example as pm4py_example
from luigiMiner import run_luigi_inductive_miner as luigi_miner


start = datetime.datetime.now()

TOY_CSV_PATH = './data/pm4pyexample/running-example-just-two-cases.csv'
TOY_XES_PATH = './data/pm4pyexample/running-example-just-two-cases.xes'
LUIGI_LOG_PATH = './data/minilogs'
OUTPUT_PATH = './data/pm4pyexample'

# pm4py_example(TOY_XES_PATH, OUTPUT_PATH+'/just_two_cases')

for filename in os.listdir(LUIGI_LOG_PATH):
    if filename.endswith('.log'):
        log_path = LUIGI_LOG_PATH+'/'+filename
        print('Preprocessing...', log_path)
        luigi_miner(log_path, OUTPUT_PATH+'/luigi_alphaminer.png')
        continue
    else:
        continue

finish = datetime.datetime.now()
print(finish-start)
