import pandas as pd

# TODO: Save that information as csv or xes
# TODO: Use csv and xes to visualize process


def log_to_csv(input_path):
    df = pd.DataFrame(columns=['timestamp', 'number', 'mode',
                               'line_in_code', 'message'])
    inputfile = open(input_path, 'r')
    for row in inputfile:
        timestamp = row.split(',')[0]
        rest = row.split(',')[1]
        number = rest.split(' ')[0]
        rest = rest.split(' ')[1]
        mode = rest.split(' ')[0]
        rest = row.split(mode+'   ')[1]
        line_in_code = rest.split('  - ')[0]
        message = rest.split('  - ')[1]
        df = df.append({'timestamp': timestamp, 'number': number,
                        'mode': mode, 'line_in_code': line_in_code,
                        'message': message}, ignore_index=True)
    return df


def run_luigi_alphaminer(log_path, output_path):
    log_to_csv(log_path)
    print(log_path)
