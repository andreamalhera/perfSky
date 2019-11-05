from pm4py.visualization.petrinet import factory as vis_factory
from pm4py.algo.discovery.inductive import factory as inductive_miner
from pm4py.objects.log.importer.xes import factory as xes_importer
from pm4py.objects.conversion.log import factory as conversion_factory
from pm4py.objects.log.importer.csv import factory as csv_importer


def get_log_from_csv(path):
    event_stream = csv_importer.import_event_stream(path,
                                                    parameters={csv_importer.
                                                                SEP: ';'})
    for event in event_stream:
        event['case:concept:name'] = event['Case ID']
        event['case:creator'] = 'Fluxicon Nitro'
        event['concept:name'] = event['Activity']
        event['org:resource'] = event['Resource']
        event['time:timestamp'] = event['dd-MM-yyyy:HH.mm']
        print(event)
    csv_log = conversion_factory.apply(event_stream)
    return csv_log


def inductive_miner_csv(csv_path):
    csv_log = get_log_from_csv(csv_path)
    print(csv_log, '\n')
    net, initial_marking, final_marking = inductive_miner.apply(csv_log)

    for case_index, case in enumerate(csv_log):
        print(case)
        print("\n case index: %d  case id: %s" % (case_index,
              case.attributes["concept:name"]))
    for event_index, event in enumerate(case):
        print("event index: %d  event activity: %s" % (event_index,
              event["concept:name"]))

    iviz = vis_factory.apply(net, initial_marking, final_marking)

    iviz.graph_attr['bgcolor'] = 'white'
    return iviz


def inductive_miner_xes(log_path):
    xes_log = xes_importer.import_log(log_path)

    print(xes_log, '\n')
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
    return iviz


def run_inductiveminer_example(log_path, output_path):
    csv_path = log_path.split('.xes')[0]+'.csv'

    xes_iviz = inductive_miner_xes(log_path)
    vis_factory.save(xes_iviz, output_path+'_xes_im.png')

    csv_iviz = inductive_miner_csv(csv_path)
    vis_factory.save(csv_iviz, output_path+'_csv_im.png')

    # vis_factory.view(gviz)
