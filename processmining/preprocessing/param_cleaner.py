"""
Find most relevant parameters in task_name and shorten task_name to only those parameters.
A parameter is relevant if 
"""
import re
import pandas as pd
import numpy as np

def extract_parameters(task_call):
    """
    Extracts everything between first '(' and last ')'. Whatever is sepparated by '='
    is stored in a dictionary of parameter, value. Positional parameters
    are stored as keys.

    :param task_call: string containing function name and parameters between '(' ')'s
    """
    task_split = task_call.split('(', 1)
    parameters = {}
    next_key = None
    key = None
    if len(task_split)>1:
        reversed_parameters = [''.join(reversed(element)) for element in task_split[1:]][0].split(')', 1)[1:]
        forward_parameters = [''.join(reversed(element)) for element in reversed_parameters][0]
        parameters_call = forward_parameters.split('=')
        #print(task_call)
        for i, element in enumerate(parameters_call):
            if next_key is None and key is None:
                key = element
                continue
            if next_key is not None:
                key = next_key
            if element.startswith('('):
                next_key = re.search('\), (.*)', element)
                value = re.search('(\(.*)\), ', element)
            else:
                next_key = re.search(', (.*)', element)
                value = re.search('(.*), ', element)
            if next_key is None:
                #Find out if elem is key or value
                value = element
            else:
                next_key = next_key.group(1)
                if element.startswith('('):
                    value = value.group(0)[:-2]
                else:
                    value = value.group(1)
            #print('A: ', key, value)
            parameters[key] = value
        return parameters

# TODO: Write unit test
def get_activity_new_name(old_name, column_key, column_value):
    if column_key is None:
        return old_name
    activity_name = str(old_name)+'('+str(column_key)
    if column_value is np.nan:
        activity_name = activity_name+'=None'
    else:
        activity_name = activity_name+'='+str(column_value)
    activity_name = activity_name +')'
    return activity_name

# TODO: Write unit test
def clean_insignificant_columns(df, drop_candidates):
    BLACKLIST = ['partition']
    WHITELIST = ['parameters', 'task_call']
    catt_columns = ['case', 'activity', 'start_time', 'end_time']
    columns_to_drop = []
    verified_candidates = []
    number_of_cases = len(df.groupby(['case']))
    flag =0

    for group_candidates in drop_candidates:
        for candidate in (set(group_candidates)-set(WHITELIST)):
            group_counts = df.groupby([candidate]).size().reset_index(name='counts').sort_values(by=['counts'])['counts'].tolist()
            #print(group_counts)
            if ('date' in candidate):
                verified_candidates.append(candidate)
            if len(group_counts)==1 or len(group_counts)==number_of_cases:
                if (all(item == group_counts[0] for item in group_counts) and (group_counts[0]*len(group_counts))== len(df)):
                    #print(group_counts)
                    #or all(item == number_of_cases for item in group_counts)
                    verified_candidates.append(candidate)
            else:
                flag = 1
                break
        if flag:
            first_candidate_counts = df.groupby([group_candidates[0]]).size().reset_index(name='counts')['counts'].tolist()
            if (all(first_candidate_counts==df.groupby([item]).size().reset_index(name='counts')['counts'].tolist() for item in group_candidates)):
                all(verified_candidates.append(item) for item in group_candidates[:-1])
            flag = 0
    columns_to_drop = list(set(verified_candidates)-set(catt_columns)-set(WHITELIST))
    columns_to_drop.extend(list(set(df.columns)&set(BLACKLIST)))

    df = df.drop(columns_to_drop, axis=1)
    #print('Dropped: ',columns_to_drop, ' for activity: ', df['activity'].iloc[0])

    #if (set(df.columns)-set(catt.columns)-set({'parameters', 'task_call'})==set()):
    df['activity_parametrized'] = df['activity']
    retained_columns = set(df.columns)-set(catt_columns)-set(WHITELIST)
    if not (retained_columns==set()):
        for column in retained_columns-set({'activity_parametrized'}):
            df['activity_parametrized'] = df.apply(lambda row: get_activity_new_name(row['activity_parametrized'], column, row[column]), axis=1)
    #print(df['activity'].iloc[0], 'was added', retained_columns-set({'activity_parametrized'}))
    return df

