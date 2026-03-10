import sys
import os
import uvicorn 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from fastapi import FastAPI
from document_processing.doc_qa import question_answer_gen

app = FastAPI(title="QA Bot API")

@app.get("/qa")
def qa_endpoint(question: str):
    try:
      answer = question_answer_gen(question)
      if answer is not None:
        return {"answer": answer}
      else:
        return {"answer": 'Error while generating the answer'}    
    except Exception as e:
      return {"answer": 'Error while generating the answer'}  

if __name__ == "__main__":
    uvicorn.run("document_processing.endpoint_api_swagger:app", host="0.0.0.0", port=8000, reload=True)    