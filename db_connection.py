import db_details
import psycopg2

def connect_to_db():
    try:
        connection = psycopg2.connect(
            dbname=db_details.db_name,
            user=db_details.db_user,
            password=db_details.db_password,
            host=db_details.db_host,
            port=db_details.db_port,
        )
        print("Connection to database established successfully.")
        return connection
    except Exception as error:
        print(f"Error connecting to database: {error}")
        return None