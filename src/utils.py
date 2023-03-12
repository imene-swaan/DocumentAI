import re
import json
import pdfplumber
import pandas as pd
import os
import tabula
from pdf2image import convert_from_path
import requests
import spacy



def load_prompts_entity(entity):
    query = [
        f'What is the address of {entity}?',
        f'What is the Tax ID of {entity}?',
        f'What is the Telephone number of {entity}?',
        f'What is the Email of {entity}?',
        f'What is the Fax of {entity}?',
    ]
    return query

def load_prompts_project():
    query = [
        'What is the service?',
        'What are the specific services?',
        'What are the provided services?',
        'What are the contracted works?',
    ]
    return query

def load_contact_person_schema():
    schema = [{'Person': ['Company', 'Position']}]

    return schema

def read_text(path):
    with open(path, 'r') as f:
        text = f.read()
    return text


def convert_pdf_to_png(pdf_path: str, png_path: str):
    pages = convert_from_path(pdf_path, 500)
    for page in pages:
        page.save(png_path, 'PNG')

def convert_pdf_to_txt(path):
    with pdfplumber.open(path) as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()
        return text





def convert_pdf_table_to_csv(path):
    # Read PDF file and extract tables
    table = tabula.read_pdf(path, pages='all')
    if len(table) == 0:
        return {}
    
    else:
        table = table[0]
        tab = {table.iloc[i, 0]: table.iloc[i, 1] for i in range(table.shape[0])}
        tab[table.columns[0]] = table.columns[1]
        return tab


def convert_text_table_to_csv(text):
    pth = "([\w ]+):([\w \-\.\,\/\–]+).?\n"

    matchs = re.findall(pth, text)

    if len(matchs) == 0:
        return {}
    
    else:
        table = {matchs[i][0]: matchs[i][1] for i in range(len(matchs))}
        return table


def get_tables(path):
    table = convert_pdf_table_to_csv(path)
    
    if len(table) == 0:
        text = convert_pdf_to_txt(path)
        table = convert_text_table_to_csv(text)

    
    return table



def remove_table_from_text(text, tables):
    # Remove table from text
    for df in tables:
        start = df.columns[0]
        lines = df.shape[0] + 1
    
        pat = ".+\n"

        final_path = start + pat*lines

        text = re.sub(final_path, '', text)

    return text

#def make_ner(path):
    # Load the spaCy model
    nlp = spacy.load('en_core_web_trf')

    with open(path + 'text.txt', 'r') as f:
        text = f.read()

    # Process the text with spaCy
    doc = nlp(text)

    # Extract the relevant information
    companies = {'name': []}

    for ent in doc.ents:
        if ent.label_ == 'ORG':
            companies['name'].append(ent.text)

    return companies

def preprocess(text_string):
    space_pattern = '\s+'
    new_line = '\n+'
    giant_url_regex = ('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|'
        '[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
    non_word_char = '[^\w]'
    
    parsed_text = re.sub(space_pattern, ' ', text_string)
    parsed_text = re.sub(new_line, ' ', parsed_text)
    parsed_text = re.sub(giant_url_regex, '', parsed_text)
    parsed_text = re.sub(non_word_char, ' ', parsed_text)
    
    return parsed_text



def get_ner_orgs(text):

    
    API_TOKEN = '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'
    API_URL = "https://api-inference.huggingface.co/models/flair/ner-english-large"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
    
    text = preprocess(text)
        
    ners = query({"inputs": text})
    output = [org['word'] for org in ners if org['entity_group'] == 'ORG']
    output = list(map(lambda x: str.lower(x), output))

    from nltk.corpus import stopwords
    stop_words = list(set(stopwords.words('english')))

    for company in output:
        for word in company.split(' '):
            if word in stop_words:
                output.remove(company)
                break
        

    c = {x : output.count(x) for x in set(output)}

    companies = {}

    companies['contractor'] = max(c, key=c.get)
    companies['contracting'] = min(c, key=c.get)

    return companies


if __name__ == '__main__':
    for i in range(1, 6):
        table = convert_pdf_table_to_csv(f'../data/Document {str(i)}.pdf')
        print(table)
