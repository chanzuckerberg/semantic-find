import os
import psycopg2
import numpy as np
from pgvector.psycopg2 import register_vector
from FlagEmbedding import BGEM3FlagModel



POSTGRES_USER=os.environ.get("POSTGRES_USER", "sf_user")
POSTGRES_PASSWORD=os.environ.get("POSTGRES_USER", "sf_password")
POSTGRES_DB=os.environ.get("POSTGRES_USER", "semantic_find")
POSTGRES_HOST=os.environ.get("POSTGRES_HOST", "localhost")
POSTGRES_PORT=os.environ.get("POSTGRES_PORT", 5434)


"""Main module."""
def search(query: str) -> None:
    """Search for the given query."""
    print(f"Searching for {query}...")

    conn = psycopg2.connect(host=POSTGRES_HOST, port=POSTGRES_PORT, user=POSTGRES_USER, password=POSTGRES_PASSWORD, dbname=POSTGRES_DB)
    register_vector(conn)
    cursor = conn.cursor()

    model = BGEM3FlagModel("BAAI/bge-m3", use_fp16=True)
    query_emb = model.encode(query)['dense_vecs']

    cursor.execute('SELECT * FROM vector_embeddings ORDER BY embedding <-> %s LIMIT 2', (query_emb,))
    results = cursor.fetchall()
    for result in results:
        print(result)

    cursor.close()
    conn.commit()


def insert():
    conn = psycopg2.connect(host=POSTGRES_HOST, port=POSTGRES_PORT, user=POSTGRES_USER, password=POSTGRES_PASSWORD, dbname=POSTGRES_DB)
    register_vector(conn)

    cursor = conn.cursor()
    test_embedding = np.random.rand(1024)
    cursor.execute("""
        INSERT INTO vector_embeddings (content, tokens, embedding) 
                   VALUES (%s, %s, %s)
                   """, 
                   ("test", 1, test_embedding)
    )
    cursor.close()
    conn.commit()
    

def insert2():
    conn = psycopg2.connect(host=POSTGRES_HOST, port=POSTGRES_PORT, user=POSTGRES_USER, password=POSTGRES_PASSWORD, dbname=POSTGRES_DB)
    register_vector(conn)

    cursor = conn.cursor()
    model = BGEM3FlagModel("BAAI/bge-m3", use_fp16=True)
    corpus = [
        "Unlike tomato plants, the potato's most caloric edible component grows under ground, in the soil.",
        "Sometimes, sentences can even contain discussion of technology, like computers."
    ]
    corpus_emb = model.encode(corpus, batch_size=12, max_length=1024)['dense_vecs']
    for index, sentence in enumerate(corpus):
        cursor.execute("""
            INSERT INTO vector_embeddings (content, tokens, embedding) 
            VALUES (%s, %s, %s)
            """, 
            (sentence, len(sentence.split()), corpus_emb[index]) 
        )
    cursor.close()
    conn.commit()