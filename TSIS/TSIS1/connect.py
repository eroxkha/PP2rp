# connect.py
import psycopg2
from config import config

def get_connection():
    try:
        params = config()
        conn = psycopg2.connect(**params)
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(f"Ошибка при подключении: {error}")
        return None

if __name__ == '__main__':
    c = get_connection()
    if c:
        print("Связь с базой установлена успешно!")
        c.close()