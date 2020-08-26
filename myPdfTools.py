import sys
import argparse
from gooey import Gooey
from functools import reduce
from PyPDF2 import PdfFileWriter, PdfFileReader


#region Funtions
def extract_page(doc_name, from_page, to_page):
    # Open file
    try:
        pdf_reader = PdfFileReader(open(doc_name, 'rb'))
        numPages = pdf_reader.getNumPages()
        if numPages == 0:
            raise OSError('Check the file and try again')
        if to_page > numPages:
            raise Exception('PageOutOfRange', f'This numbers have to be less than {numPages+1}')
        # Create PDF writer
        pdf_writer = PdfFileWriter()
        # Put the pages on the writer.
        for page in range(from_page, to_page + 1):
            pdf_writer.addPage(pdf_reader.getPage(page))
    except OSError as err:
        raise Exception('FileError', f'Error readding the file: {format(err)}')
    except:
        raise
    # Create the new PDF file.
    if from_page == 0 or from_page == to_page:
        sufix = f'{to_page+1}'
    else:
        sufix = f'{from_page+1}-{to_page+1}'
    with open(f'document-pages-{sufix}.pdf', 'wb') as doc_file:
        pdf_writer.write(doc_file)

#TODO: extract args to use this function
def split_pdf(doc_name, page_num):
    pdf_reader = PdfFileReader(open(doc_name, "rb"))
    numPages = pdf_reader.getNumPages()
    if page_num > numPages:
        #TODO: Throw exception.
        print(f'This numbers have to be less than {numPages}')
        return
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
#endregion

@Gooey
def main():
    #region Arg parse
    parser = argparse.ArgumentParser(description='Pdf utilities')
    parser.add_argument('doc', help='PDF path')
    parser.add_argument('NumberPages', type=int, nargs='+',
                        help='''Number of pages to extract
    One page: extract from first to input page.
    Two pages: from firsto to second input page.''')

    args = vars(parser.parse_args())
    #endregion
    
    # Get length of the 'NumberPages' input.
    lenPages = len(args['NumberPages'])
        # print(f'Len : {lenPages}')
    # Substract 1 to 'NumberPages' to python array index.
    pages = [p-1 for p in args['NumberPages']]
        # print(pages)
    try:
        if pages[0] < 0:
            raise Exception('InputError','This numbers have to be greater equal than 1')
        if lenPages == 1:
            extract_page(args['doc'], 0, pages[0])
        if pages[0] > pages[1]:
            raise Exception('InputError','The first number have to be less equal than the second number.')
        elif lenPages == 2:
            extract_page(args['doc'], pages[0], pages[1])
        else:
            print('Ops sorry, This function will be available comming soon.')
    except:
        print(f'Unespected Error: {sys.exc_info()[1]}')

main()