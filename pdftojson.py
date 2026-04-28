import pdfplumber
import re
import json

def ex_text_pdf(pdf_path):
    text = ''
    with pdfplumber.open(pdf_ppath) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + '\n'
    return text
