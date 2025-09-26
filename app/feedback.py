import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text


load_dotenv()

DB_URL = os.getenv("DB_URL")
if not DB_URL:
    raise ValueError("DB_URL not set in .env")

engine = create_engine(DB_URL, future=True)

def init_feedback_table():
    with engine.begin() as conn:
        conn.execute(text("""
        CREATE TABLE IF NOT EXISTS feedback(
          id SERIAL PRIMARY KEY,
          hash_id TEXT NOT NULL,
          question TEXT NOT NULL,
          answer TEXT NOT NULL,
          label INT NOT NULL,
          comment TEXT,
          created_at TIMESTAMP DEFAULT NOW()
        );
        """))

def add_feedback(hash_id, question, answer, label, comment):
    with engine.begin() as conn:
        conn.execute(
            text("""
            INSERT INTO feedback(hash_id,question,answer,label,comment)
            VALUES (:h,:q,:a,:l,:c)
            """),
            {"h": hash_id, "q": question, "a": answer, "l": label, "c": comment}
        )
