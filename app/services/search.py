import os
import pinecone
from app.config import *

from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores.pinecone import Pinecone

def get_vector_search_index(documents):
    embeddings = embeddings = OpenAIEmbeddings(api_key=os.environ['OPENAI_API_KEY'])
    pinecone.init(
        api_key=PINECONE_API_KEY,
        environment=PINECONE_ENVIRONMENT,
    )
    index_name=PINECONE_INDEX
    index = Pinecone.from_documents(documents=documents, embedding=embeddings, index_name=index_name)
    return index

def retrieve_query(documents, query, k=4):
    index = get_vector_search_index(documents=documents)
    matching_results = index.similarity_search(query=query, k=k)
    return matching_results
