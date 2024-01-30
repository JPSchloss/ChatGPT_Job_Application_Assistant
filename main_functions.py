from PyPDF2 import PdfReader
from bs4 import BeautifulSoup
import requests

from langchain.text_splitter import RecursiveCharacterTextSplitter

def split_text_documents(docs: list):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=20, separators=[" ", ",", "\n"])
    documents = text_splitter.split_documents(docs)
    return documents

def text_to_doc_splitter(text: str):
    spliiter = RecursiveCharacterTextSplitter(chunk_size = 10000, chunk_overlap = 0, length_function = len, add_start_index = True,)
    document = spliiter.create_documents([text])
    return document

def extract_text_from_url(url):
    html = requests.get(url).text
    soup = BeautifulSoup(html, features="html.parser")
    text = []
    for lines in soup.findAll('div', {'class': 'description__text'}):
        text.append(lines.get_text())
    
    lines = (line.strip() for line in text)
    text = '\n'.join(line for line in lines if line)
    
    document = text_to_doc_splitter(text)
    return document

def load_pdf(pdf):
    pdf_reader = PdfReader(pdf)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    
    document = text_to_doc_splitter(text)
    return document

