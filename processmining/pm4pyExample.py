import os
import pandas as pd
import collections
import json
from pm4py.visualization.petrinet import factory as vis_factory
from pm4py.algo.discovery.inductive import factory as inductive_miner
from pm4py.objects.log.adapters.pandas import csv_import_adapter
from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.objects.conversion.log import factory as conversion_factory
from pm4py.objects.log.importer.csv import factory as csv_importer


def dict_groupby(to_group, group_column):
    grouped = collections.defaultdict(list)
    for item in to_group:
        grouped[item[group_column]].append(item)
    # for item in grouped:
    #     print(item)
    # print('\n')
    print(json.dumps(grouped, indent=1))
    return grouped


def get_log_from_csv(path):
    # csv_log = csv_import_adapter.import_dataframe_from_path(path)
    # csv_log = csv_log.groupby(['Case ID'])
    # print(csv_log.head(), '\n')

    event_stream = csv_importer.import_event_stream(path)
    event_stream_length = len(event_stream)
    print(event_stream_length)
    for event in event_stream:
        print(event)
    print('\n')
    event_stream = dict_groupby(event_stream, 'Case ID')
    csv_log = conversion_factory.apply(event_stream)
    return csv_log


def run_inductiveminer_example(log_path, output_path):
    csv_path = log_path.split('.xes')[0]+'.csv'

    xes_log = xes_importer.import_log(log_path)
    csv_log = get_log_from_csv(csv_path)

    # TODO: Generate visualization from csv_log
    print('XESXESXES')
    # example_log = conversion_factory.apply(example_log)

    # example_log['concept:name'] = example_log['Activity']
    # example_log['org:resource'] = example_log['Resource']
    # example_log['time:timestamp'] = example_log['dd-MM-yyyy:HH.mm']
    # log = conversion_factory.apply(example_log)

    net, initial_marking, final_marking = inductive_miner.apply(xes_log)

    for case_index, case in enumerate(xes_log):
        print(case)
        print("\n case index: %d  case id: %s" % (case_index,
              case.attributes["concept:name"]))
    for event_index, event in enumerate(case):
        print("event index: %d  event activity: %s" % (event_index,
              event["concept:name"]))

    iviz = vis_factory.apply(net, initial_marking, final_marking)

    iviz.graph_attr['bgcolor'] = 'white'

    vis_factory.save(iviz, output_path+'_im.png')
    # vis_factory.view(gviz)
