
from pdf2image import convert_from_path
def load_prompts():
    query = [
        'What is the contracting entity/company?',
        'What is the address of the contracting entity/company?',
        'What is the Tax ID of the contracting entity/company?',
        'What is the Tel of the contracting entity/company?',
        'What is the Email of the contracting entity/company?',
        'What is the Fax of the contracting entity/company?',

        'What is the name of the contractor?',
        'What is the address of the contractor?',
        'What is the Tax ID of the contractor?',
        'What is the Tel of the contractor?',
        'What is the Email of the contractor?',
        'What is the Fax of the contractor?',

        'What is the project?',
        'What is the project id/no?',
        'What is the order id/no?',
        'What is the date of the project?',

        'What is the service?',
        'What are the specific services?',
        'What are the provided services?',
        'What are the contracted works?',

    ]
    return query

def convert_pdf_to_png(pdf_path: str, png_path: str):
    pages = convert_from_path(pdf_path, 500)
    for page in pages:
        page.save(png_path, 'PNG')