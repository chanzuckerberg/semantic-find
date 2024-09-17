import os
import psycopg2
import numpy as np
from pgvector.psycopg2 import register_vector



POSTGRES_USER=os.environ.get("POSTGRES_USER", "sf_user")
POSTGRES_PASSWORD=os.environ.get("POSTGRES_USER", "sf_password")
POSTGRES_DB=os.environ.get("POSTGRES_USER", "semantic_find")
POSTGRES_HOST=os.environ.get("POSTGRES_HOST", "localhost")
POSTGRES_PORT=os.environ.get("POSTGRES_PORT", 5434)


"""Main module."""
def search(query: str) -> None:
    """Search for the given query."""
    print(f"Searching for {query}...")


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
    