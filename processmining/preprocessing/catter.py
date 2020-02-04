"""
Generate catt's from preprocessed csv, typically from luigi_miner.py
"""
import numpy as np
import pandas as pd

# TODO: Should fail for empty task_calls
def get_task(task_call):
    """
    Extracts task name from task_call. Removing parameters of call.

    :param task_call: call of task function from log
    """
    if isinstance(task_call, float):
        return task_call
    return task_call.split('(')[0]

# TODO: Replace 'done' with 'end' for state
def run_catter(df):
    """
    Generates a 'catt' as output with at least the following columns: 
            'case': Indicating the case/trace where the activity happend. E.g. 'daily.2019-09-04_23-23-01.csv'
            'activity': Name for activity that happend in a trace. E.g. 'CrawlTask(crawler=ty-superman)(chunk=01)'
            'start_time': Indicating when an activity started in a particular trace. E.g. '2019-09-05 01:13:08'
            'end_time': Indicating when an activity ended in a particular trace. Must be same or later than 'start_time'
                        E.g. '2019-09-05 01:13:48'

    :param df: Dataframe including at least columns: 
        'task': Describing an activity. E.g.: 'CrawlTask(date=2019-09-04_23-23-01, prev_date=2019-09-03_03-44-01)\n'
        'timestamp': E.g. '2019-09-05 01:13:08'
        'state': Can be 'start' or 'done' indicating if the log line describes the start or the end of a task.
        'source_file': Indicating name of log where the entry was extracted from. E.g.: 'daily.2019-09-04_23-23-01.csv'
    """

    df['task_call'] = df['task']
    df['task_name'] = np.where(df['task'].notnull(), df['task'].apply(get_task), df['task'])
    df = df[['task_name','state','timestamp','task_call', 'source_file']].copy()

    df['start_time'] = np.where(df['state']=='start', df['timestamp'], np.nan)
    df['end_time'] = np.where(df['state']=='done', df['timestamp'], np.nan)

    start_df = df[df['state']=='start']
    print('Start entries: ',len(start_df))

    end_df = df[df['state']=='done']
    print('End entries: ',len(end_df))

    merged = pd.merge(start_df, end_df, on=['task_call', 'source_file'], how='inner')
    merged = merged[merged['start_time_x'].notnull()]
    merged = merged[merged['end_time_y'].notnull()]

    merged['case'] = merged['source_file']
    merged['activity'] = merged['task_name_x']
    merged['start_time'] = merged['start_time_x']
    merged['end_time'] = merged['end_time_y']

    merged = merged[['case', 'activity', 'task_call', 'start_time','end_time']].copy()


    catt = merged[['case', 'activity','start_time','end_time']].copy()
    return catt
