import pandas as pd
import re

# TODO: Save that information as csv or xes
# TODO: Use csv and xes to visualize process


def file_to_df(inputfile):
    data = pd.DataFrame(columns=['line'])
    for row in inputfile:
        data = data.append({'line': row}, ignore_index=True)
    return data


def get_task(row):
    if ' running' in row['message']:
        return re.split(r'running\s+', row['message'])[1]
    if ' done' in row['message']:
        return re.split(r'done\s+', row['message'])[1]
    return None


def get_state(row):
    if ' running' in row['message']:
        return 'start'
    if ' done' in row['message']:
        return 'done'
    return None


def get_pid(row):
    if 'pid' in row['message']:
        return int(row['message'].split('pid ')[1].split('] ')[0])
    return None


def data_from_log(input_path):
    df = pd.DataFrame(columns=['timestamp', 'number', 'mode',
                               'line_in_code', 'task', 'pid', 'state',
                               'message'])
    inputfile = open(input_path, 'r')
    data = file_to_df(inputfile)
    df['timestamp'] = data.apply(lambda row: row['line'].split(',')[0],
                                 axis=1)
    df['number'] = data.apply(lambda row:
                              row['line'].split(',')[1].split(' ')[0], axis=1)
    df['mode'] = data.apply(lambda row: re.split(r'\d{3}\s',
                            row['line'])[1].split(' ')[0], axis=1)
    df['line_in_code'] = data.apply(lambda row: re.split(r'[A-Z]+\s+',
                                    row['line'])[1].split(' - ')[0],
                                    axis=1)
    df['message'] = data.apply(lambda row: row['line'].split(' - ')[1], axis=1)
    df['pid'] = df.apply(lambda row: get_pid(row), axis=1)
    df['task'] = df.apply(lambda row: get_task(row), axis=1)
    df['state'] = df.apply(lambda row: get_state(row), axis=1)
    print(df.to_string())
    return df


def run_luigi_inductive_miner(log_path, output_path):
    df = data_from_log(log_path)
    csv_path = log_path.split('.log')[0]+'.csv'
    print(csv_path)
    df.to_csv(csv_path)
    df_after = pd.read_csv(csv_path)
    print("\n"+df_after.to_string())
