import psycopg2
from psycopg2 import sql

class Database:
    def __init__(self, dbname: str, user: str, password: str, host: str = "localhost", port: str = "5432"):
        """
        Initialize the database connection parameters.
        
        :param dbname: Name of the database.
        :param user: Database user name.
        :param password: Password for the database user.
        :param host: Database host (default is "localhost").
        :param port: Database port (default is "5432").
        """
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.connection = None
        self.cursor = None

    def connect(self):
        """Connect to the PostgreSQL database."""
        try:
            print("Connecting to the database...")
            self.connection = psycopg2.connect(
                dbname=self.dbname,
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port
            )
            self.cursor = self.connection.cursor()
            print(f"Successfully connected to the {self.dbname} database at {self.host}:{self.port}")
        except Exception as e:
            print(f"Error connecting to the database: {e}")
            raise

    def create_table_if_not_exists(self):
        """Creates the model_results table if it does not exist."""
        create_table_query = """
        CREATE TABLE IF NOT EXISTS model_results (
            id SERIAL PRIMARY KEY,
            accuracy FLOAT,
            loss FLOAT,
            model_name VARCHAR(255)
        );
        """
        try:
            print("Ensuring table 'model_results' exists...")
            self.cursor.execute(create_table_query)
            self.connection.commit()
            print("Table 'model_results' is ready.")
        except Exception as e:
            print(f"Error creating table: {e}")
            self.connection.rollback()

    def execute_query(self, query: str, params: tuple = None):
        """
        Execute a given SQL query and commit changes to the database.
        
        :param query: The SQL query to execute.
        :param params: A tuple of parameters for the query (default is None).
        """
        if not self.cursor:
            print("Error: Cursor not initialized")
            return
        try:
            print(f"Executing query: {query}")
            if params:
                print(f"With parameters: {params}")
            self.cursor.execute(query, params)
            self.connection.commit()
            print("Query executed successfully.")
        except Exception as e:
            print(f"Error executing query: {e}")
            print(f"Query that failed: {query}")
            self.connection.rollback()

    def fetch_all(self, query: str, params: tuple = None):
        """
        Execute a SELECT query and return all results.
        
        :param query: The SQL query to execute.
        :param params: A tuple of parameters for the query (default is None).
        :return: A list of rows from the result.
        """
        if not self.cursor:
            print("Error: Cursor not initialized")
            return []
        try:
            print(f"Fetching data with query: {query}")
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching data: {e}")
            return []

    def close(self):
        """Close the database connection and cursor."""
        if self.cursor:
            self.cursor.close()
            print("Cursor closed.")
        if self.connection:
            self.connection.close()
            print("Database connection closed.")