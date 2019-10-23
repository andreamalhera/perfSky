from pm4pyExample import run_alphaminer_example as pm4py_example
from luigiMiner import run_luigi_alphaminer as luigi_alphaminer

TOY_XES_PATH = './data/pm4pyexample/running-example-just-two-cases.xes'
LUIGI_LOG_PATH = './data/minilogs/daily.2019-09-01_09-29-01.log'
OUTPUT_PATH = './data/pm4pyexample'

pm4py_example(TOY_XES_PATH, OUTPUT_PATH+'/just_two_cases_alphaminer.png')
luigi_alphaminer(LUIGI_LOG_PATH, OUTPUT_PATH+'/luigi_alphaminer.png')
