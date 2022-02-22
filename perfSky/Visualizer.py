import os
import pandas as pd
import datetime
import time
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.lines as mlines
import numpy as np
import sys
import random

from collections import OrderedDict

class Vis:
    # TODO: Move all drawing helper functions to own file.
    # TODO: TESTME: Write tests for this module

    def get_color_from_label(label, color):
        return color

    def multiline_text(text, max_in_line):
        many_lines = []
        result=''
        i=0
        while len(text)>max_in_line and i==0:
            many_lines.append(text[0:max_in_line+1])
            text = text[max_in_line+1:]
        if len(text):
            many_lines.append(text)
        for item in many_lines:
            result += item + '\n'
        return result

    def title_from_list(act_selection):
        result=''
        for act in act_selection:
            result+=act+'_'
        return result

    def plot_newline(p1, p2):
        ax = plt.gca()
        xmin, xmax = ax.get_xbound()

        if(p2[0] == p1[0]):
            xmin = xmax = p1[0]
            ymin, ymax = ax.get_ybound()
        else:
            ymax = p1[1]+(p2[1]-p1[1])/(p2[0]-p1[0])*(xmax-p1[0])
            ymin = p1[1]+(p2[1]-p1[1])/(p2[0]-p1[0])*(xmin-p1[0])

        l = mlines.Line2D([xmin,xmax], [ymin,ymax], color='grey', linestyle='--', linewidth=1)
        ax.add_line(l)
        return l

    def draw_traces(data_selection, ax, draw_skylines=None):
        unique_trace = data_selection['case'].unique().tolist()
        colormapt = cm.gist_ncar
        trace_colorlist = [colors.rgb2hex(colormapt(i)) for i in np.linspace(0, 0.9, len(unique_trace))]
        trace_legend = dict(zip(unique_trace, trace_colorlist))
        for j, k in enumerate(data_selection['case'].drop_duplicates()):
            current = data_selection[data_selection['case']==k]
            l = k
            c = trace_legend.get(l)

            if draw_skylines:
                skyline = get_skyline_points(current)
                ax.plot(skyline['num_start'], skyline['num_end'], label='skyline '+k, zorder=0, color=c)
            else:
                ax.plot(current['num_start'], current['num_end'], label='trace '+k, zorder=0, color=c)

    def draw_allen_lines(allen_point, ax, yax, duration_plot=None):
                x = allen_point['num_start'].values[0]
                y = allen_point['num_end'].values[0]

                if duration_plot:
                    ax.axvline(x, c='grey', linewidth=1, linestyle='--')
                    ax.axvline(x+y, c='grey', linewidth=1, linestyle='--')
                    plot_newline([x,y],[x+2*y,-y])
                    plot_newline([x-y,y],[x+y,-y])
                else:
                    ax.plot([x,x],[x,yax],'k-', c='grey', linewidth=1, linestyle='--')
                    ax.plot([y,y],[y,yax],'k-', c='grey', linewidth=1, linestyle='--')
                    ax.plot([0,x],[x,x],'k-', c='grey', linewidth=1, linestyle='--')
                    ax.plot([0,y],[y,y],'k-', c='grey', linewidth=1, linestyle='--')

    def sort_dict(d):
        items = [[k, v] for k, v in sorted(d.items(), key=lambda x: x[0])]
        for item in items:
            if isinstance(item[1], dict):
                item[1] = sort_dict(item[1])
        return OrderedDict(items)

    def plot_point_transformer(title, data_selection, activity=None, traces=None,  allen_point=None, size=None,
            duration_plot=None, draw_skylines=None, output_path=None, show_plot=None):
        fig, ax = plt.subplots()

        if size:
            fig.set_size_inches(18.5, 18.5)

        #colormap = cm.nipy_spectral
        #colormap = cm.prism
        #colormap = cm.tab20
        colormap = cm.hsv
        #colormap = cm.gist_rainbow
        #colormap = cm.gist_ncar

        unique_act = sorted(data_selection['activity'].unique().tolist())
        unique_trace = data_selection['case'].unique().tolist()

        colorlist = [colors.rgb2hex(colormap(i)) for i in np.linspace(0, 0.9, len(unique_act))]
        legend = dict(zip(unique_act, colorlist))
        colorby = 'activity'

        if activity:
            data_selection = data_selection.loc[data_selection['activity']==activity].reset_index()
            colorlist = [colors.rgb2hex(colormap(i)) for i in np.linspace(0, 0.9, len(unique_trace))]
            legend = dict(zip(unique_trace, colorlist))
            colorby = 'case'
        elif traces:
            data_selection = data_selection.loc[data_selection['case'].isin(traces)].reset_index()

        for i, e in enumerate(data_selection['num_start']):
            x = data_selection['num_start'][i]
            y = data_selection['num_end'][i]
            l = data_selection[colorby][i]
            c = legend.get(l)

            ax.scatter(x, y, label=l, s=50, linewidth=0.1, c=c)

        yin, yax= ax.get_ylim()
        xin, xax= ax.get_xlim()
        ax.set_xlim(xmin=0)
        ax.set_ylim(ymin=0)

        if not duration_plot:
            #Draw diagonal
            plot_newline([0,0],[max(xax,yax),max(xax,yax)])
            ax.set_ylabel('End time')
        else:
            ax.set_ylabel('Duration')

        if traces:
            draw_traces(data_selection, ax, draw_skylines=draw_skylines)

