from app.services.search import *
from app.utils.utils import *
from langchain_community.chat_models import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain

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
