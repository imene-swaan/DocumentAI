import os

from paddlenlp import Taskflow
from typing import List
from components import Entity, process_result

class DocumentExtractor:
    def __init__(
            self,
            query: List[str],
    ):
        self.doc_prompt = Taskflow("document_intelligence")
        self.query = query

        self.contracting_entity = {}
        self.contractor_entity = {}
        self.project = {}
        self.services = {}

    def extract(self, image_path: str):
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"File {image_path} not found")

        outputs = self.doc_prompt({"doc": image_path, "prompt": self.query})

        self.contracting_entity['entity'] = process_result(outputs[0]['result'][0])
        self.contracting_entity['address'] = process_result(outputs[1]['result'][0])
        self.contracting_entity['taxID'] = process_result(outputs[2]['result'][0])
        self.contracting_entity['num'] = process_result(outputs[3]['result'][0])
        self.contracting_entity['email'] = process_result(outputs[4]['result'][0])
        self.contracting_entity['fax'] = process_result(outputs[5]['result'][0])

        self.contractor_entity['entity'] = process_result(outputs[6]['result'][0])
        self.contractor_entity['address'] = process_result(outputs[7]['result'][0])
        self.contractor_entity['taxID'] = process_result(outputs[8]['result'][0])
        self.contractor_entity['num'] = process_result(outputs[9]['result'][0])
        self.contractor_entity['email'] = process_result(outputs[10]['result'][0])
        self.contractor_entity['fax'] = process_result(outputs[11]['result'][0])

        self.project['project'] = process_result(outputs[12]['result'][0])
        self.project['project_id'] = process_result(outputs[13]['result'][0])
        self.project['order_id'] = process_result(outputs[14]['result'][0])
        self.project['date'] = process_result(outputs[15]['result'][0])

        self.services['service'] = process_result(outputs[16]['result'][0])
        self.services['specific_services'] = process_result(outputs[17]['result'][0])
        self.services['provided_services'] = process_result(outputs[18]['result'][0])
        self.services['contracted_works'] = process_result(outputs[19]['result'][0])

        # return a set of all values from self.services
        self.services['services'] = list(set(self.services.values()))
        self.services.pop('service')
        self.services.pop('specific_services')
        self.services.pop('provided_services')
        self.services.pop('contracted_works')

        entities = [Entity(**self.contracting_entity).dict(),
                    Entity(**self.contractor_entity).dict(),
                    self.project,
                    self.services]

        return entities
