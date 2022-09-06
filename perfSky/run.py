import datetime
import os
import pandas as pd 

from difflib import SequenceMatcher
from perfSky.preprocessing.luigi_miner import run_luigi_log_miner as luigi_miner
from perfSky.preprocessing.catter import run_catter as catter
from perfSky.Skyline import get_relative_timestamps
from perfSky import Visualizer as visualizer
from perfSky.Skyline import get_relative_timestamps

# TODO: Move whole thing to self calling function so it can be tested
# TODO: Visualize process as in boxplot notebook
# TODO: Expand parameters for every task_call and clean those parameters
# FUDO: Use spark for handling big data logs in multiple pipelines
#       Take a look at sukiyaki's docker-compose.yml

# TODO: Not only for 2 strings but list of string
def longestSubstring(str1,str2):

     # initialize SequenceMatcher object with
     # input string 
     seqMatch = SequenceMatcher(None,str1,str2)

     # find match of longest sub-string
     # output will be like Match(a=0, b=0, size=5)
     match = seqMatch.find_longest_match(0, len(str1), 0, len(str2)) 

     # print longest substring
     if (match.size!=0):
          result = str1[match.a: match.a + match.size]
          print (result)
          return result
     else:
          print ('No longest common sub-string found')


def run_preprocessing(luigi_log_path):
    appended_preprocessed = pd.DataFrame()
    files = [file for file in os.listdir(luigi_log_path) if file.endswith('.log')]

    for i, filename in enumerate(files):
        log_path = luigi_log_path+'/'+filename
        print('\nPreprocessing...', log_path, ' ', i+1, '/', len(files))
        preprocessed = luigi_miner(log_path)
        preprocessed = catter(preprocessed)
        appended_preprocessed = appended_preprocessed.append(preprocessed)
        continue

    process_name = longestSubstring(files[0].split('.log')[0],files[-1].split('.log')[0])
    csv_path = luigi_log_path+'/'+str(process_name)+'.csv'
    appended_preprocessed.to_csv(csv_path)
    print('Saved ', csv_path)
    return csv_path

def run_visualization(csv_path):
    event_log=pd.read_csv(csv_path, index_col=0)
    event_log=get_relative_timestamps(event_log,['AllTasks'])#WIP


if __name__ == "__main__":
    start = datetime.datetime.now()

    TOY_CSV_PATH = './data/pm4pyexample/running-example-just-two-cases.csv'
    TOY_XES_PATH = './data/pm4pyexample/running-example-just-two-cases.xes'
    #pm4py_example(TOY_XES_PATH, OUTPUT_PATH+'/just_two_cases')

# TODO: Make directory of logs a dynamic argument from make for different pipelines
    PROCESS_NAME='table-precomp' # As in directory where logs are stored
    LUIGI_LOG_PATH = './data/minilogs/'+PROCESS_NAME+'/logs/october/mongo'
    OUTPUT_PATH = './data/minilogs/'+PROCESS_NAME+'/graphs'

    run_preprocessing(LUIGI_LOG_PATH)

    finish = datetime.datetime.now()
    print('Running whole pipeline took: ',finish-start)

