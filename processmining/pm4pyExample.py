import os
from pm4py.visualization.petrinet import factory as vis_factory
from pm4py.algo.discovery.inductive import factory as inductive_miner
from pm4py.objects.log.adapters.pandas import csv_import_adapter
from pm4py.objects.conversion.log import factory as conversion_factory

def run_inductiveminer_example(log_path, output_path):
    dataframe = csv_import_adapter.import_dataframe_from_path(
            os.path.join("", "", log_path), sep=",")
    log = conversion_factory.apply(dataframe)

    net, initial_marking, final_marking = inductive_miner.apply(log)

    for case_index, case in enumerate(log):
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
