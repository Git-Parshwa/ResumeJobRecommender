from pdfminer.high_level import extract_text
import spacy
from spacy.matcher import PhraseMatcher
import re

nlp=spacy.load("en_core_web_sm")

skills_list=[
    'python', 'java', 'c++', 'sql', 'machine learning', 'deep learning', 
    'nlp', 'data analysis', 'pandas', 'numpy', 'django', 'flask', 'excel',
    'react', 'node.js', 'aws', 'git', 'html', 'css'
]


def extract_text_from_pdf(file_path):
    return extract_text(file_path)

def extract_email(text):
    match = re.search(r'\S+@\S+', text)
    return match.group(0) if match else None

def extract_phone(text):
    match = re.search(r'\+?\d[\d\s\-]{8,15}\d', text)
    return match.group(0) if match else None

def extract_name(text):
    doc=nlp(text)
    for ent in doc.ents:
        if ent.label_=='PERSON':
            return ent.text
    return None

def extract_skills(text):
    text=text.lower()
    doc=nlp(text)

    matcher=PhraseMatcher(nlp.vocab,attr="LOWER")
    patterns=[nlp(skill) for skill in skills_list]
    matcher.add("SKILLS",patterns)

    matches=matcher(doc)
    found_skills=list(set([doc[start:end].text for _,start,end in matches]))

    return found_skills

def extract_resume_info(file_path):
    text=extract_text_from_pdf(file_path)
    name=extract_name(text)
    email=extract_email(text)
    phone=extract_phone(text)
    skills=extract_skills(text)

    return {
        "name":name,
        "email":email,
        "phone":phone,
        "skills":skills,
        "raw_text":text
    }