

from extract import DocumentExtractor
from utils import load_prompts
import json

if __name__ == '__main__':
    doc = DocumentExtractor(
        query=load_prompts(),
    )

    with open('output_entities.json', 'w') as f:
        json.dump(doc.extract('../data/images/document_5.png'), f, indent=4)