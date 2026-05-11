import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

def db_connection():
    return mysql.connector.connect(
        host = os.getenv('HOST'),
        user = os.getenv('USER'),
        password = os.getenv('PASSWORD'),
        database = os.getenv('DATABASE')
    )

def get_all_files(search_query=None):
    conn = db_connection()
    cursor = conn.cursor(dictionary=True)
    
    if search_query:
        query = "SELECT * FROM gallery WHERE filename LIKE %s ORDER BY upload_time DESC"
        cursor.execute(query, (f"%{search_query}%",))
    else:
        query = "SELECT * FROM gallery ORDER BY upload_time DESC"
        cursor.execute(query)
        
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result