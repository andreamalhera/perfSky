import pandas as pd

# TODO: Read and extract interesting information from Luigi Logs
# TODO: Save that information as csv or xes
# TODO: Use csv and xes to visualize process


def log_to_csv(input_path):
    inputfile = open(input_path, 'r')
    for row in inputfile:
        print(row)
        text = row
    df = pd.DataFrame(columns=[1, 2, 3, 4, 5])
    m = text.split(',')[0]
    return m


def run_luigi_alphaminer(log_path, output_path):
    log_to_csv(log_path)
    print(log_path)
