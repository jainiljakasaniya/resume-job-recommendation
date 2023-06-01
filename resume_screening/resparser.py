import re
# from resume_parser import resumeparse
import extract_skill

# import nltk
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('universal_tagset')
# nltk.download('maxent_ne_chunker')
# nltk.download('stopwords')
# nltk.download('wordnet')
# nltk.download('brown')
from tika import parser


def skill(resume_file):
    data = extract_skill.read_file(resume_file)
    resume = data['skills']
    skills = []
    skills.append(' '.join(word for word in resume))
    return skills

# def parser(resume_file):
#     data = resumeparse.read_file(resume_file)
#     return data

def convert_docx_to_txt(docx_file):
    text = parser.from_file(docx_file, service='text')['content']
    clean_text = re.sub(r'\n+', '\n', text)
    clean_text = clean_text.replace("\r", "\n").replace("\t", " ")  # Normalize text blob
    resume_lines = clean_text.splitlines()  # Split text blob into individual lines
    resume_lines = [re.sub('\s+', ' ', line.strip()) for line in resume_lines if line.strip()]  # Remove empty strings and whitespaces
    return resume_lines

def convert_pdf_to_txt(pdf_file):
    raw_text = parser.from_file(pdf_file, service='text')['content']
    full_string = re.sub(r'\n+', '\n', raw_text)
    full_string = full_string.replace("\r", "\n")
    full_string = full_string.replace("\t", " ")

    # Remove awkward LaTeX bullet characters
    full_string = re.sub(r"\uf0b7", " ", full_string)
    full_string = re.sub(r"\(cid:\d{0,2}\)", " ", full_string)
    full_string = re.sub(r'• ', " ", full_string)

    # Split text blob into individual lines
    resume_lines = full_string.splitlines(True)

    # Remove empty strings and whitespaces
    resume_lines = [re.sub('\s+', ' ', line.strip()) for line in resume_lines if line.strip()]
    return resume_lines