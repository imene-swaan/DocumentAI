import os
import tabula
import pdfplumber
import pandas







def convert_pdf_to_txt(doc_num):
    with pdfplumber.open(f'../data/Document {str(doc_num)}.pdf') as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()
    
    with open(f'inputs/doc{str(doc_num)}/text.txt', 'w') as f:
        f.write(text)

    print('saved')
    return text
    

def convert_pdf_table_to_csv(doc_num):
    # Read PDF file and extract tables
    tables = tabula.read_pdf(f'../data/Document {str(doc_num)}.pdf', pages='all')

    for i, t in enumerate(tables):
        t.to_csv(f'inputs/doc{str(doc_num)}/table_{i}.csv', index=False)

    return tables




def make_dir(doc_num):
    directory = f'inputs/doc{str(doc_num)}'

    if not os.path.exists(directory):
        os.makedirs(directory)

    return directory

if __name__ == '__main__':
    for i in range(1, 6):
        make_dir(i)
        convert_pdf_to_txt(i)
        convert_pdf_table_to_csv(i)

