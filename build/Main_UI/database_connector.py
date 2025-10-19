#database_connector.py
import mysql.connector

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",        # change if you set another MySQL user
        password="",        # fill in if you set a password in XAMPPS
        database="barangay_eservice",
    )
if __name__ == "__main__":
    conn = get_connection()
    if conn.is_connected():
        print("✅ Connected!")
    conn.close()
