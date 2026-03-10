import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import logging
from langchain_chroma import Chroma
from langchain.embeddings import OpenAIEmbeddings,HuggingFaceEmbeddings
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser
from operator import itemgetter
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.text_splitter import (CharacterTextSplitter,RecursiveCharacterTextSplitter,NLTKTextSplitter,TokenTextSplitter,MarkdownTextSplitter)
from langchain_openai import ChatOpenAI
from langchain.document_loaders import TextLoader
from app_config.open_ai_cred import OPENAI_KEY 
from app_config.open_ai_cred import model_name , embed_model

#import openai


os.environ['OPENAI_API_KEY'] = OPENAI_KEY

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
current_dir = os.path.dirname(os.path.abspath(__file__))
data_folder = os.path.join(current_dir, '..', 'all_ubuntu_data')
data_folder = os.path.abspath(data_folder)

#data_folder = 'all_ubuntu_data'
class VectorStore:
    def __init__(self,model_name,embed_model_name):
        self.model_name = model_name
        self.embed_model_name = embed_model_name

    def document_splitter(self,md_path):

        # Load MD
        try:
            loader = TextLoader(md_path)
            documents = loader.load()
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
            chunked_docs = text_splitter.split_documents(documents)
            logging.info("...Splitting Done")  
            return chunked_docs
        except Exception as e:
            logging.info("...error while splitting the document....")    

    def document_indexer(self,chunked_docs): 
        try:   
            openai_embed_model = OpenAIEmbeddings(model=self.embed_model_name)
            chroma_db = Chroma.from_documents(documents=chunked_docs,
                                    collection_name='sample_proj',
                                    embedding=openai_embed_model,
                                    collection_metadata={"hnsw:space": "cosine"},
                                    persist_directory="./proj_db")

            logging.info(".....Indexing done.....")
        except Exception as e:
            logging.info("...error while Indexing ....")                              

    def vectord_db_loader(self):
        try:
            openai_embed_model = OpenAIEmbeddings(model=self.embed_model_name)
            chroma_db = Chroma(persist_directory="./proj_db",
                    collection_name='sample_proj',
                    embedding_function=openai_embed_model)
            
            logging.info(".....Loading vectord db....")
            return chroma_db           
        except Exception as e:
            logging.info("...can't load Vector db ....")

# vector_store = VectorStore(model_name , embed_model)


# md_file = os.listdir(data_folder)
# chunked_all_data = []
# for val in md_file :
#     md_path  = os.path.join(data_folder,val)
#     res = vector_store.document_splitter(md_path)
#     chunked_all_data.extend(res)
# logging.info("total no of document chunk in ubuntu docs "+str(len(chunked_all_data)))
# vector_store.document_indexer(chunked_all_data)  

# chroma_db = vector_store.vectord_db_loader()
# count = chroma_db._collection.get(limit=5)
# logging.info("Total chunk count in chroma "+str(count))