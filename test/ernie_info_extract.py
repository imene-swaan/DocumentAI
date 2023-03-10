import json
from paddlenlp import Taskflow
import os




def get_declaration(path):
    schema = [{'Person': ['Company', 'Position']}]
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
