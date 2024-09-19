import os
import psycopg2


POSTGRES_USER = os.environ.get("POSTGRES_USER", "sf_user")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_USER", "sf_password")
POSTGRES_DB = os.environ.get("POSTGRES_USER", "semantic_find")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "localhost")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", 5434)


def setup_db():
    conn = psycopg2.connect(
        host=POSTGRES_HOST,
        port=POSTGRES_PORT,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        dbname=POSTGRES_DB,
    )
    cur = conn.cursor()
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    create_document_table = """
    CREATE TABLE IF NOT EXISTS document (
        id BIGSERIAL PRIMARY KEY, 
        title TEXT, 
        file_name TEXT, 
        author VARCHAR(255),
        byte_count BIGINT,
        page_count INT,
        type VARCHAR(255)
    );
    """
    cur.execute(create_document_table)

    create_paragraph_table = """
    CREATE TABLE IF NOT EXISTS paragraph (
    id BIGSERIAL PRIMARY KEY, 
    content TEXT
    );
    """
    cur.execute(create_paragraph_table)

    create_vector_embeddings = """
    CREATE TABLE IF NOT EXISTS vector_embedding (
        id BIGSERIAL PRIMARY KEY, 
        content TEXT, 
        embedding VECTOR(1024),
        page_number INT,
        start_byte BIGINT,
        paragraph_id INT REFERENCES paragraph(id),
        document_id INT REFERENCES document(id)
    );
    """
    cur.execute(create_vector_embeddings)
    cur.close()
    conn.commit()
    print("Database setup complete.")


if __name__ == "__main__":
    setup_db()
