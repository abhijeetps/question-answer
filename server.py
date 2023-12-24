from app.config import *
from app.utils.utils import *
from app.services.answer import *
from app.services.search import *

from fastapi import FastAPI, UploadFile
from fastapi.exceptions import HTTPException

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
