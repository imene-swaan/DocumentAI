import spacy
import json

# Load the spaCy model
nlp = spacy.load('en_core_web_trf')

with open('../data/doc1.txt', 'r') as f:
    text = f.read()


# Process the text with spaCy
doc = nlp(text)

# Extract the relevant information
companies = {'name': []}

for ent in doc.ents:
    if ent.label_ == 'ORG':
        companies['name'].append(ent.text)


with open ('../data/doc1.json', 'w') as f:
    json.dump(companies, f, indent=4)