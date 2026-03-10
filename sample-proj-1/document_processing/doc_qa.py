import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from langchain_chroma import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import (CharacterTextSplitter,RecursiveCharacterTextSplitter,NLTKTextSplitter,TokenTextSplitter,MarkdownTextSplitter)
from langchain_openai import ChatOpenAI
from app_config.open_ai_cred import OPENAI_KEY 
from app_config.open_ai_cred import model_name , embed_model
from document_processing.doc_indexer import VectorStore
from document_processing.proj_prompt import qa_prompt
from langchain_core.messages import HumanMessage
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter
import os 


os.environ['OPENAI_API_KEY'] = OPENAI_KEY

vector_store = VectorStore(model_name,embed_model)
chroma_db = vector_store.vectord_db_loader()

def format_docs(docs):
    try:
        return "\n\n".join(doc.page_content for doc in docs)
    except Exception as e:
        logging.info("Formatting function ggeting failed")    


def retriever_call():
    try:
        similarity_threshold_retriever = chroma_db.as_retriever(search_type="similarity_score_threshold",
                                                            search_kwargs={"k": 3,
                                                                        "score_threshold": 0.3})
        final_retriever = similarity_threshold_retriever
        return final_retriever
    except Exception as e:
        logging.info("error in retrieval")     

def question_answer_gen(question):
    try:
        chatgpt = ChatOpenAI(model_name=model_name,temperature=0)
        final_retriever = retriever_call()
        relevant_docs = final_retriever.get_relevant_documents(question)
        print(relevant_docs)
        qa_rag_chain = (
        {
            "context": (itemgetter('context')
                            |
                        RunnableLambda(format_docs)),
            "question": itemgetter('question')
        }
        |
        qa_prompt
        |
        chatgpt
        |
        StrOutputParser()
    )
        result = qa_rag_chain.invoke({"question": question, "context": relevant_docs})
        print(result)
        return result 
    except Exception as e:
        logging.info("error while generating the answer")
        return None


# res = question_answer_gen("define model assertion")
# print(res)


  


  