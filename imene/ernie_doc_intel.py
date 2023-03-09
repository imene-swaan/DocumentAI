import json
import os
from paddlenlp import Taskflow




directory = 'outputs/Declaration/Document_Intelligence/'
if not os.path.exists(directory):
    os.makedirs(directory)


def get_declaration(path):
    docprompt = Taskflow("document_intelligence")
    a = docprompt({"doc": path, "prompt": ["declaration/confirmation:"]})
    return a




if __name__ == '__main__':
    for i in range(1, 6):
        print(i)
        a = get_declaration(f'../data/Document {i}-1.png')
        with open(directory + 'doc' + str(i) + '.json', 'w') as f:
            json.dump(a, f, indent=4)

