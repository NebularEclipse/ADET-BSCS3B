import mysql.connector
from mysql.connector import Error

class DBManager:
    def __init__(self, config):
        """Initialize the DBManager with the given MySQL config."""
        self.config = config

    def connect(self, use_db=True):
        """Create a connection to the database. By default, it connects to the database specified in the config."""
        try:
            config_copy = self.config.copy()
            if not use_db:
                config_copy.pop('database', None)  # If no database exists yet, remove it from the config
            connection = mysql.connector.connect(**config_copy)
            return connection
        except Error as e:
            print(f"Error connecting to database: {e}")
            return None

    def create_database(self):
        """Create the database if it doesn't exist."""
        connection = self.connect(use_db=False)
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("CREATE DATABASE IF NOT EXISTS adet")
                print("Database created or already exists.")
            except Error as e:
                print(f"Error creating database: {e}")
            finally:
                cursor.close()
                connection.close()

    def create_users_table(self):
        """Create the users table if it doesn't exist."""
        connection = self.connect()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS adet_user (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        username VARCHAR(255) NOT NULL UNIQUE,
                        first_name VARCHAR(255),
                        middle_name VARCHAR(255),
                        last_name VARCHAR(255),
                        contact_number VARCHAR(20),
                        email VARCHAR(255) NOT NULL UNIQUE,
                        address TEXT,
                        password VARCHAR(255) NOT NULL
                    )
                """)
                print("Users table created or already exists.")
            except Error as e:
                print(f"Error creating users table: {e}")
            finally:
                cursor.close()
                connection.close()

    def create_user(self, username, first_name, middle_name, last_name, contact_number, email, address, password):
        """Insert a new user into the database."""
        query = """
            INSERT INTO adet_user (username, first_name, middle_name, last_name, contact_number, email, address, password)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        connection = self.connect()
        if connection:
            cursor = connection.cursor()
            try:
                cursor.execute(query, (username, first_name, middle_name, last_name, contact_number, email, address, password))
                connection.commit()
                print("User created successfully.")
            except Error as e:
                print(f"Error creating user: {e}")
            finally:
                cursor.close()
                connection.close()

    def get_user_by_username(self, username):
        """Fetch a user by their username."""
        query = "SELECT * FROM adet_user WHERE username = %s"
        connection = self.connect()
        if connection:
            cursor = connection.cursor(dictionary=True)
            try:
                cursor.execute(query, (username,))
                user = cursor.fetchone()
                return user
            except Error as e:
                print(f"Error fetching user: {e}")
            finally:
                cursor.close()
                connection.close()
        return None
