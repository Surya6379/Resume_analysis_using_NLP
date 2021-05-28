import spacy
import sys, fitz

model = spacy.load('resume_model')

def pdf_text(path):
    fname = path
    doc = fitz.open(fname)
    text = ""
    for page in doc:
        text = text + str(page.getText())

    tx = " ".join(text.split('\n'))
    return tx

def nlp1(text):
    docs = model(text)
    output = {}
    for ents in docs.ents:
        if str(ents.label_) in output.keys():
            output[str(ents.label_)].append(ents.text)
        else:
            output[str(ents.label_)] = [ents.text]  
    del output['Name'] 
    return output
            