#    if not allen_point is None :# Weird if statement because of maybe empty object or dataframe
#        draw_allen_lines(allen_point, ax, yax, duration_plot=duration_plot)

        ax.legend()

        ax.set_xlabel('Start time')

        xlocs, labels = plt.xticks()
        ylocs, labels = plt.yticks()
        plt.xticks(xlocs[1:], get_time_list_from_seconds(xlocs[1:]),rotation='vertical')
        plt.yticks(ylocs[1:], get_time_list_from_seconds(ylocs[1:]))

        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = dict(zip(labels, handles))
        by_label = sort_dict(by_label)

        #if len(by_label)>50:
        #    plt.legend(by_label.values(), by_label.keys(), loc='center left', bbox_to_anchor=(1, 0.5), ncol=2)
        #else:
        plt.legend(by_label.values(), by_label.keys(), loc='center left', bbox_to_anchor=(1, 0.5))

        #plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
        plt.title(multiline_text(title, 175))

        if output_path:
            print('Saving in ',output_path)
            fig.savefig(output_path,  bbox_inches='tight')

        if show_plot:
            plt.show()
        plt.close(fig)
        return fig


    def get_duration(start_time, end_time):
        start = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        end = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        duration = abs(end - start)
        return duration
#get_duration(ex['timestamp'][10],ex['timestamp'][1])

    def get_time_list_from_seconds(list):
        result = []
        for item in list:
            if item < 0:
                result.append('')
            else:
                result.append(datetime.timedelta(seconds=item))
        return result

    def avg_datetime(series):
        averages = (series.sum())/len(series)
        #averages = time.strftime('%H:%M:%S', time.gmtime(averages))
        return averages

    def get_average_times(group):
        group['average_start'] = time.strftime('%H:%M:%S', time.gmtime(avg_datetime(group['num_start'])))
        group['average_end'] = time.strftime('%H:%M:%S', time.gmtime(avg_datetime(group['num_end'])))
        group['num_start'] = avg_datetime(group['num_start'])
        group['num_end'] = avg_datetime(group['num_end'])
        group['std_num_end'] = group['num_end'].std()
        return group

    def get_data_selection_avgtrace(df):
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

    def get_zero_points(group):
        group['zero_point'] = group['start_time'].min()
        return group

    def get_duration(start_time, end_time):
        start = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
        end = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
        duration = abs(end - start)
        return duration
        #get_duration(ex['timestamp'][10],ex['timestamp'][1])


    def get_relative_timestamps(df, exclude_tasks=[]):
        #WIP for failing test: relatived['zero_points']=relatived['start_time'].groupby(relatived['case']).transform('min')
        relatived = df.copy()

        #print('First timestamp in dataframe ', df['start_time'].min())
        #print('Last timestamp in dataframe ',df['end_time'].max())
        grouped = df.groupby(['case'])
        grouped = grouped.apply(get_zero_points)
        #print('Grouped:', len(grouped), 'columns', grouped.columns.tolist())


        relatived = pd.merge(grouped, relatived, on = ['case', 'activity', 'start_time', 'end_time'], how = 'inner') 
        #print('Merged relatived:', len(relatived), 'columns', relatived.columns.tolist())

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

    def plot_selected_traces(snippet, output_path=None, show_plot=None):
        #plot_point_transformer('Point transformer: Trace \''+ str(snippet['case'][0]) + '\' only', snippet)
        traces_selection = snippet['case'].drop_duplicates().tolist()[0:3]
        #traces_selection = [unique_trace[1]]
        data_selection = snippet.loc[snippet['case'].isin(traces_selection)].reset_index().iloc[:]
        if len(data_selection[data_selection['num_start']>0])>0:
            point = data_selection[data_selection['num_start']>0].sample(n=1)
            #point = data_selection.iloc[ 1 , : ].to_frame().transpose()
            figurept = plot_point_transformer('Point transformer: Trace '+ str(traces_selection) + ' only, Allen\'s point: '+str(point['activity'].values)+' in '+str(point['case'].values),
                                            data_selection, size=1, traces=traces_selection, allen_point=point, output_path=output_path,
                                            show_plot=show_plot)
        else:
            figurept = plot_point_transformer('Point transformer: Trace '+ str(traces_selection) + ' only.',
                                            data_selection, size=1, traces=traces_selection, output_path=output_path, show_plot=show_plot)
        #print(data_selection[['activity','rel_start','rel_end']])

    def plot_all_traces(snippet, output_path=None, draw_skylines=None, show_plot=None):
        traces_selection = snippet['case'].drop_duplicates().tolist()
        #print(point)
        if len(snippet[snippet['num_start']>0])>0:
            point = snippet[snippet['num_start']>0].sample(n=1)
            #point = snippet.iloc[ 1 , : ].to_frame().transpose()
            figurept = plot_point_transformer('Point transformer: All activities in all traces. Allen\'s point: '+str(point['activity'].values)+' in '+str(point['case'].values), snippet, allen_point=point,
                    traces=traces_selection,  size=1 , draw_skylines=draw_skylines, output_path=output_path, show_plot=show_plot)
            #plot_point_transformer('Point transformer: All activities in all traces', snippet, size=1, allen_point=snippet[(snippet['case']==4)&(snippet['num_start']==75840)])
        else:
            figurept = plot_point_transformer('Point transformer: All activities in all traces.', snippet, traces=traces_selection,
                    size=1 , draw_skylines=1, output_path=output_path, show_plot=show_plot)
        return figurept

    def plot_average_trace(snippet, output_path = None, draw_skylines=None, show_plot=None):
        #FIXME: Average End and start are only taking hours:minutes and not days into account
        #print(snippet['activity'].drop_duplicates().tolist())
        data_selection = get_data_selection_avgtrace(snippet).iloc[:]
        traces_selection = data_selection['case'].drop_duplicates().tolist()
        if len(data_selection[data_selection['num_start']>0])>0:
            point = data_selection[data_selection['num_start']>0].sample(n=1)
            #data_selection.iloc[ 1 , : ].to_frame().transpose()
            #print(data_selection)
            figurept = plot_point_transformer('Point transformer: Average trace from all activities, Allen\'s point: '+str(point['activity'].values)+' in '+str(point['case'].values), 
                                            data_selection, traces=traces_selection, size=1, allen_point=point,
                                            output_path=output_path, draw_skylines=draw_skylines, show_plot=show_plot)
            #plot_point_transformer('Point transformer: Average trace from all activities', snippet, allen_point=point)
        else:
            figurept = plot_point_transformer('Point transformer: Average trace from all activities', 
                                            data_selection, traces=traces_selection, size=1, output_path=output_path,
                                            draw_skylines=draw_skylines, show_plot=show_plot)
        return figurept

    def plot_selected_activities(snippet, output_path = None, show_plot = None):
        #TODO: Adapt frame dynamically
        #TODO: Add start by zero option
        unique_act = snippet['activity'].unique().tolist()
        #print('There are ', len(unique_act), 'unique activities.')
        activity_selection=unique_act[0]
        #print(activity_selection)
        figurept = plot_point_transformer('Point transformer: Activity \''+ str(activity_selection) + '\' only', snippet ,
                activity=activity_selection, size=1, output_path=output_path, show_plot=show_plot)
        #print(snippet[snippet['activity']==activity_selection])

    def plot_duration_selectedtraces(w_duration, output_path=None, show_plot = None):
        #TODO: Suspect 'meets' line is wrong
        traces_selection = w_duration['case'].drop_duplicates().tolist()[0:3]
        if len(w_duration[w_duration['num_start']>0])>0:
            point = w_duration[w_duration['num_start']>0].sample(n=1)
            #point = w_duration.iloc[ 2 , : ].to_frame().transpose()
            #print(point)
            figurept = plot_point_transformer('Point transformer: Trace '+ str(traces_selection) + ' only, Allen\'s point: '+str(point['activity'].values)+' in '+str(point['case'].values),
                                            w_duration, duration_plot=1, allen_point=point, traces=traces_selection, size=1, 
                                            output_path=output_path, show_plot=show_plot)
            #plot_point_transformer('Point transformer: All activities in all traces', snippet, size=1, allen_point=snippet[(snippet['case']==4)&(snippet['num_start']==75840)])
        else:
            figurept = plot_point_transformer('Point transformer: Trace '+ str(traces_selection),
                    w_duration, duration_plot=1, traces=traces_selection, size=1, output_path=output_path, show_plot=show_plot)

