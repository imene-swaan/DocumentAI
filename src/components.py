
from transformers import DonutProcessor, VisionEncoderDecoderModel
import torch
import re
from PIL.Image import open as open_image
import json


if __name__ == '__main__':
    from paddlenlp import Taskflow

    # Chinese Word Segmentation
    docprompt = Taskflow("document_intelligence")
    print(docprompt({"doc": "document_3.png", "prompt": ['What are the contracted works', 'What is the project', 'What is the project ID']}))
