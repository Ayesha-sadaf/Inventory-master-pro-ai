# from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma 
import os
from langchain_nomic import NomicEmbeddings
from dotenv import load_dotenv

load_dotenv()
if not os.environ.get("NOMIC_API_KEY"):
    os.environ["NOMIC_API_KEY"] = os.getenv("NOMIC_API_KEY")



def vector_store_generatrion():
    #Loading the embedding model 
    print("LOADING MODEL EMBEDDING")

    embedding_model = NomicEmbeddings(
    model="nomic-embed-text-v1.5",
    dimensionality=384
    )
    
    print("MODEL EMBEDDING LOADED")
        

    PERSIST_DIR = "data/chroma_db"

    # Check if DB already exists
    if os.path.exists(PERSIST_DIR) and os.listdir(PERSIST_DIR):
        
        #creating chroma client
        print(" Loading existing vector store...")
        vector_store = Chroma(
            persist_directory=PERSIST_DIR,
            embedding_function=embedding_model
        )      
    else:
        print("Creating new vector store...")
        from processed_test import docs
        vector_store = Chroma.from_documents(
            docs,
            embedding_model,
            persist_directory=PERSIST_DIR
        )      
        
    return vector_store
        
vector_store = vector_store_generatrion()



