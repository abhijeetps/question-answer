import os
import pinecone
import json
import shutil

from fastapi import FastAPI, UploadFile
from fastapi.exceptions import HTTPException

from langchain.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.pinecone import Pinecone

from langchain_community.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
DOCUMENTS_DIRECTORY_PATH = "documents/"
JSON_DIRECTORY_PATH = "jsons/"

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

def get_vector_search_index(documents):
    embeddings = embeddings = OpenAIEmbeddings(api_key=os.environ['OPENAI_API_KEY'])
    pinecone.init(
        api_key=os.environ['PINECONE_API_KEY'],
        environment=os.environ['PINECONE_ENVIRONMENT'],
    )
    index_name=os.environ['PINECONE_INDEX']
    index = Pinecone.from_documents(documents=documents, embedding=embeddings, index_name=index_name)
    return index

def retrieve_query(documents, query, k=4):
    index = get_vector_search_index(documents=documents)
    matching_results = index.similarity_search(query=query, k=k)
    return matching_results

def get_llm(model_name="gpt-3.5-turbo",temperature=0.5):
    llm = ChatOpenAI(
        model_name=model_name,
        temperature=temperature,
    )
    return llm

def get_chain():
    llm = get_llm()
    chain = load_qa_chain(llm=llm, chain_type="stuff")
    return chain

def retrieve_answers(documents, query):
    doc_search = retrieve_query(documents, query=query)
    chain = get_chain()
    response = chain.run(input_documents=doc_search, question=query)
    return response

def find_answer_to_query(query):
    docs = read_doc('documents/')
    documents = chunk_data(docs=docs)
    answer = retrieve_answers(documents, query=query)
    return answer

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

app = FastAPI()

@app.post("/qa")
async def upload_file(question: UploadFile, doc: UploadFile):
    if question.content_type != "application/json" or doc.content_type != "application/pdf":
        if question.content_type != "application/json" and doc.content_type != "application/pdf":
            raise HTTPException(400, detail="Question should be a JSON and Doc should be a PDF.")
        elif question.content_type != "application/json":
            raise HTTPException(400, detail="Question should be a JSON.")
        elif question.content_type != "application/pdf":
            raise HTTPException(400, detail="Doc should be a PDF.")
    else:
        result = {}
        make_directories()
        question_file_location = save_file(file=question, path=JSON_DIRECTORY_PATH)
        save_file(file=doc, path=DOCUMENTS_DIRECTORY_PATH)
        questions_list = get_questions(question_file_location)
        for question in questions_list:
            print(f"Finding answer for: {question}")
            answer = find_answer_to_query(query=question)
            result[question] = answer
            print("Answer generated successfully.")
        return result


if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