#TODO: Draw skylines
    def plot_duration_alltraces(w_duration, output_path=None, show_plot=None): 
        traces_selection= w_duration['case'].drop_duplicates().tolist()
        if len(w_duration[w_duration['num_start']>0])>0:
            point = w_duration[w_duration['num_start']>0].sample(n=1)
            #point = w_duration.iloc[ 5 , : ].to_frame().transpose()
            #print(appended[['case','activity','start_time','end_time']].sort_values(by=['case']))
            figurept = plot_point_transformer('Point transformer: All activities in all traces', w_duration, size=1, duration_plot=1,
                    allen_point=point, traces=traces_selection, output_path=output_path, show_plot=show_plot)
            #plot_point_transformer('Point transformer: All activities in all traces', snippet, size=1, allen_point=snippet[(snippet['case']==4)&(snippet['num_start']==75840)])
        else:
            figurept = plot_point_transformer('Point transformer: All activities in all traces', w_duration, size=1, duration_plot=1,
                    traces=traces_selection, output_path=output_path, show_plot=show_plot)

    def plot_point_transformer_selection(subset, output_path_prefix, show_plot=None):
        activity = subset['activity'].apply(lambda row: row.split('(',1)[0]).unique().tolist()
        #filename_addition = title_from_list(activity)
        filename_addition = ''
        output_path_prefix += '_'+filename_addition
        print('\nSubset of ', activity, 'has:')
        print(len(subset), ' entries')

        unique_act = subset['activity'].unique().tolist()
        print(len(unique_act), 'different activities')
        #print(unique_act['activity'].tolist(),'\n')

        unique_trace = subset['case'].unique().tolist()
        print(len(unique_trace), ' cases')
        #print(unique_trace, '\n')

        snippet = get_relative_timestamps(subset, ['AllTasks'])

        outputpath_seltr = output_path_prefix+'point_transformer_selectedTraces'+'.png'
        #print(outputpath_seltr)
        plot_selected_traces(snippet, output_path=outputpath_seltr, show_plot=show_plot)

        output_path_atr = output_path_prefix+'point_transformer_allTraces'+'.png'
        #print(output_path_atr)
        plot_all_traces(snippet, output_path=output_path_atr, show_plot=show_plot)

        output_path_atr = output_path_prefix+'point_transformer_allTraces_skyline'+'.png'
        #print(output_path_atr)
        plot_all_traces(snippet, output_path=output_path_atr, draw_skylines=1, show_plot=show_plot)

        output_path_avtr = output_path_prefix+'point_transformer_averageTrace'+'.png'
        #print(output_path_avtr)
        plot_average_trace(snippet, output_path=output_path_avtr, show_plot=show_plot)

        output_path_avtr = output_path_prefix+'point_transformer_averageTrace_skyline'+'.png'
        #print(output_path_avtr)
        plot_average_trace(snippet, output_path=output_path_avtr, draw_skylines=1, show_plot=show_plot)

        output_path_sa = output_path_prefix+'point_transformer_selectedAct'+'.png'
        #print(output_path_sa)
        plot_selected_activities(snippet, output_path=output_path_sa)

        w_duration = snippet.copy()
        w_duration['duration'] = w_duration.apply(lambda row: str(get_duration(str(row['start_time']),str(row['end_time']))), axis=1, show_plot=show_plot)
        w_duration['rel_end']=w_duration['duration']
        w_duration['t_duration']= w_duration.apply(lambda row: (get_duration(str(row['start_time']),str(row['end_time'])).total_seconds()), axis=1, show_plot=show_plot)
        w_duration['num_end']=w_duration['t_duration']
        w_duration = w_duration[['case','activity','rel_start','num_start', 'rel_end', 'num_end']]

        #print(w_duration.columns)
        #print(len(w_duration))

        output_path_st_duration = output_path_prefix+'point_transformer_duration_selectedTraces'+'.png'
        #print(output_path_st_duration)
        plot_duration_selectedtraces(w_duration, output_path=output_path_st_duration, show_plot=show_plot)

        output_path_duration = output_path_prefix+'point_transformer_duration_allTraces'+'.png'
        #print(output_path_duration)
        plot_duration_alltraces(w_duration, output_path=output_path_duration, show_plot=show_plot)

        return snippet

    def run_point_transformer(appended):
        EXCLUDED_TASKS=['AllTasks']

        counts = appended.groupby(['activity']).size().reset_index(name='counts').sort_values(by=['counts'], ascending=False)
        counts = counts.sort_values(by=['counts'], ascending = False)
        counts.head()

        #appended = appended.head(100)
        #print(len(appended))
        unique_act = appended['activity'].unique().tolist()
        print(len(unique_act), ' activities')
        #print(unique_act)

        short_activities=[]
        for item in unique_act:
            short_name = item.split('(',1)[0]
            short_activities.append(short_name)
        unique_short_activities = list(sorted(set(short_activities)-set(EXCLUDED_TASKS)))
        print(len(unique_short_activities),' short activity names:')
        print(unique_short_activities,'\n')

        unique_trace = appended['case'].unique().tolist()
        print(len(unique_trace), ' cases')
        #print(unique_trace)

        return appended

