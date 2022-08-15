import datetime
import pandas as pd

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