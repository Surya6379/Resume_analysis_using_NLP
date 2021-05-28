from __future__ import unicode_literals, print_function
 
from tkinter.ttk import *
from tkinter.filedialog import asksaveasfile 
from tkinter.filedialog import askopenfile 


import pytesseract
import spacy
import plac
import random

from pathlib import Path
from tqdm import tqdm
import fileinput
from pdf2image import convert_from_path 
import os 
from PIL import Image  
import csv
import sys 
import pickle
import fileinput
import docx
from docx import Document
from docx2pdf import convert

def ocr(path):
    PDF_file = path
    print(PDF_file)
    pages = convert_from_path(PDF_file, 500) 
    image_counter = 1
    for page in pages: 
        filename = "page_"+str(image_counter)+".jpg"
        page.save(filename, 'JPEG') 
        image_counter = image_counter + 1
    filelimit = image_counter-1
    outfile = "out_text.txt"
    f = open(outfile, "a") 
    output_text = ""
    for i in range(1, filelimit + 1): 
        filename = "page_"+str(i)+".jpg"
#         text = str(((pytesseract.image_to_string(Image.open(filename))))) 
        text = str(((pytesseract.image_to_string(filename)))) 
        text = text.replace('-\n', '')     
        output_text = output_text+text
        f.write(text) 
    new_text = ""
    for i in range(len(output_text)):
        if output_text[i] == '\n' and output_text[i+1] != '\n':
                new_text = new_text + " "
        else:
            new_text = new_text + output_text[i]
    f.close() 
    return output_text
def nlp(text):
    nlp = spacy.load('en_core_web_sm')
    docs = nlp(text)
    output = {}
    for ents in docs.ents:
        if str(ents.label_) in output.keys():
            output[str(ents.label_)].append(ents.text)
        else:
            output[str(ents.label_)] = [ents.text]   
    return output

    