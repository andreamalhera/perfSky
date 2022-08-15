import datetime
import pandas as pd
import time

def get_duration(start_time, end_time):
    start = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    end = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
    duration = abs(end - start)
    return duration
    #get_duration(ex['timestamp'][10],ex['timestamp'][1])

def get_relative_timestamps(df, exclude_tasks=[]):
    """
    Adds columns 'rel_start', 'rel_end', 'num_start', 'num_end', relative to the first start and end timestamps per case to the first start and end timestamps per case..
    """
    def get_zero_points(group):
        group['zero_point'] = group['start_time'].min()
        return group

    #WIP for failing test: relatived['zero_points']=relatived['start_time'].groupby(relatived['case']).transform('min')
    relatived = df.copy()

    #print('First timestamp in dataframe ', df['start_time'].min())
    #print('Last timestamp in dataframe ',df['end_time'].max())
    grouped = df.groupby(['case'])
    grouped = grouped.apply(get_zero_points)
    print('Grouped:', len(grouped), 'columns', grouped.columns.tolist())


    relatived = pd.merge(grouped, relatived, on = ['case', 'activity', 'start_time', 'end_time'], how = 'inner') 
    print('Merged relatived:', len(relatived), 'columns', relatived.columns.tolist())

    excluding = exclude_tasks
    relatived['rel_start'] = relatived.apply(lambda row:
                                        str(get_duration(str(row['zero_point']),
                                                            str(row['start_time']))), axis=1)
    relatived['rel_end'] = relatived.apply(lambda row:
                                        str(get_duration(str(row['zero_point']),
                                                            str(row['end_time']))), axis=1)

    relatived['num_start']= list(pd.to_timedelta(relatived['rel_start'], errors="coerce").dt.total_seconds ())
    relatived['num_end']= list(pd.to_timedelta(relatived['rel_end'], errors="coerce").dt.total_seconds ())

    #relatived = relatived[['case', 'activity','rel_start', 'rel_end', 'num_start', 'num_end', 'start_time', 'end_time']]

    relatived = relatived.sort_values(by=['num_start'], ascending=True)
    relatived = relatived[~relatived['activity'].isin(excluding)].reset_index()
    #print('Exclusive: ', len(relatived), 'columns', relatived.columns.tolist())


    relatived = relatived[['case','activity','rel_start','rel_end','num_start','num_end','start_time','end_time']].iloc[: , :]
    #relatived = relatived.iloc[199:500 , :].reset_index()
    relatived = relatived.sort_values(by=['case','num_start'], ascending=True)
    #print('Relatived: ', len(relatived), 'columns', relatived.columns.tolist())
    return relatived


def get_average_trace(df):

    def get_average_times(group):

        def avg_datetime(series):
            averages = (series.sum())/len(series)
            #averages = time.strftime('%H:%M:%S', time.gmtime(averages))
            return averages

        group['average_start'] = time.strftime('%H:%M:%S', time.gmtime(avg_datetime(group['num_start'])))
        group['average_end'] = time.strftime('%H:%M:%S', time.gmtime(avg_datetime(group['num_end'])))
        group['num_start'] = avg_datetime(group['num_start'])
        group['num_end'] = avg_datetime(group['num_end'])
        group['std_num_end'] = group['num_end'].std()
        return group

    average_trace = df[['case','activity','num_start','num_end']].iloc[: , :]
    average_trace = average_trace.groupby(['activity'])
    average_trace = average_trace.apply(get_average_times)
    average_trace = average_trace.drop_duplicates('activity', keep='first').reset_index()
    average_trace['case'] = 'Average Case'
    average_trace = average_trace[['activity','average_start', 'average_end','num_start','num_end', 'case', 'std_num_end']].sort_values(by=['num_start'])
    return average_trace

def get_skyline_points(df):
    df = df.reset_index()
    df.sort_values(by=['num_start'])
    skyline = pd.DataFrame()
    for unique_case in df['case'].unique():
        max_x = []
        max_y = []
        activity = []
        case = []
        iter_case = df[df['case']==unique_case]
        for i in range(len(iter_case)):
            maxi = max(iter_case['num_start'][0:i+1].values.tolist())
            mayi = max(iter_case['num_end'][0:i+1].values.tolist())
            #print(e, maxi, mayi)
            if maxi in iter_case[iter_case['num_end']==mayi]['num_start'].values:
                max_x.append(maxi)
                max_y.append(mayi)
                activity.append(iter_case['activity'].iloc[i])
                case.append(iter_case['case'].iloc[i])
        skyline = pd.concat([skyline, pd.DataFrame({'num_start':max_x, 'num_end':max_y, 'activity': activity, 'case': case})])
    skyline = skyline.drop_duplicates().reset_index()[['num_start','num_end','activity','case']]

    return skyline
    #first_case = snippet.loc[snippet['case']==snippet['case'][0]].reset_index()
    #get_skyline_points(first_case).head()
