import datetime
import pandas as pd
import time

from perfSky.config import CASE_ID_COL, ACTIVITY_ID_COL

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

    #WIP for failing test: relatived['zero_points']=relatived['start_time'].groupby(relatived[CASE_ID_COL]).transform('min')
    relatived = df.copy()

    #print('First timestamp in dataframe ', df['start_time'].min())
    #print('Last timestamp in dataframe ',df['end_time'].max())
    grouped = df.groupby([CASE_ID_COL])
    grouped = grouped.apply(get_zero_points)
    print('Grouped:', len(grouped), 'columns', grouped.columns.tolist())


    relatived = pd.merge(grouped, relatived, on = [CASE_ID_COL, ACTIVITY_ID_COL, 'start_time', 'end_time'], how = 'inner') 
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

    #relatived = relatived[[CASE_ID_COL, ACTIVITY_ID_COL,'rel_start', 'rel_end', 'num_start', 'num_end', 'start_time', 'end_time']]

    relatived = relatived.sort_values(by=['num_start'], ascending=True)
    relatived = relatived[~relatived[ACTIVITY_ID_COL].isin(excluding)].reset_index()
    #print('Exclusive: ', len(relatived), 'columns', relatived.columns.tolist())


    relatived = relatived[[CASE_ID_COL,ACTIVITY_ID_COL,'rel_start','rel_end','num_start','num_end','start_time','end_time']].iloc[: , :]
    #relatived = relatived.iloc[199:500 , :].reset_index()
    relatived = relatived.sort_values(by=[CASE_ID_COL,'num_start'], ascending=True)
    #print('Relatived: ', len(relatived), 'columns', relatived.columns.tolist())
    return relatived


def get_average_trace(df):
    #FIXME: Average End and start are only taking hours:minutes and not days into account
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

    average_trace = df[[CASE_ID_COL,ACTIVITY_ID_COL,'num_start','num_end']].iloc[: , :]
    average_trace = average_trace.groupby([ACTIVITY_ID_COL])
    average_trace = average_trace.apply(get_average_times)
    average_trace = average_trace.drop_duplicates(ACTIVITY_ID_COL, keep='first').reset_index()
    average_trace[CASE_ID_COL] = 'Average Case'
    average_trace = average_trace[[ACTIVITY_ID_COL,'average_start', 'average_end','num_start','num_end', CASE_ID_COL, 'std_num_end']].sort_values(by=['num_start'])
    return average_trace

def get_skyline_points(df):
    df = df.reset_index()
    df.sort_values(by=['num_start'])
    skyline = pd.DataFrame()
    for unique_case in df[CASE_ID_COL].unique():
        max_x = []
        max_y = []
        activity = []
        case = []
        iter_case = df[df[CASE_ID_COL]==unique_case]
        for i in range(len(iter_case)):
            maxi = max(iter_case['num_start'][0:i+1].values.tolist())
            mayi = max(iter_case['num_end'][0:i+1].values.tolist())
            #print(e, maxi, mayi)
            if maxi in iter_case[iter_case['num_end']==mayi]['num_start'].values:
                max_x.append(maxi)
                max_y.append(mayi)
                activity.append(iter_case[ACTIVITY_ID_COL].iloc[i])
                case.append(iter_case[CASE_ID_COL].iloc[i])
        skyline = pd.concat([skyline, pd.DataFrame({'num_start':max_x, 'num_end':max_y, ACTIVITY_ID_COL: activity, CASE_ID_COL: case})])
    skyline = skyline.drop_duplicates().reset_index()[['num_start','num_end',ACTIVITY_ID_COL,CASE_ID_COL]]

    return skyline
    #first_case = snippet.loc[snippet[CASE_ID_COL]==snippet[CASE_ID_COL][0]].reset_index()
    #get_skyline_points(first_case).head()

def get_average_skyline(df):
    average_trace = get_average_trace(df).iloc[:]
    result = get_skyline_points(average_trace)
    return result

def get_skyline_average(df):
    skyline_points = get_skyline_points(df)
    result = get_average_trace(skyline_points).iloc[:]
    return result

def get_skyline_activity_set(df):
    """
    Computes following stats for an event_log with start and end timestamps:
        ACTIVITY_ID_COL: Unique ACTIVITY_ID_COL as in param df. E.g. 'CrawlTask'
        'total_points_in_activity': Number of appearances of ACTIVITY_ID_COL in all cases. E.g. 5030
        'points_in_skyline': Number of appearances of ACTIVITY_ID_COL in all skylines. Must be lower or equal to
            'total_points_in_activity'. E.g. 123
        'cases_in_skyline': Number of cases, where ACTIVITY_ID_COL appears in skyline. Must be lower or equal to
            'points_in_skyline'. E.g. 5
        'probability_activity_in_skyline': 'cases_in_skyline' divided by number of cases which contain ACTIVITY_ID_COL. Between 0 and 100% E.g. 100%

    :param df: Dataframe including at least colimns:
        CASE_ID_COL: Indicating the case/trace where the activity happened. E.g. 'daily.2019-09-04_23-23-01'
        ACTIVITY_ID_COL: Name for activity that happened in a case. E.g. 'CrawlTask'
        'start_time': Indicating when an event (activity appearance) started in a particular case. E.g. '2019-09-05 01:13:08'
        'end_time': Indicating when an event ended in a particular case. Must be same or later than 'start_time'
            E.g. '2019-09-05 01:13:48'
    """
    skyline_points = get_skyline_points(df)
    representative = skyline_points[[CASE_ID_COL,ACTIVITY_ID_COL]].drop_duplicates()
    all_by_activity = df.groupby(ACTIVITY_ID_COL).size().reset_index(name='total_points_in_activity').sort_values(by=['total_points_in_activity'], ascending=False)
    skyline_by_activity = skyline_points.groupby(ACTIVITY_ID_COL).size().reset_index(name='points_in_skyline').sort_values(by=['points_in_skyline'], ascending=False)
    r_by_activity = representative.groupby(ACTIVITY_ID_COL).size().reset_index(name='cases_in_skyline').sort_values(by=['cases_in_skyline'], ascending=False)
    by_activity = r_by_activity.merge(skyline_by_activity, on=ACTIVITY_ID_COL)
    #by_activity = by_activity.merge(all_by_activity, on=ACTIVITY_ID_COL)
    #all_by_activity.plot.hist(bins=16, alpha=0.5)

    merged_by_activity = by_activity.merge(all_by_activity)[[ACTIVITY_ID_COL,'total_points_in_activity','points_in_skyline', 'cases_in_skyline']].sort_values(by=['total_points_in_activity'], ascending=False)
    #merged_by_activity['skyline_percentage'] = round(merged_by_activity.apply(lambda row: row['points_in_skyline']/row['total_points_in_activity']*100, axis=1),2)

    total_diffferent_cases= len(df[CASE_ID_COL].unique())
    total_points_in_skyline = merged_by_activity['points_in_skyline'].sum()

    merged_by_activity['probability_activity_in_skyline']=round(merged_by_activity.apply(lambda row: row['cases_in_skyline']/total_diffferent_cases*100, axis=1),2)
    #merged_by_activity['prob_skyline_appearance']=round(merged_by_activity.apply(lambda row: row['points_in_skyline']/(total_points_in_skyline/total_diffferent_cases)*100, axis=1),2)
    #print(len(merged_by_activity))
    result = merged_by_activity.sort_values(by='probability_activity_in_skyline', ascending=False)

    return result
