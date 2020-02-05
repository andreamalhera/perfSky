import datetime
import os
from pm4pyExample import run_inductiveminer_example as pm4py_example
from preprocessing.luigi_miner import run_luigi_log_miner as luigi_miner

# TODO: Visualize process as in boxplot notebook
# TODO: Expand parameters for every task_call and clean those parameters
# FUDO: Use spark for handling big data logs in multiple pipelines
#       Take a look at sukiyaki's docker-compose.yml

start = datetime.datetime.now()

TOY_CSV_PATH = './data/pm4pyexample/running-example-just-two-cases.csv'
TOY_XES_PATH = './data/pm4pyexample/running-example-just-two-cases.xes'

# TODO: Make directory of logs a dynamic argument from make for different pipelines
PROCESS_NAME='table-precomp' # As in directory where logs are stored
LUIGI_LOG_PATH = './data/minilogs/'+PROCESS_NAME+'/logs/october/mongo'
OUTPUT_PATH = './data/minilogs/'+PROCESS_NAME+'/graphs'


# pm4py_example(TOY_XES_PATH, OUTPUT_PATH+'/just_two_cases')
files = [file for file in os.listdir(LUIGI_LOG_PATH) if file.endswith('.log')]
for i, filename in enumerate(files):
    log_path = LUIGI_LOG_PATH+'/'+filename
    print('Preprocessing...', log_path, ' ', i+1, '/', len(files))
    luigi_miner(log_path)
    continue

finish = datetime.datetime.now()
print(finish-start)
