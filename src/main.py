from extract import DocumentExtractor
import json
import os

if __name__ == '__main__':
    if not os.path.exists('../outputs'):
        os.mkdir('../outputs')
    for i in range(1, 6):
        print(i)
        data = []
        doc = DocumentExtractor(i)

        data += doc.get_entity('contracting')
        data += doc.get_entity('contractor')

        data += doc.get_project()
        data += doc.get_order()
        data += doc.get_dates()

        data += doc.get_services()

        data += doc.get_declaration()
        data += doc.get_contact_person()

        with open('../outputs/{}.json'.format(i), 'w') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


        
