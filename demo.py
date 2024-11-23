




# import chromadb
# chroma_client = chromadb.Client()
# collection_name = "test_collection"
# collection = chroma_client.get_or_create_collection(collection_name)
# documents = [
#   {"id":"doc1" , "text": "hello, world!"  },
#   {"id":"doc2" , "text": "how are you today?"  },
#   {"id":"doc3" , "text": "goodbye, see you later!"  }
# ]

# for doc in documents :
#   collection.upsert(ids=doc["id"] ,  documents = [doc["text"]])

# query = "hello world!"

# results =  collection.query(query_texts=[query], n_results=3 )
# print(results)

# from openai import OpenAI
# from sk import my_key
# client = OpenAI(api_key = my_key)

# myembedding = client.embeddings.create(
#   model="text-embedding-ada-002",
#   input="The food was delicious and the waiter...",
#   encoding_format="float"
# )

# print(myembedding)


# import os
# from dotenv import load_dotenv
# import chromadb
# from openai import OpenAI
# from sk import my_key
# from chromadb.utils import embedding_functions

# load_dotenv()
# openai_key =os.getenv("OPENAI_API_KEY")


# client = OpenAI( api_key = my_key, )

# chat_completion = client.chat.completions.create(
#     messages=[
#         {
#             "role": "user",
#             "content": "listen to your",
#         }
#     ],
#     model="gpt-3.5-turbo",
#     max_tokens=2,
#     n=1,
#     temperature=1,
# )

# for i in range(len(chat_completion.choices)):
#     print (chat_completion.choices[i].message.content);
