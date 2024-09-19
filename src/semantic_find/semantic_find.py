import os
import psycopg2
import numpy as np
from pgvector.psycopg2 import register_vector
from FlagEmbedding import BGEM3FlagModel
from ngrams import NGramIterator
from parsers import get_data
from psycopg2.extensions import AsIs


POSTGRES_USER = os.environ.get("POSTGRES_USER", "sf_user")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_USER", "sf_password")
POSTGRES_DB = os.environ.get("POSTGRES_USER", "semantic_find")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", 5434)


"""Main module."""


def search(query: str) -> None:
    """Search for the given query."""
    print(f"Searching for {query}...")

    conn = psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        dbname=POSTGRES_DB,
    )
    register_vector(conn)
    cursor = conn.cursor()

    model = BGEM3FlagModel("BAAI/bge-m3", use_fp16=True)
    query_emb = model.encode(query)["dense_vecs"]

    cursor.execute(
        """
                   SELECT 
                   ve.content,
                   p.content,
                   d.title, 
                   d.file_name,
                   d.type,
                   embedding <=> %s::vector as distance,
                   ve.embedding
                   FROM vector_embedding ve
                   JOIN paragraph p ON p.id = ve.paragraph_id
                   JOIN document d ON d.id = ve.document_id
                   ORDER BY embedding <-> %s LIMIT 10""",
        (
            query_emb,
            query_emb,
        ),
    )
    results = cursor.fetchall()

    for index, result in enumerate(results):
        print("=====================================")
        print("Result: ", index + 1)
        print("ngram: ", result[0])
        print()
        print("paragraph: ", result[1])
        print()
        print("title: ", result[2])
        print("file_name: ", result[3])
        print("type: ", result[4])
        print("distance: ", result[5])
        print("=====================================")

    cursor.close()
    conn.commit()


def insert3(data_path: str = "./data/"):
    texts = get_data(data_path)
    paragraphs_seen = set()
    conn = psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        dbname=POSTGRES_DB,
    )
    register_vector(conn)
    cursor = conn.cursor()
    model = BGEM3FlagModel("BAAI/bge-m3", use_fp16=True)
    for document in texts:
        doc = document.__dict__()
        db_string = cursor.mogrify(
            "INSERT INTO document (%s) values %s RETURNING id",
            (AsIs(",".join(doc.keys())), tuple(doc.values())),
        )
        cursor.execute(db_string)
        conn.commit()
        document_id = cursor.fetchone()[0]

        ngrams = [
            (ngram, paragraph_index)
            for ngram, paragraph_index in NGramIterator(document.get_paragraphs())
        ]
        corpus_emb = model.encode(
            [ngram[0] for ngram in ngrams], batch_size=12, max_length=1024
        )
        for index, (ngram, paragraph_index) in enumerate(ngrams):
            if paragraph_index not in paragraphs_seen:
                cursor.execute(
                    "INSERT INTO paragraph (content) VALUES (%s) RETURNING id",
                    (document.paragraphs[paragraph_index].content,),
                )
                conn.commit()
                paragraph_id = cursor.fetchone()[0]
                paragraphs_seen.add(paragraph_index)

            cursor.execute(
                """
                INSERT INTO vector_embedding (content, embedding, page_number, start_byte, paragraph_id, document_id) 
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    ngram,
                    corpus_emb["dense_vecs"][index],
                    None,
                    None,
                    paragraph_id,
                    document_id,
                ),
            )
    cursor.close()
    conn.commit()
