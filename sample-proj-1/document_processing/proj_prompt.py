import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app_config.open_ai_cred import *
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter
from langchain.docstore.document import Document
from langchain_openai import ChatOpenAI
from app_config.open_ai_cred import OPENAI_KEY 
from app_config.open_ai_cred import model_name , embed_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda
from langchain_core.output_parsers import StrOutputParser
from langchain.chains import create_history_aware_retriever
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
import os 
os.environ['OPENAI_API_KEY'] = OPENAI_KEY




qa_system_prompt = """You are an assistant for question-answering tasks.
            Use the following pieces of retrieved context to answer the question.
            If no context is present or if you don't know the answer, just say that you don't know the answer.
            Do not make up the answer unless it is there in the provided context.
            Give a detailed answer and to the point answer with regard to the question.

            Question:
            {question}

            Context:
            {context}

            Answer:
         """
qa_prompt = ChatPromptTemplate.from_template(qa_system_prompt)


