import pandas as pd
import re



def read_text(path):
    with open(path + 'text.txt', 'r') as f:
        text = f.read()
    return text

def read_table(path):
    df = pd.read_csv(path + 'table_0.csv')
    return df



def remove_table(path):
    df = pd.read_csv(path + 'table_0.csv')

    start = df.columns[0]
    lines = df.shape[0] + 1
    
    pat = ".+\n"

    final_path = start + pat*lines

    text = read_text(path)
    text = re.sub(final_path, '\n\n', text)

    return text


    
def remove_declaration(path):

    text = remove_table(path)

    pat = r"declaration:([\n\w\s.,°-]+\.)"

    text = re.sub(pat, '\n\n', text)

    with open(path + 'doc.txt', 'w') as f:
        for line in text:
            f.write(line)
         
        f.close()

if __name__ == '__main__':
    for i in range(1, 3):
        remove_table('inputs/doc' + str(i) + '/')
