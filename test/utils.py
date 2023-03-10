import re
import json
import pdfplumber
import pandas
import os
import tabula



def convert_pdf_to_txt(doc_num):
    with pdfplumber.open(f'../data/Document {str(doc_num)}.pdf') as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()
        return text
    

def convert_pdf_table_to_csv(doc_num):
    # Read PDF file and extract tables
    tables = tabula.read_pdf(f'../data/Document {str(doc_num)}.pdf', pages='all')
    return tables




def make_dir(doc_num):
    directory = f'inputs/doc{str(doc_num)}/'

    if not os.path.exists(directory):
        os.makedirs(directory)

    return directory


def remove_table_from_text(text, tables):
    # Remove table from text
    for df in tables:
        start = df.columns[0]
        lines = df.shape[0] + 1
    
        pat = ".+\n"

        final_path = start + pat*lines

        text = re.sub(final_path, '', text)

    return text


def get_declaration(text):

    pth = r"declaration:([\n\w\s.,°-]+\.)"
    declarations = re.findall(pth, text, re.IGNORECASE)

    if len(declarations) > 0:
        declaration = declarations[0]
    
    else:
        declaration = ''
    return declaration






if __name__ == '__main__':
    for i in range(1, 6):
        text = convert_pdf_to_txt(i)
        tables = convert_pdf_table_to_csv(i)
        
        clean = remove_table_from_text(text, tables)
        clean = re.sub(get_declaration(text), '', clean)

        with open(f'outputs/doc{i}.txt', 'w') as f:
            f.write(clean)
        
        
        