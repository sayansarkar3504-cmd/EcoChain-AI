import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """
    Creates and returns a connection to the MySQL database.
    """
    try:
        connection = mysql.connector.connect(
            host=os.getenv("MYSQL_HOST", "localhost"),
            user=os.getenv("MYSQL_USER", "root"),
            password=os.getenv("MYSQL_PASSWORD", ""),
            database=os.getenv("MYSQL_DATABASE", "ecochain_db"),
            port=int(os.getenv("MYSQL_PORT", 3306))
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return None

def execute_query(query: str, params: tuple = None, fetch: bool = True):
    """
    Executes a SQL query safely.
    """
    conn = get_db_connection()
    if not conn:
        return None
    
    try:
        cursor = conn.cursor(dictionary=True)
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
            
        if fetch:
            result = cursor.fetchall()
            return result
        else:
            conn.commit()
            return cursor.rowcount
    except Error as e:
        print(f"Error executing query: {e}")
        return None
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()
