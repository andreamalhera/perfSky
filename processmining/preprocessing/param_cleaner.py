"""
Find most relevant parameters in task_name and shorten task_name to only those parameters.
A parameter is relevant if 
"""
import re

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