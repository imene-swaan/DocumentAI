import spacy
import json



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


if __name__ == '__main__':
    for i in range(1, 3):
        make_ner('inputs/doc' + str(i) + '/')