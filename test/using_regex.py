import re
import os
import json

directory = 'outputs/Declaration/Regex/'
if not os.path.exists(directory):
    os.makedirs(directory)


def get_declaration(path):

    pth = r"declaration:([\n\w\s.,°-]+\.)"
    with open(path, 'r') as f:
        a = f.read()
    
    
    b = re.findall(pth, a, re.IGNORECASE)

    if len(b) > 0:
        b = b[0]
    return b


if __name__ == '__main__':
    for i in range(1, 6):
        print(i)
        a = get_declaration('inputs/doc' + str(i) + '/text.txt')
        with open(directory + 'doc' + str(i) + '.json', 'w') as f:
            json.dump(a, f, indent=4)