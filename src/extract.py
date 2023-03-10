import os
import re
import pandas as pd
from paddlenlp import Taskflow
from typing import List, Literal, Optional
from components import Entity, process_result
from utils import *

class DocumentExtractor:
    def __init__(
            self,
            doc_num: int,
    ):

        self.doc_num = doc_num
        self.image_path = f'../data/images/document_{doc_num}.png'
        self.pdf_path = f'../data/Document {doc_num}.pdf'


        self.image_promt = Taskflow("document_intelligence")
        
        self.schema = load_contact_person_schema()
        self.text_promt = Taskflow("information_extraction", schema=self.schema, model='uie-base-en')




    def get_entity(self, type: str= 'contracting'):
        if type not in ['contracting', 'contractor']:
            raise ValueError("Wrong type of company entity")
        
        company_name = get_ner_orgs(convert_pdf_to_txt(self.pdf_path))[type]
        self.query = load_prompts_entity(company_name)


        if not os.path.exists(self.image_path):
            raise FileNotFoundError(f"File not found")

        outputs = self.image_promt({"doc": self.image_path, "prompt": self.query})

        self.entities = {type: {'name': company_name, 'attributes': {}}}

        self.entities[type]['attributes']['address'] = process_result(outputs[0]['result'][0])
        self.entities[type]['attributes']['taxID'] = process_result(outputs[1]['result'][0])
        self.entities[type]['attributes']['Tel'] = process_result(outputs[2]['result'][0])
        self.entities[type]['attributes']['email'] = process_result(outputs[3]['result'][0])
        self.entities[type]['attributes']['fax'] = process_result(outputs[4]['result'][0])
        return [self.entities]



    def get_project(self):
        self.project = {}
        table = get_tables(self.pdf_path)
        for key in table.keys():
            if ('project' in str.lower(key)):
                self.project[key] = table[key]

        return [self.project]

    def get_order(self):
        self.order = {}
        table = get_tables(self.pdf_path)
        for key in table.keys():
            if ('order' in str.lower(key)):
                self.order[key] = table[key]

        return [self.order]
    
    def get_dates(self):
        self.date = {}
        table = get_tables(self.pdf_path)
        for key in table.keys():
            if ('date' in str.lower(key)):
                self.date[key] = table[key]

        return [self.date]


    def get_declaration(self):
        self.declaration = {}

        text = convert_pdf_to_txt(self.pdf_path)
        
        pth = r"declaration:([\n\w\s.,°-]+\.)"
        declarations = re.findall(pth, text, re.IGNORECASE)

        if len(declarations) > 0:
            declaration = declarations[0]
        
        else:
            declaration = ''

        self.declaration['name'] = 'declaration'
        self.declaration['entity'] = declaration.strip()
        return [self.declaration]
    


    def get_contact_person(self):
        self.contact_person = {}
        text = convert_pdf_to_txt(self.pdf_path)
        person = self.text_promt(text)

        self.contact_person['name'] = 'contact_person'
        self.contact_person['entity'] = person[0]['Person'][0]['text']
        self.contact_person['position'] = person[0]['Person'][0]['relations']['Position'][0]['text']
        return [self.contact_person]
    
