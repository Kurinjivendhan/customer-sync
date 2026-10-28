import os 

import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port = int(os.getenv("DB_PORT", "3306")),
        database = os.getenv("DB_NAME"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        connection_timeout=5,
    )


def save_customers(customers):
    if not customers:
        return 0

    connection = get_connection()

    try:
        cursor= connection.cursor()

        
        
        query = """
            INSERT INTO customers (external_id, name, email)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE
                name = VALUES(name),
                email = VALUES(email)
        """

        values = []

        for customer in customers:
            values.append((
                customer["id"],
                customer["name"],
                customer["email"],
            ))

        cursor.executemany(query, values)
        connection.commit()


        return len(customers)

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()
        connection.close()
