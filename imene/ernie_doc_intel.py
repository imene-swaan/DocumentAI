import json
from paddlenlp import Taskflow



docprompt = Taskflow("document_intelligence")


a = docprompt({"doc": "../data/Document 1-1.png", "prompt": ["what are the companies?"]})



with open("outputs/Document_Intelligence/doc1.json", "w") as f:
    json.dump(a, f, indent=4)

