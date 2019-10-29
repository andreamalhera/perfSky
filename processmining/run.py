import datetime
from pm4pyExample import run_inductiveminer_example as pm4py_example
from luigiMiner import run_luigi_inductive_miner as luigi_miner


start = datetime.datetime.now()

TOY_XES_PATH = './data/pm4pyexample/running-example-just-two-cases.csv'
LUIGI_LOG_PATH = './data/minilogs/filtered_daily.2019-09-01_09-29-01.log'
OUTPUT_PATH = './data/pm4pyexample'

#pm4py_example(TOY_XES_PATH, OUTPUT_PATH+'/just_two_cases')
luigi_miner(LUIGI_LOG_PATH, OUTPUT_PATH+'/luigi_alphaminer.png')

finish = datetime.datetime.now()
print(finish-start)
