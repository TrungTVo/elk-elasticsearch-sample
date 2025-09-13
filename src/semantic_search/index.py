from requests import post
import json
from os import environ
from dotenv import load_dotenv
from elasticsearch import Elasticsearch
from elastic_config import MyElasticsearch

load_dotenv()
OPENAI_API_KEY = environ.get('OPENAI_API_KEY')

API_URL = "https://api.openai.com/v1/embeddings"
headers = {"Authorization": f"Bearer {OPENAI_API_KEY}"}

def embed_text(text: str):
    req_body = {
        "input": text,
        "model": "text-embedding-ada-002",
        "encoding_format": "float"
    }
    response = post(API_URL, headers=headers, json=req_body)
    response.raise_for_status()
    if response.status_code == 200:
        return response.json()["data"][0]["embedding"]
    return None




catalog: list[str] = [
    "Python is widely used for machine learning and artificial intelligence projects.",
    "JavaScript powers interactive websites and front-end applications.",
    "Mount Fuji is a famous symbol of Japan and a popular hiking destination.",
    "The Great Wall of China is one of the most impressive architectural feats in history.",
    "The Amazon rainforest produces a significant portion of the world’s oxygen supply.",
    "Coffee and tea are the two most consumed beverages in the world.",
    "Shakespeare’s plays are considered classics of English literature.",
    "The Hubble Space Telescope has captured stunning images of distant galaxies.",
    "Soccer is played and followed passionately in almost every country.",
    "Basketball originated in the United States and has grown into a global sport."
]

es: MyElasticsearch = MyElasticsearch()
INDEX_NAME: str = "semantic_index"
es.create_index(index_name=INDEX_NAME, mapping={
    "mappings": {
        "properties": {
            "text": {"type": "text"},
            "embedding": {
                "type": "dense_vector",
                "dims": 1536  # must match embedding size
            }
        }
    }
})

def embed_catalog():
    for sentence in catalog:
        embedding = embed_text(sentence)
        document = {
            "text": sentence,
            "embedding": embedding
        }
        if embedding is not None:
            es.insert_document(index_name=INDEX_NAME, document=document)


# Embed sample catalog
# embed_catalog()

# Search query
query = "Which are famous landmarks to visit in Asia?"

def sample_search(query: str):
    query_embedding = embed_text(query)

    # Example semantic search
    knn = {
        "field": "embedding",               # field storing vectors
        "query_vector": query_embedding,
        "k": 3,                             # top-k results
        "num_candidates": 100               # candidate pool for efficiency
    }
    response = es.semantic_search(index_name=INDEX_NAME, knn=knn, source=["text"])
    print("Top 3 most similar sentences:")
    print(json.dumps(response.body, indent=4))


sample_search(query=query)

# es.delete_index(index_name=INDEX_NAME)