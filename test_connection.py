
import os
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

connection = None
cursor = None

try:
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "3306")),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        connection_timeout=5,
    )

    cursor = connection.cursor()
    cursor.execute("SELECT DATABASE(), CURRENT_USER()")

    result = cursor.fetchone()

    print("Connection successful!")
    print("Database:", result[0])
    print("User:", result[1])

except mysql.connector.Error as error:
    print("Connection failed:", error)

finally:
    if cursor is not None:
        cursor.close()

    if connection is not None and connection.is_connected():
        connection.close()
