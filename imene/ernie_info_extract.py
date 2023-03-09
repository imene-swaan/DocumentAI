import json
from paddlenlp import Taskflow
import os


directory = 'outputs/Information_extraction'
if not os.path.exists(directory):
    os.makedirs(directory)


schema = [{
          'Declaration': ['Declare']
          }]
ie_en = Taskflow('information_extraction', schema=schema, model='uie-base-en')


with open('../data/doc5.txt', 'r') as f:
    text = f.read()

a = ie_en(text)






with open("outputs/Information_extraction/doc5.json", "w") as f:
    json.dump(a, f, indent=4)

