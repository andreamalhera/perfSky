from pm4pyExample import run_example
# TODO: Read and extract interesting information from Luigi Logs
# TODO: Save that information as csv or xes
# TODO: Use csv and xes to visualize process

LOG_PATH = './data/dockervolume/running-example-just-two-cases.xes'
OUTPUT_PATH = './data/dockervolume/example.png'

run_example(LOG_PATH, OUTPUT_PATH)
