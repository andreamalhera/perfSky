import pandas as pd
import re

'''
luigi_miner takes a log generated by Luigi looking e.g. like:

    2019-09-01 09:29:23,303 DEBUG    worker.py:260  - Checking if RootTask(date=2019-09-01_09-29-01, prev_date=2019-08-30_13-45-01, chunk=03) is complete
    2019-09-01 09:29:23,306 INFO     worker.py:313  - Scheduled RootTask(date=2019-09-01_09-29-01, prev_date=2019-08-30_13-45-01, chunk=03) (PENDING)
    2019-09-01 09:29:23,306 DEBUG    worker.py:260  - Checking if ChunkTask(date=2019-09-01_09-29-01, prev_date=2019-08-30_13-45-01, chunk=03) is complete
    2019-09-01 09:29:23,311 INFO     worker.py:313  - Scheduled ChunkTask(date=2019-09-01_09-29-01, prev_date=2019-08-30_13-45-01, chunk=03) (PENDING)
    2019-09-01 09:29:23,312 DEBUG    worker.py:260  - Checking if UpdateTimelineTask(date=2019-09-01_09-29-01, prev_date=2019-08-30_13-45-01, chunk=03) is complete
    2019-09-01 09:29:24,604 INFO     worker.py:313  - Scheduled UpdateTimelineTask(date=2019-09-01_09-29-01, prev_date=2019-08-30_13-45-01, chunk=03) (PENDING)
    2019-09-01 09:29:24,604 DEBUG    worker.py:260  - Checking if ChunkReviewTimelineTask(date=2019-09-01_09-29-01, prev_date=2019-08-30_13-45-01, chunk=02) is complete
    2019-09-01 09:29:25,205 INFO     worker.py:313  - Scheduled ChunkReviewTimelineTask(date=2019-09-01_09-29-01, prev_date=2019-08-30_13-45-01, chunk=02) (PENDING)
    2019-09-01 09:29:25,205 DEBUG    worker.py:260  - Checking if ReviewDedupTask(date=2019-09-01_09-29-01, prev_date=2019-08-30_13-45-01, chunk=02) is complete

    and delivers a csv with the follwing columns:
    'timestamp','number','mode','line_in_code','task','pid','state','message'

    E.g.:
    0,2019-09-01 09:29:23,303,DEBUG,worker.py:260 ,,,,
    "Checking if RootTask(date=2019-09-01_09-29-01, prev_date=2019-08-30_13-45-01, chunk=03) is complete
    "
    1,2019-09-01 09:42:15,089,INFO,worker.py:58  ,
    "DumpTask(date=2019-09-01_09-29-01, prev_date=2019-08-30_13-45-01, chunk=prep, sql_filename=daily_urls,
    kvs=None, target_filename=None, db_host=host.com, db_port=6666, db_user=user, db_name=my_db)
    ",37714.0,start,"[pid 37714] Worker Worker(salt=235269763, host=my_host, username=this-user, pid=45075) 
    running   DumpTask(date=2019-09-01_09-29-01, prev_date=2019-08-30_13-45-01, chunk=prep, sql_filename=daily_urls, 
    kvs=None, target_filename=None, db_host=host.com, db_port=6666, db_user=user, db_name=my_db)

'''

# TODO: Catch failed and restarted tasks
def file_to_df(inputfile):
    data = pd.DataFrame(columns=['line'])
    lineList = inputfile.readlines()
    for index, row in enumerate(lineList):
        if index == 0:
            data = data.append({'line': row}, ignore_index=True)
        if '[pid' in row:
            data = data.append({'line': row}, ignore_index=True)
        if index >= len(lineList)-3:
            data = data.append({'line': row}, ignore_index=True)
    pd.options.display.max_colwidth = 100
    return data


def get_task(row):
    if ' running' in row['message']:
        return re.split(r'running\s*', row['message'])[1]
    if ' done' in row['message']:
        return re.split(r'done\s*', row['message'])[1]
    return None


def get_state(row):
    if ' running' in row['message']:
        return 'start'
    if ' done' in row['message']:
        return 'done'
    return None


def get_pid(row):
    if '[pid' in row['message']:
        return int(row['message'].split('pid ')[1].split('] ')[0])
    return None


def get_message(row):
    message = re.split(r'py:\d+\s+', row['line'])[1]
    if message.startswith('- '):
        message = row['line'].split('- ')[1]
    return message


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
    df['message'] = data.apply(lambda row: get_message(row), axis=1)
    df['pid'] = df.apply(lambda row: get_pid(row), axis=1)
    df['task'] = df.apply(lambda row: get_task(row), axis=1)
    df['state'] = df.apply(lambda row: get_state(row), axis=1)

    return df

# TODO: Preprocess csv: Get rid of unnecessary info
def run_luigi_log_miner(log_path):
    df = data_from_log(log_path)
    df = df[['timestamp','task','state']]

    filename = log_path.rsplit('/', 1)[1].split('.log')[0]
    df['source_file'] = filename

    df['state'][0]='start'
    df['task'][0]='AllTasks'

    df['state'][len(df)-1]='done'
    df['task'][len(df)-1]='AllTasks'

    df = df.dropna()
    return df
