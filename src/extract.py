import os
import re

from paddlenlp import Taskflow
from typing import List
from components import Entity, process_result
from utils import read_text

class DocumentExtractor:
    def __init__(
            self,
            query: List[str],
            schema: List[dict]
    ):
        self.image_promt = Taskflow("document_intelligence")
        self.query = query


        self.schema = schema
        self.text_promt = Taskflow("information_extraction", schema=self.schema, model='uie-base-en')

        

        self.contracting_entity = {}
        self.contractor_entity = {}
        self.attributes = {}
        self.project = {}
        self.services = {}

        self.declaration = {}
        self.contact_person = {}

    def extract(self, image_path: str):
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"File {image_path} not found")

        outputs = self.image_promt({"doc": image_path, "prompt": self.query})

        self.attributes['entity'] = process_result(outputs[0]['result'][0])
        self.attributes['address'] = process_result(outputs[1]['result'][0])
        self.attributes['taxID'] = process_result(outputs[2]['result'][0])
        self.attributes['num'] = process_result(outputs[3]['result'][0])
        self.attributes['email'] = process_result(outputs[4]['result'][0])
        self.attributes['fax'] = process_result(outputs[5]['result'][0])

        self.contracting_entity['name'] = 'Contracting Entity'
        self.contracting_entity['attributes'] = Entity(**self.attributes).dict()


        self.attributes['entity'] = process_result(outputs[6]['result'][0])
        self.attributes['address'] = process_result(outputs[7]['result'][0])
        self.attributes['taxID'] = process_result(outputs[8]['result'][0])
        self.attributes['num'] = process_result(outputs[9]['result'][0])
        self.attributes['email'] = process_result(outputs[10]['result'][0])
        self.attributes['fax'] = process_result(outputs[11]['result'][0])

        self.contractor_entity['name'] = 'Contractor Entity'
        self.contractor_entity['attributes'] = Entity(**self.attributes).dict()

        self.project['project'] = process_result(outputs[12]['result'][0])
        self.project['project_id'] = process_result(outputs[13]['result'][0])
        self.project['order_id'] = process_result(outputs[14]['result'][0])
        self.project['date'] = process_result(outputs[15]['result'][0])
        self.project['address'] = process_result(outputs[16]['result'][0])
        

        # check in self.project if there are any empty values
        self.project = {k: v for k, v in self.project.items() if v != ''}

        self.services['service'] = process_result(outputs[17]['result'][0])
        self.services['specific_services'] = process_result(outputs[19]['result'][0])
        self.services['provided_services'] = process_result(outputs[19]['result'][0])
        self.services['contracted_works'] = process_result(outputs[20]['result'][0])

        # return a set of all values from self.services
        self.services['services'] = list(set(self.services.values()))
        self.services.pop('service')
        self.services.pop('specific_services')
        self.services.pop('provided_services')
        self.services.pop('contracted_works')

        entities = [self.contracting_entity,
                    self.contractor_entity,
                    self.project,
                    self.services]

        return entities



    def get_declaration(self, text_path):
        if not os.path.exists(text_path):
            raise FileNotFoundError(f"File {text_path} not found")

        text = read_text(text_path)
        
        pth = r"declaration:([\n\w\s.,°-]+\.)"
        declarations = re.findall(pth, text, re.IGNORECASE)

        if len(declarations) > 0:
            declaration = declarations[0]
        
        else:
            declaration = ''

        self.declaration['name'] = 'declaration'
        self.declaration['entity'] = declaration.strip()
        return self.declaration
    


    def get_contact_person(self, text_path):
        if not os.path.exists(text_path):
            raise FileNotFoundError(f"File {text_path} not found")

        text = read_text(text_path)
        person = self.text_promt(text)

        self.contact_person['name'] = 'contact_person'
        self.contact_person['entity'] = person[0]['Person'][0]['text']
        self.contact_person['position'] = person[0]['Person'][0]['relations']['Position'][0]['text']
        return [self.contact_person]
    
