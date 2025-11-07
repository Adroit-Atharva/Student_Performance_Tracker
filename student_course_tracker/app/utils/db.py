# app/utils/db.py

import psycopg2
from psycopg2 import sql, OperationalError

def connect_db():
    """
    Establishes and returns a connection to the PostgreSQL database.
    Update the credentials below to match your local setup.
    """
    try:
        conn = psycopg2.connect(
            dbname="student_tracker_db",
            user="atharva",
            password="Atharva123",
            host="localhost",
            port="5432"
        )
        print("✅ Database connection established.")
        return conn

    except OperationalError as e:
        print("❌ Error: Could not connect to the database.")
        print(e)
        exit(1)


def close_db(conn):
    """Closes the database connection."""
    if conn:
        conn.close()
        print("🔒 Database connection closed.")
