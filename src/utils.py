import re
import json
import pdfplumber
import pandas as pd
import os
import tabula
from pdf2image import convert_from_path


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

def convert_pdf_to_txt(doc_num):
    with pdfplumber.open(f'../data/Document {str(doc_num)}.pdf') as pdf:
        first_page = pdf.pages[0]
        text = first_page.extract_text()
        return text



def convert_pdf_table_to_csv(doc_num):
    # Read PDF file and extract tables
    tables = tabula.read_pdf(f'../data/Document {str(doc_num)}.pdf', pages='all')
    return tables



def convert_text_to_table(text):
    pth = "([\w ]+):([\w \-\.\,\/\–]+).?\n"

    matchs = re.findall(pth, text)
    df = pd.DataFrame(matchs, columns=['key', 'value'])

    return df

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
