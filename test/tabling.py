import re
import json
import pandas as pd

for i in range(3,6):
    with open(f'../data/texts/doc{i}.txt', 'r') as f:
        text = f.read()

    pth = "([\w ]+):([\w \-\.\,\/\–]+).?\n"

    matchs = re.findall(pth, text)
    df = pd.DataFrame(matchs, columns=['key', 'value'])

    df.to_csv(f'../data/tables/doc{i}.csv', index=False, header=False)



