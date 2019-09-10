import os
from pm4py.algo.discovery.alpha import factory as alpha_miner
from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.visualization.petrinet import factory as vis_factory

parameters = {"timestamp_sort": True}
log = xes_importer.import_log('running-example-just-two-cases.xes')
net, initial_marking, final_marking = alpha_miner.apply(log)

for case_index, case in enumerate(log):
    print("\n case index: %d  case id: %s" % (case_index, case.attributes["concept:name"]))
    for event_index, event in enumerate(case):
        print("event index: %d  event activity: %s" % (event_index, event["concept:name"]))


gviz = vis_factory.apply(net, initial_marking, final_marking)
vis_factory.view(gviz)