# TODO: Write unit test
def get_parametrized_activity(df):
    clean_dump = pd.DataFrame()
    return_columns = ['activity_parametrized', 'case', 'activity', 'start_time', 'end_time', 'task_call']
    non_str_columns = ['parameters']
    df = df.replace('None', np.nan)
    activities = df.groupby(['activity']).size().reset_index(name='counts').sort_values(by=['counts'], ascending=False)['activity'].tolist()
    for activity in activities:
        activity_selection = df[df['activity']==activity].sort_values(by='case')
        activity_selection = activity_selection.dropna(axis=1,how='all')
        column_selection = set(activity_selection.columns) - set(non_str_columns)

        groups_description = pd.DataFrame(columns=['column','different_groups_per_column'])
        for column in column_selection:
            #print(column,len(clean_activity_selection.groupby([column]).size().reset_index(name='counts').sort_values(by=['counts'])))
            groups_description = groups_description.append([{'column': column, 'different_groups_per_column': len(activity_selection.groupby([column]).size().reset_index(name='counts').sort_values(by=['counts']))}])
        groups_description = groups_description.reset_index()[['column','different_groups_per_column']].sort_values(by=['different_groups_per_column'])

        similar_group_descr = groups_description.groupby(by=['different_groups_per_column']).size().reset_index(name='similar_group')
        similar_group_counts = similar_group_descr[similar_group_descr['similar_group']>1]['different_groups_per_column'].tolist()
        #print('Similar number of groups with multiple appereances in Groupbys: ', similar_group_counts)

        drop_candidates = []
        for group in similar_group_counts:
            parameters = groups_description[groups_description['different_groups_per_column']==group]['column'].tolist()
            drop_candidates.append(parameters)
        #print('Groups with similar number of groups: ', drop_candidates)
        clean_dump = clean_dump.append(clean_insignificant_columns(activity_selection, drop_candidates)[return_columns])
    df = pd.merge(df, clean_dump, on=return_columns[1:], how='inner')[return_columns]
    return df

def run_param_cleaner(task_calls):
    """
    Returns dataframe containing activity name with only
    relevant parameters for column 'activity'.
    Relevant parameters being the ones that are not redundant accross activity names.

    :param task_calls: dataframe containing task_calls. E.g DumpTask( parameter=value)
    """
    task_calls['parameters'] = task_calls.apply(lambda row: extract_parameters(row['task_call']), axis=1)
    expanded_params = pd.concat([task_calls[:], task_calls['parameters'].apply(pd.Series)], axis=1)

    #activity_selection = expanded_params[expanded_params['activity']=='CrawlTask'].sort_values(by='case')
    activity_selection = expanded_params.copy()
    activity_selection = activity_selection.dropna(axis=1,how='all')
    drop_candidates = [['prev_date', 'case', 'date'], ['task_call', 'end_time', 'start_time']]
    clean_dump = clean_insignificant_columns(activity_selection, drop_candidates)
    #print(clean_dump.head())
    counts = clean_dump.groupby(['activity_parametrized']).size().reset_index(name='counts').sort_values(by=['counts'], ascending=False)
    counts = counts.sort_values(by=['counts'], ascending = False)

    subset = expanded_params[expanded_params['activity'].str.startswith('CrawlTask') & expanded_params['case'].isin(['daily.2019-09-04_23-23-01.csv','daily.2019-09-09_01-34-02.csv'])]

    params_call = get_parametrized_activity(expanded_params)
    params_call['activity'] = params_call['activity_parametrized']

    params_catt = params_call[['case', 'activity','start_time','end_time']]
    # Used to generate test data: params_catt.to_csv('./tests/data/params_catt_daily.2019-09-01_09-29-01_head.csv')
    return params_catt