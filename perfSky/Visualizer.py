import os
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as colors
import matplotlib.lines as mlines
import numpy as np
import sys
import random

from collections import OrderedDict
from perfSky.Skyline import get_relative_timestamps, get_duration, get_average_trace, get_skyline_points

CASE_ID_COL = "case"
ACTIVITY_ID_COL = "activity"
LEN_SUBSET = 3

class Vis:
# TODO: TESTME: Write tests for this module

    def get_color_from_label(label, color):
        return color

    def title_from_list(act_selection):
        result=''
        for act in act_selection:
            result+=act+'_'
        return result

    def plot_newline(self, p1, p2):
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

    def draw_traces(self, data_selection, ax, draw_skylines=None):
        unique_trace = data_selection[CASE_ID_COL].unique().tolist()
        colormapt = cm.gist_ncar
        trace_colorlist = [colors.rgb2hex(colormapt(i)) for i in np.linspace(0, 0.9, len(unique_trace))]
        trace_legend = dict(zip(unique_trace, trace_colorlist))
        for j, k in enumerate(data_selection[CASE_ID_COL].drop_duplicates()):
            current = data_selection[data_selection[CASE_ID_COL]==k]
            l = k
            c = trace_legend.get(l)

            if draw_skylines:
                skyline = get_skyline_points(current)
                ax.plot(skyline['num_start'], skyline['num_end'], label='skyline '+k, zorder=0, color=c)
            else:
                ax.plot(current['num_start'], current['num_end'], label='trace '+k, zorder=0, color=c)

    def draw_allen_lines(self, allen_point, ax, yax, duration_plot=None):
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

    def plot_point_transformer(self, title, data_selection, activity=None, traces=None,  allen_point=None, size=None,
            duration_plot=None, draw_skylines=None, output_path=None, show_plot=None):

        def get_time_list_from_seconds(list):
            result = []
            for item in list:
                if item < 0:
                    result.append('')
                else:
                    result.append(datetime.timedelta(seconds=item))
            return result

        def sort_dict(d):
            items = [[k, v] for k, v in sorted(d.items(), key=lambda x: x[0])]
            for item in items:
                if isinstance(item[1], dict):
                    item[1] = sort_dict(item[1])
            return OrderedDict(items)

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

        fig, ax = plt.subplots()

        if size:
            fig.set_size_inches(18.5, 18.5)

        #COLORMAP = cm.nipy_spectral
        #COLORMAP = cm.prism
        #COLORMAP = cm.tab20
        COLORMAP = cm.hsv
        #COLORMAP = cm.gist_rainbow
        #COLORMAP = cm.gist_ncar

        unique_act = sorted(data_selection[ACTIVITY_ID_COL].unique().tolist())
        unique_trace = data_selection[CASE_ID_COL].unique().tolist()

        colorlist = [colors.rgb2hex(COLORMAP(i)) for i in np.linspace(0, 0.9, len(unique_act))]
        legend = dict(zip(unique_act, colorlist))
        colorby = ACTIVITY_ID_COL

        if activity:
            data_selection = data_selection.loc[data_selection[ACTIVITY_ID_COL]==activity].reset_index()
            colorlist = [colors.rgb2hex(COLORMAP(i)) for i in np.linspace(0, 0.9, len(unique_trace))]
            legend = dict(zip(unique_trace, colorlist))
            colorby = CASE_ID_COL
        elif traces:
            data_selection = data_selection.loc[data_selection[CASE_ID_COL].isin(traces)].reset_index()

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
            self.plot_newline([0,0],[max(xax,yax),max(xax,yax)])
            ax.set_ylabel('End time')
        else:
            ax.set_ylabel('Duration')

        if traces:
            self.draw_traces(data_selection, ax, draw_skylines=draw_skylines)

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

    def plot_all_traces(self, snippet, output_path=None, draw_skylines=None, show_plot=None, allen_point=None):
        traces_selection = snippet[CASE_ID_COL].drop_duplicates().tolist()
        activity_list = snippet[ACTIVITY_ID_COL].drop_duplicates().tolist()
        #print(point)
        header = 'Point transformer: All '+str(len(activity_list))+' activities in all '+str(len(traces_selection))+' traces.'

        if allen_point is not None and len(snippet[snippet['num_start']>0])>0:
            point = snippet[snippet['num_start']>0].sample(n=1)
            #point = snippet.iloc[ 1 , : ].to_frame().transpose()
            figurept = self.plot_point_transformer(header+' Allen\'s point: '+str(point[ACTIVITY_ID_COL].values)+' in '+str(point[CASE_ID_COL].values),
                    snippet, allen_point=point, traces=traces_selection,  size=1 , draw_skylines=draw_skylines,
                    output_path=output_path, show_plot=show_plot)
            #plot_point_transformer('Point transformer: All activities in all traces', snippet, size=1, allen_point=snippet[(snippet['case']==4)&(snippet['num_start']==75840)])
        else:
            figurept = self.plot_point_transformer(header, snippet, traces=traces_selection,
                    size=1 , draw_skylines=draw_skylines, output_path=output_path, show_plot=show_plot)
        return figurept

    def plot_average_trace(self, snippet, output_path = None, draw_skylines=None, show_plot=None):
        #TESTME
        #FIXME: Average End and start are only taking hours:minutes and not days into account
        #print(snippet['activity'].drop_duplicates().tolist())
        data_selection = get_average_trace(snippet).iloc[:]
        traces_selection = data_selection[CASE_ID_COL].drop_duplicates().tolist()
        if len(data_selection[data_selection['num_start']>0])>0:
            point = data_selection[data_selection['num_start']>0].sample(n=1)
            #data_selection.iloc[ 1 , : ].to_frame().transpose()
            #print(data_selection)
            figurept = self.plot_point_transformer('Point transformer: Average trace from all activities, Allen\'s point: '
                    +str(point[ACTIVITY_ID_COL].values)+' in '+str(point[CASE_ID_COL].values),
                                            data_selection, traces=traces_selection, size=1, allen_point=point,
                                            output_path=output_path, draw_skylines=draw_skylines, show_plot=show_plot)
            #plot_point_transformer('Point transformer: Average trace from all activities', snippet, allen_point=point)
        else:
            figurept =self.plot_point_transformer('Point transformer: Average trace from all activities',
                                            data_selection, traces=traces_selection, size=1, output_path=output_path,
                                            draw_skylines=draw_skylines, show_plot=show_plot)
        return figurept

    def plot_selected_activities(self, snippet, output_path = None, show_plot = None):
        #TODO: Add activity list selection as param
        #TODO: Adapt frame dynamically
        #TODO: Add start by zero option
        unique_act = snippet[ACTIVITY_ID_COL].unique().tolist()
        #print('There are ', len(unique_act), 'unique activities.')
        activity_selection=unique_act[0]
        #print(activity_selection)
        figurept = self.plot_point_transformer('Point transformer: Activity \''+ str(activity_selection) + '\' only', snippet ,
                activity=activity_selection, size=1, output_path=output_path, show_plot=show_plot)
        #print(snippet[snippet['activity']==activity_selection])

    def plot_duration_selectedtraces(self, w_duration, output_path=None, show_plot = None):
        #TODO: Suspect 'meets' line is wrong
        traces_selection = w_duration[CASE_ID_COL].drop_duplicates().tolist()[0:3]
        if len(w_duration[w_duration['num_start']>0])>0:
            point = w_duration[w_duration['num_start']>0].sample(n=1)
            #point = w_duration.iloc[ 2 , : ].to_frame().transpose()
            #print(point)
            figurept = self.plot_point_transformer('Point transformer: Trace '+ str(traces_selection) + ' only, Allen\'s point: '
                    +str(point[ACTIVITY_ID_COL].values)+' in '+str(point[CASE_ID_COL].values),
                                            w_duration, duration_plot=1, allen_point=point, traces=traces_selection, size=1,
                                            output_path=output_path, show_plot=show_plot)
            #plot_point_transformer('Point transformer: All activities in all traces', snippet, size=1, allen_point=snippet[(snippet['case']==4)&(snippet['num_start']==75840)])
        else:
            figurept = self.plot_point_transformer('Point transformer: Trace '+ str(traces_selection),
                    w_duration, duration_plot=1, traces=traces_selection, size=1, output_path=output_path, show_plot=show_plot)

    def plot_duration_alltraces(self, w_duration, output_path=None, show_plot=None): 
        #TODO: Draw skylines
        traces_selection= w_duration[CASE_ID_COL].drop_duplicates().tolist()
        if len(w_duration[w_duration['num_start']>0])>0:
            point = w_duration[w_duration['num_start']>0].sample(n=1)
            #point = w_duration.iloc[ 5 , : ].to_frame().transpose()
            #print(appended[['case','activity','start_time','end_time']].sort_values(by=['case']))
            figurept = self.plot_point_transformer('Point transformer: All activities in all traces', w_duration, size=1, duration_plot=1,
                    allen_point=point, traces=traces_selection, output_path=output_path, show_plot=show_plot)
            #plot_point_transformer('Point transformer: All activities in all traces', snippet, size=1, allen_point=snippet[(snippet['case']==4)&(snippet['num_start']==75840)])
        else:
            figurept = self.plot_point_transformer('Point transformer: All activities in all traces', w_duration, size=1, duration_plot=1,
                    traces=traces_selection, output_path=output_path, show_plot=show_plot)

    def plot_all(self, subset, output_path_prefix, show_plot=None):
        activity_sel = subset[ACTIVITY_ID_COL].apply(lambda row: row.split('(',1)[0]).unique().tolist()
        #filename_addition = title_from_list(activity_sel)
        filename_addition = ''
        output_path_prefix += '_'+filename_addition
        print('\nSubset of ', activity_sel, 'has:')
        print(len(subset), ' entries')

        unique_act = subset[ACTIVITY_ID_COL].unique().tolist()
        print(len(unique_act), 'different activities')
        #print(unique_act['activity'].tolist(),'\n')

        unique_trace = subset[CASE_ID_COL].unique().tolist()
        print(len(unique_trace), ' cases')
        #print(unique_trace, '\n')

        snippet = get_relative_timestamps(subset, ['AllTasks'])

        outputpath_seltr = output_path_prefix+'point_transformer_selectedTraces'+'.png'
        #print(outputpath_seltr)
        subset = snippet[snippet[CASE_ID_COL].isin(snippet[CASE_ID_COL].unique()[:LEN_SUBSET])]
        self.plot_all_traces(subset, output_path=outputpath_seltr, show_plot=show_plot)

        output_path_atr = output_path_prefix+'point_transformer_allTraces'+'.png'
        #print(output_path_atr)
        self.plot_all_traces(snippet, output_path=output_path_atr, show_plot=show_plot)

        output_path_atr = output_path_prefix+'point_transformer_allTraces_skyline'+'.png'
        #print(output_path_atr)
        self.plot_all_traces(snippet, output_path=output_path_atr, draw_skylines=1, show_plot=show_plot)

        output_path_avtr = output_path_prefix+'point_transformer_averageTrace'+'.png'
        #print(output_path_avtr)
        self.plot_average_trace(snippet, output_path=output_path_avtr, show_plot=show_plot)

        output_path_avtr = output_path_prefix+'point_transformer_averageTrace_skyline'+'.png'
        #print(output_path_avtr)
        self.plot_average_trace(snippet, output_path=output_path_avtr, draw_skylines=1, show_plot=show_plot)

        output_path_sa = output_path_prefix+'point_transformer_selectedAct'+'.png'
        #print(output_path_sa)
        self.plot_selected_activities(snippet, output_path=output_path_sa)

        w_duration = snippet.copy()
        w_duration['duration'] = w_duration.apply(lambda row: str(get_duration(str(row['start_time']),str(row['end_time']))), axis=1)#, show_plot=show_plot)
        w_duration['rel_end']=w_duration['duration']
        w_duration['t_duration']= w_duration.apply(lambda row: (get_duration(str(row['start_time']),str(row['end_time'])).total_seconds()), axis=1)#, show_plot=show_plot)
        w_duration['num_end']=w_duration['t_duration']
        w_duration = w_duration[[CASE_ID_COL,ACTIVITY_ID_COL,'rel_start','num_start', 'rel_end', 'num_end']]

        #print(w_duration.columns)
        #print(len(w_duration))

        output_path_st_duration = output_path_prefix+'point_transformer_duration_selectedTraces'+'.png'
        #print(output_path_st_duration)
        self.plot_duration_selectedtraces(w_duration, output_path=output_path_st_duration, show_plot=show_plot)

        output_path_duration = output_path_prefix+'point_transformer_duration_allTraces'+'.png'
        #print(output_path_duration)
        self.plot_duration_alltraces(w_duration, output_path=output_path_duration, show_plot=show_plot)

        return snippet
