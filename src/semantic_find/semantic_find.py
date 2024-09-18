import os
import psycopg2
import numpy as np
from pgvector.psycopg2 import register_vector
from FlagEmbedding import BGEM3FlagModel
from pathlib import Path
import re



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

# This inheritence might not be a good idea but starting off with it
class DataParser:
    def __init__(self, data_path: str):
        self.data_path = data_path
    
    def parse(self):
        raise NotImplementedError


class TxtDataParser(DataParser):
    def parse(self) -> list[dict[str, str]]:
        with open(self.data_path, "r") as file:
            txt_data = file.read()
            paragraphs = re.split(r"\n\n+", txt_data)
        return [{"paragraph_number": index, "text": paragraph} for index, paragraph in enumerate(paragraphs)]


def get_data(data_path: str) -> dict[list[dict[str, str]]]:
    files = Path(data_path).glob("*")
    text_dicts = {}
    for file in files:
        file_name = file.name.rstrip(file.suffix)
        if file.suffix == ".txt":
            paragraph_list = TxtDataParser(file).parse()

        text_dicts[file_name] = paragraph_list
    return text_dicts

def insert3(data_path: str = "./data/"):
    text_dicts = get_data(data_path)


    conn = psycopg2.connect(host=POSTGRES_HOST, port=POSTGRES_PORT, user=POSTGRES_USER, password=POSTGRES_PASSWORD, dbname=POSTGRES_DB)
    register_vector(conn)

    cursor = conn.cursor()
    model = BGEM3FlagModel("BAAI/bge-m3", use_fp16=True)
    for text_name, paragraphs in text_dicts.items():
        text_only = [p["text"] for p in paragraphs]
        corpus_emb = model.encode(text_only, batch_size=12, max_length=1024)
        for index, paragraph in enumerate(paragraphs):
            cursor.execute("""
                INSERT INTO vector_embeddings (content, tokens, embedding) 
                VALUES (%s, %s, %s)
                """, 
                (paragraph["text"], len(paragraph["text"].split()), corpus_emb["dense_vecs"][index]) 
            )
    cursor.close()
    conn.commit()