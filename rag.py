from encodings import utf_8
import os
from urllib import response
import chromadb
from dotenv import load_dotenv
from openai import OpenAI
from chromadb.utils import embedding_functions

load_dotenv()
openai_key = os.getenv ("OPENAI_API_KEY")
openai_ef = embedding_functions.OpenAIEmbeddingFunction(
    api_key= openai_key ,  model_name = "text-embedding-3-small"
)
# load_dotenv()

# openai_key = os.getenv("OPENAI_API_KEY")

# openai_ef = embedding_functions.OpenAIEmbeddingFunction(
#     api_key=openai_key, model_name="text-embedding-3-small"
# )

chroma_client= chromadb.PersistentClient(path="chroma_persistent_storage")
collection_name= "document_qa_collection"
collection = chroma_client.get_or_create_collection(
    name=collection_name , embedding_function= openai_ef, metadata={"hnsw:M": 64}
)

def load_documents(doc_directory):
    documents= []
    for filename in os.listdir(doc_directory):
        print(filename)
        if filename.endswith(".txt"):
            file=open ( os.path.join (doc_directory,filename) , 'r' , encoding= "utf_8")
            documents.append({"id": filename , "text": file.read()})
    
    return documents



def chunking_text (text , chunck_size = 1000 , overlap =20):
    chunks=[]
    start = 0
    while start< len(text):
            end = start+chunck_size
            chunks.append (text[start:end])
            start = end - overlap 
    return chunks


def chunking_documents (documents):
    chunked_documents = []
    for doc in documents: 
        chunks = chunking_text (doc["text"])
        for i , chunk in enumerate(chunks):
            chunked_documents.append({"id": f"{doc['id']}_chunk{i+1}" , "text": chunk  })

    return chunked_documents


documents = load_documents("./news_articles")
chunked_documents =  chunking_documents (documents)

print ("documents count: " , len(documents))
print ("chunked documents count:" , len(chunked_documents))

client =  OpenAI(api_key= openai_key)

def generate_openai_embedding (text):
    response= client.embeddings.create(input="text" ,  model="text-embedding-3-small")
    embedding= response.data[0].embedding
    return embedding

for i, doc in enumerate(chunked_documents):
    doc["embedding"] = generate_openai_embedding(doc["text"])
    print ("embedding:" , i)

for doc in chunked_documents:
    collection.upsert(
        ids=[doc["id"]], documents=[doc["text"]], embeddings=[doc["embedding"]]
    )


def query_documents (question , n_results=2):                     
    results = collection.query(query_texts=question, n_results=n_results)
    relevant_chunks = [doc for sublist in results["documents"] for doc in sublist]
    return relevant_chunks


# Function to generate a response from OpenAI
def generate_response(question, relevant_chunks):
    context = "\n\n".join(relevant_chunks)
    prompt = (
        "You are an assistant for question-answering tasks. Use the following pieces of "
        "retrieved context to answer the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the answer concise."
        "\n\nContext:\n" + context + "\n\nQuestion:\n" + question
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": prompt,
            },
            {
                "role": "user",
                "content": question,
            },
        ],
    )

    answer = response.choices[0].message
    return answer


# Example query
# query_documents("tell me about AI replacing TV writers strike.")
# Example query and response generation
question = "tell me about ai replace writers"
question = "tell me about databricks"
relevant_chunks = query_documents(question)
answer = generate_response(question, relevant_chunks)

print(answer)

    
