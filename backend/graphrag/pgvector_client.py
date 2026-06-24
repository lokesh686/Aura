import os
import psycopg2
from psycopg2.extras import execute_values
import numpy as np

class PgVectorClient:
    def __init__(self):
        self.conn_str = os.getenv(
            "DATABASE_URL", 
            "postgresql://aura_user:aura_password@localhost:5432/aura_db"
        )
        self.conn = psycopg2.connect(self.conn_str)
        self.setup_db()

    def setup_db(self):
        with self.conn.cursor() as cur:
            # Enable the pgvector extension
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            # Create the documents table for storing compliance text and vectors
            cur.execute("""
                CREATE TABLE IF NOT EXISTS compliance_documents (
                    id SERIAL PRIMARY KEY,
                    policy_id VARCHAR(100),
                    content TEXT,
                    embedding vector(1536) -- Using 1536 dimensions for OpenAI/standard embeddings
                );
            """)
            self.conn.commit()

    def insert_document(self, policy_id: str, content: str, embedding: list[float]):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO compliance_documents (policy_id, content, embedding)
                VALUES (%s, %s, %s)
            """, (policy_id, content, str(embedding)))
            self.conn.commit()

    def search_similar_documents(self, query_embedding: list[float], limit: int = 5):
        with self.conn.cursor() as cur:
            # Using the <-> operator for L2 distance (euclidean) in pgvector
            cur.execute("""
                SELECT policy_id, content 
                FROM compliance_documents 
                ORDER BY embedding <-> %s 
                LIMIT %s
            """, (str(query_embedding), limit))
            
            results = cur.fetchall()
            return [{"policy_id": r[0], "content": r[1]} for r in results]

    def close(self):
        self.conn.close()

# Singleton instance for the app
pgvector_client = PgVectorClient()
