import json
from paddlenlp import Taskflow
import os


directory = 'outputs/Declaration/Information_extraction/'
if not os.path.exists(directory):
    os.makedirs(directory)


def get_declaration(path):
    schema = [{'Declaration': ['declar', 'confirms']}]
    ie_en = Taskflow('information_extraction', schema=schema, model='uie-base-en')

    with open(path + 'text.txt', 'r') as f:
        text = f.read()

    a = ie_en(text)

    return a








if __name__ == '__main__':
    for i in range(1, 6):
        a = get_declaration('inputs/doc' + str(i) + '/')
        with open(directory + 'doc' + str(i) + '.json', 'w') as f:
            json.dump(a, f, indent=4)
