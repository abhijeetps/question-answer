import os
import shutil
import json

from app.config import *

from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

def read_doc(directory):
    file_loader = PyPDFDirectoryLoader(directory)
    documents = file_loader.load()
    return documents

def chunk_data(docs, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    doc = text_splitter.split_documents(docs)
    return doc

def save_file(file, path):
    file_location = f"{path}/{file.filename}"
    print(f"Saving file {file} at {file_location}.")
    with open(file_location, "wb+") as file_object:
        shutil.copyfileobj(file.file, file_object)
    print(f"Sucessfully saved file at {file_location}.")
    return file_location

def get_questions(question_file_location):
    questions_list = []
    questions = json.load(open(question_file_location))
    for question in questions:
        questions_list.append(question['content'])
    return questions_list

def make_directories():
    try:
        print("Creating required directories.")
        os.mkdir(DOCUMENTS_DIRECTORY_PATH)
        os.mkdir(JSON_DIRECTORY_PATH)
        print("Successfully created directories.")
    except OSError as error:
        print(f"Error occured while creating directory.", error)
