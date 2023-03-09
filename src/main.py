
from pdf2image import convert_from_path

if __name__ == '__main__':
    for i in range(1, 6):
        pages = convert_from_path(f'../data/Document {i}.pdf', 500)
        for page in pages:
            page.save(f'document_{i}.png', 'PNG')