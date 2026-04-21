import psycopg2

def get_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="eroxkha",
        password="Rerokha01"
    )
    return conn