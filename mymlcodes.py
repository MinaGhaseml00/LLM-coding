# 1.chat completetion with openai api
from openai import OpenAI
from sk import my_key
client = OpenAI( api_key = my_key, )

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": "listen to your",
        }
    ],
    model="gpt-3.5-turbo",
    max_tokens=2,
    n=1,
    temperature=1,
)

for i in range(len(chat_completion.choices)):
    print (chat_completion.choices[i].message.content);


# 2. embedding vector generation with openai API
from openai import OpenAI
from sk import my_key
client = OpenAI(api_key = my_key)

myembedding = client.embeddings.create(
  model="text-embedding-ada-002",
  input="The food was delicious and the waiter...",
  encoding_format="float"
)

print(myembedding)