

from extract import DocumentExtractor
from utils import load_prompts, load_schema
import json

if __name__ == '__main__':
    for i in range(1, 6):
        print(i)
        doc = DocumentExtractor(
            query=load_prompts(),
            schema = load_schema()
        )

        meta_data = doc.extract(f'../data/images/document_{i}.png')

        meta_data.append(doc.get_declaration(f'../data/texts/doc{i}.txt'))
        meta_data.append(doc.get_contact_person(f'../data/texts/doc{i}.txt'))
        with open(f'outputs/doc{i}.json', 'w') as f:
            json.dump(meta_data, f, indent=4)
