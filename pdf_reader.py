#pip install pdfminer.six
import io

from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


def convert_pdf_to_txt(path):
    '''Convert pdf content from a file path to text

    :path the file path
    '''
    rsrcmgr = PDFResourceManager()
    codec = 'utf-8'
    laparams = LAParams()

    with io.StringIO() as retstr:
        with TextConverter(rsrcmgr, retstr, codec=codec,
                           laparams=laparams) as device:
            with open(path, 'rb') as fp:
                interpreter = PDFPageInterpreter(rsrcmgr, device)
                password = ""
                maxpages = 0
                caching = True
                pagenos = set()

                for page in PDFPage.get_pages(fp,
                                              pagenos,
                                              maxpages=maxpages,
                                              password=password,
                                              caching=caching,
                                              check_extractable=True):
                    interpreter.process_page(page)

                return retstr.getvalue()


if __name__ == "__main__":
    print(convert_pdf_to_txt('test.pdf'))


import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import tempfile
import pdf2image

pytesseract.pytesseract.tesseract_cmd = r'path/to/tesseract'  # Update this path

def ocr_pdf(pdf_path):
    # Convert PDF pages to images
    pages = pdf2image.convert_from_path(pdf_path)
    
    text = ""
    for page in pages:
        # Save the image of the page in temp file
        with tempfile.NamedTemporaryFile(delete=True) as temp:
            page.save(temp.name, 'JPEG')
            # Use pytesseract to do OCR on the image file
            page_text = pytesseract.image_to_string(Image.open(temp.name))
            text += page_text + "\n"
    return text

pdf_path = 'path/to/your/pdf.pdf'
extracted_text = ocr_pdf(pdf_path)
print(extracted_text)

