import fitz  # PyMuPDF
import spacy
import re
import pandas as pd

# Charger le modèle NER spaCy
nlp = spacy.load("C:/Users/pc/OneDrive/Desktop/cours master IA/S2/NLP/projet/CVproject-20250518T220055Z-1-001/CVproject/model/output/model-best")

REQUIRED_LABELS = [
    "NAME", "EMAIL ADDRESS", "LINKEDIN LINK", "SKILLS", "CERTIFICATION",
    "COLLEGE NAME", "DEGREE", "UNIVERSITY", "YEAR OF GRADUATION",
    "COMPANIES WORKED AT", "WORKED AS", "YEARS OF EXPERIENCE",
    "LOCATION", "LANGUAGE", "AWARDS"
]

def extract_text_from_pdf(pdf_file):
    text = ""
    with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_entities(text: str, nlp_model) -> dict:
    doc = nlp_model(text)
    entities = {}

    for ent in doc.ents:
        if ent.label_ not in entities:
            entities[ent.label_] = []
        entities[ent.label_].append(ent.text.strip())

    if "NAME" not in entities or not entities["NAME"]:
        possible_name = re.findall(r'\b[A-Z][A-Z]+\s+[A-Z][A-Z]+\b', text[-300:])
        if possible_name:
            entities["NAME"] = [possible_name[0]]
    return entities

def convert_to_row(entities: dict) -> dict:
    row = {}
    for label in REQUIRED_LABELS:
        values = entities.get(label, [])
        row[label] = ", ".join(set(values)) if values else ""
    return row
