import mysql.connector
def get_db_connection():
    try:
        # 1. Establish the connection
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="ksk123", # Change this to your actual password
            database="timetable_db" # Change this to your DB name
        )

        if connection.is_connected():
            print("--- Connection Successful ---")
            
            # 2. Create a cursor to execute commands
            cursor = connection.cursor()
            
            # 3. Test: List all tables in your database
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
            
            print(f"Tables found in database: {tables}")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        # 4. Always close the connection when done
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed")
    return get_db_connection