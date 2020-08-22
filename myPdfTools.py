import argparse
from PyPDF2 import PdfFileWriter, PdfFileReader

def extract_page(doc_name, from_page, to_page):
    # Open file
    pdf_reader = PdfFileReader(open(doc_name, 'rb'))
    # Create PDF writer
    pdf_writer = PdfFileWriter()
    # Put the pages on the writer.
    for page in range(from_page, to_page + 1):
        pdf_writer.addPage(pdf_reader.getPage(page))
    # Create the new PDF file.
    if from_page == 0:
        sufix = f'{to_page+1}'
    else:
        sufix = f'{from_page+1}-{to_page+1}'
    with open(f'document-pages-{sufix}.pdf', 'wb') as doc_file:
        pdf_writer.write(doc_file)

def split_pdf(doc_name, page_num):
    pdf_reader = PdfFileReader(open(doc_name, "rb"))
    pdf_writer1 = PdfFileWriter()
    pdf_writer2 = PdfFileWriter()
    for page in range(page_num):
        pdf_writer1.addPage(pdf_reader.getPage(page))
    for page in range(page_num, pdf_reader.getNumPages()):
        pdf_writer2.addPage(pdf_reader.getPage(page))
    with open("doc1.pdf", 'wb') as file1:
        pdf_writer1.write(file1)
    with open("doc2.pdf", 'wb') as file2:
        pdf_writer2.write(file2)


parser = argparse.ArgumentParser(description='Pdf utilities')
parser.add_argument('doc', help='Document to extract')
parser.add_argument('NumberPages', type=int, nargs='+',
                    help='Number of pages to extract')
parser.add_argument('--opc',
                    help='More options')

args = parser.parse_args()

if args.opc:
    print('Workin on that feature')

lenPages = len(args.NumberPages)
    # print(f'Len : {lenPages}')
# Substract 1 to NumberPages to coincide with the PDF num pages.
pages = [p-1 for p in args.NumberPages]
    # print(pages)
if lenPages == 1 and pages[0] >= 1:
    extract_page(args.doc, 0, pages[0])
elif lenPages == 2 and pages[0] < pages[1]:
    extract_page(args.doc, pages[0], pages[1])