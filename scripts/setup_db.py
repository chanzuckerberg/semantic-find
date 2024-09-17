import os
import psycopg2


POSTGRES_USER=os.environ.get("POSTGRES_USER", "sf_user")
POSTGRES_PASSWORD=os.environ.get("POSTGRES_USER", "sf_password")
POSTGRES_DB=os.environ.get("POSTGRES_USER", "semantic_find")
POSTGRES_HOST=os.environ.get("POSTGRES_HOST", "localhost")
POSTGRES_PORT=os.environ.get("POSTGRES_PORT", 5434)

def setup_db():
    conn = psycopg2.connect(host=POSTGRES_HOST, port=POSTGRES_PORT, user=POSTGRES_USER, password=POSTGRES_PASSWORD, dbname=POSTGRES_DB)
    cur = conn.cursor()
    cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
    create_vector_embeddings = """
    CREATE TABLE IF NOT EXISTS vector_embeddings (
        id BIGSERIAL PRIMARY KEY, 
        content TEXT, 
        tokens INTEGER, 
        embedding VECTOR(1024)
    );
    """
    cur.execute(create_vector_embeddings)
    cur.close()
    conn.commit()
    print("Database setup complete.")

if __name__ == "__main__":
    setup_db()