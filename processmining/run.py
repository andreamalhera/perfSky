import datetime
import os
from processmining.pm4pyExample import run_inductiveminer_example as pm4py_example
from processmining.preprocessing.luigi_miner import run_luigi_log_miner as luigi_miner
from processmining.preprocessing.catter import run_catter as catter

# TODO: Move whole thing to self calling function so it can be tested
# TODO: Visualize process as in boxplot notebook
# TODO: Expand parameters for every task_call and clean those parameters
# FUDO: Use spark for handling big data logs in multiple pipelines
#       Take a look at sukiyaki's docker-compose.yml


def run_processmining(luigi_log_path):
# pm4py_example(TOY_XES_PATH, OUTPUT_PATH+'/just_two_cases')
    files = [file for file in os.listdir(luigi_log_path) if file.endswith('.log')]
    for i, filename in enumerate(files):
        log_path = luigi_log_path+'/'+filename
        print('Preprocessing...', log_path, ' ', i+1, '/', len(files))
        preprocessed = luigi_miner(log_path)
        preprocessed = catter(preprocessed)

        csv_path = log_path.split('.log')[0]+'.csv'
        preprocessed.to_csv(csv_path)

        print('Saved ', csv_path)

        continue

if __name__ == "__main__":
    start = datetime.datetime.now()

    TOY_CSV_PATH = './data/pm4pyexample/running-example-just-two-cases.csv'
    TOY_XES_PATH = './data/pm4pyexample/running-example-just-two-cases.xes'

# TODO: Make directory of logs a dynamic argument from make for different pipelines
    PROCESS_NAME='table-precomp' # As in directory where logs are stored
    LUIGI_LOG_PATH = './data/minilogs/'+PROCESS_NAME+'/logs/october/mongo'
    OUTPUT_PATH = './data/minilogs/'+PROCESS_NAME+'/graphs'

    run_processmining(LUIGI_LOG_PATH)

    finish = datetime.datetime.now()
    print('Running whole pipeline took: ',finish-start)

