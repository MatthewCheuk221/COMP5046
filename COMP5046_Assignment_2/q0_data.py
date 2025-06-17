import json

# This is the function you need to implement
def read_data(filename):
    """Read the data from a json file.

    Keyword arguments:
    filename -- the name of a json file
    """
    
    with open(filename, 'r') as json_file:
        json_data = json.load(json_file)

    data = {'train': [], 'dev': [], 'test': []}
    queries = set()
    for example in json_data:
        data[example['data']].append((example['question'], example['sql']))
        queries.add(example['sql'])

    return data, queries