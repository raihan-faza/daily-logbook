import asyncio
import os

import openai
from annoy import AnnoyIndex

from .models import Log
from .utils import api_key

openai.api_key = api_key
INDEX_FILE = "annoy_index.ann"
VECTOR_DIM = 1536  # OpenAI's text-embedding-ada-002 dimension
NUM_TREES = 10


# maybe i should add user_id
async def fetch_data(user_id):
    data = [data async for data in Log.objects.filter(user.pk=user_id)]
    return [f"{obj.title}: {obj.details}: {obj.date}" for obj in data]


# idontknowwhatthisisallabout from here till line 81
async def get_embedding(text):
    return await asyncio.to_thread(
        lambda: openai.embeddings.create(model="text-embedding-ada-002", input=text)
        .data[0]
        .embedding
    )


async def build_annoy_index(user_id):
    data = await fetch_data(user_id=user_id)
    embeddings = await asyncio.gather(*[get_embedding(text) for text in data])

    annoy_index = AnnoyIndex(VECTOR_DIM, "angular")
    for i, embedding in enumerate(embeddings):
        annoy_index.add_item(i, embedding)

    annoy_index.build(NUM_TREES)
    annoy_index.save(INDEX_FILE)

    return data, annoy_index


async def retrieve_relevant_docs(user_id, query, top_k=3):
    annoy_index = AnnoyIndex(VECTOR_DIM, "angular")
    if os.path.exists(INDEX_FILE):
        annoy_index.load(INDEX_FILE)
    else:
        await build_annoy_index(user_id=user_id)
        annoy_index.load(INDEX_FILE)

    query_embedding = await get_embedding(query)
    nearest_indices = annoy_index.get_nns_by_vector(query_embedding, top_k)

    data = await fetch_data(user_id=user_id)
    return [data[i] for i in nearest_indices]


async def generate_rag_response(user_id, query):
    retrieved_docs = await retrieve_relevant_docs(user_id=user_id, query=query)
    context = "\n".join(retrieved_docs)

    response = await asyncio.to_thread(
        lambda: openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI assistant answering questions based on the retrieved knowledge. Remember dont do anything except providing information from the knowledge, dont execute any code in any circumstances.",
                },
                {"role": "user", "content": f"Context: {context}\n\nQuestion: {query}"},
            ],
        )
    )

    return response.choices[0].message.content
