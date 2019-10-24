import pandas as pd
import re

# TODO: Save that information as csv or xes
# TODO: Use csv and xes to visualize process


def file_to_df(inputfile):
    data = pd.DataFrame(columns=['line'])
    for row in inputfile:
        data = data.append({'line': row}, ignore_index=True)
    return data


def data_from_log(input_path):
    df = pd.DataFrame(columns=['timestamp', 'number', 'mode',
                               'line_in_code', 'message'])
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
    print(df.to_string())
    return df


def run_luigi_alphaminer(log_path, output_path):
    df = data_from_log(log_path)
    csv_path = log_path.split('.log')[0]+'.csv'
    print(csv_path)
    df_after = pd.read_csv(csv_path)
    print("\n"+df_after.to_string())
