import re
import json
import pdfplumber
import pandas as pd
import os
import tabula
from pdf2image import convert_from_path
import requests
import spacy
from collections import Counter



def load_prompts():
    query = [
        'What is the name of the contracting company/institution/entity?',
        'What is the address of the contracting company/institution/entity?',
        'What is the Tax ID of the contracting company/institution/entity?',
        'What is the Tel of the contracting company/institution?/entity',
        'What is the Email of the contracting company/institution?/entity',
        'What is the Fax of the contracting company/institution?/entity',


        'What is the name of the contractor company?',
        'What is the address of the contractor company?',
        'What is the Tax ID of the contractor company?',
        'What is the Tel of the contractor company?',
        'What is the Email of the contractor company?',
        'What is the Fax of the contractor company?',

        'What is the project about?',
        'What is the id/no of the project?',
        'What is the id/no of the order?',
        'What are all the dates of the project?',
        'What is the address of the service/work/project?',

        'What is the service?',
        'What are the specific services?',
        'What are the provided services?',
        'What are the contracted works?',
    ]
    return query


def load_schema():
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
    tables = tabula.read_pdf(path, pages='all')
    return tables


def convert_text_table_to_csv(text):
    pth = "([\w ]+):([\w \-\.\,\/\–]+).?\n"

    matchs = re.findall(pth, text)
    table = pd.DataFrame(matchs, columns=['key', 'value'])

    return table


def get_tables(path):
    tables = convert_pdf_table_to_csv(path)
    
    if len(tables) == 0:
        text = convert_pdf_to_txt(path)
        table = convert_text_table_to_csv(text)
    
    else:
        table = tables[0]
    
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

def make_ner(path):
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


def get_ner_orgs(text):

    
    API_TOKEN = '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'
    API_URL = "https://api-inference.huggingface.co/models/flair/ner-english-large"
    headers = {"Authorization": f"Bearer {API_TOKEN}"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()
        
    ners = query({"inputs": text,})
    output = [org['word'] for org in ners if org['entity_group'] == 'ORG']
    c = {x : output.count(x) for x in set(output)}

    companies = {'contracting': {}, 'contractor': {}}
    for key, value in c.items():
        if value == 1:
            companies['contracting']['entity'] = key
        else:
            companies['contractor']['entity'] = key

    return companies




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
        print(i)
        
        
        