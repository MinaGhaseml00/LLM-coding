import os
import chromadb
from dotenv import load_dotenv
from openai import OpenAI
from chromadb.utils import embedding_functions

load_dotenv()
openai_key = os.getenv ("OPENAI_API_KEY")
openai_em_func = embedding_functions.OpenAIEmbeddingFunction(
    api_key= openai_key ,  model_name = "text_embedding_3_small"
)
