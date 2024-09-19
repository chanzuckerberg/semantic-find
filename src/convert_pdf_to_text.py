# brew install poppler
# pip install pdf2image
# brew install tesseract
# pip install pytesseract

import pdf2image
import pytesseract
from pytesseract import Output, TesseractError

pdf_path = '<FILL_THIS_IN>'
print(f"converting {pdf_path} to images")
images = pdf2image.convert_from_path(pdf_path)

# pil_im = images[0] # assuming that we're interested in the first page only
for i, image in enumerate(images):
    # ocr_dict now holds all the OCR info including text and location on the image
    ocr_dict = pytesseract.image_to_data(image, lang='eng', output_type=Output.DICT)
    text = " ".join(ocr_dict['text'])

    print(f"Page {i+1}")
    print(text)
    # print(ocr_dict)
