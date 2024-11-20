import mysql.connector
from mysql.connector import Error
import streamlit as st
from typing import Generator

# Function to establish a connection to the MySQL database
def connect_to_mysql(host, user, password, database):
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        if connection.is_connected():
            st.success("Successfully connected to the database")
            return connection
    except Error as e:
        st.error(f"Error while connecting to MySQL: {str(e)}")
        return None

# Generator function to delete rows in batches lazily
def delete_batches(connection, schema: str, table: str, column: str, start_date: str, end_date: str, batch_size: int) -> Generator[int, None, None]:
    cursor = connection.cursor()
    try:
        while True:
            try:
                # Perform a batch delete
                query = f"""
                    DELETE FROM {schema}.{table}
                    WHERE {column} >= %s AND {column} < %s
                    LIMIT %s
                """
                cursor.execute(query, (start_date, end_date, batch_size))
                connection.commit()

                # Yield the number of rows deleted
                rows_deleted = cursor.rowcount
                yield rows_deleted

                # Stop if no more rows are deleted
                if rows_deleted == 0:
                    break
            except Error as e:
                st.error(f"Error during batch deletion: {str(e)}")
                break
    except Error as e:
        st.error(f"Error while processing deletion batches: {str(e)}")
    finally:
        if cursor:
            cursor.close()

# Functional wrapper to execute the deletion process
def run_deletion_process(connection, schema: str, table: str, column: str, start_date: str, end_date: str, batch_size: int):
    try:
        st.info(f"Starting deletion process for {schema}.{table} where {column} (TIMESTAMP) is between {start_date} and {end_date}...")

        # Use a generator to lazily evaluate deletion batches
        total_deleted = 0
        for rows_deleted in delete_batches(connection, schema, table, column, start_date, end_date, batch_size):
            total_deleted += rows_deleted
            st.info(f"Deleted {rows_deleted} rows. Total deleted so far: {total_deleted}")

        st.success(f"Deletion process completed for {schema}.{table}. Total rows deleted: {total_deleted}")
    except Error as e:
        st.error(f"Error during the deletion process: {str(e)}")

# Main execution
if __name__ == "__main__":
    try:
        # Database connection parameters
        DB_HOST = st.text_input("Enter database host:", "your-rds-endpoint")
        DB_USER = st.text_input("Enter database user:", "your-username")
        DB_PASSWORD = st.text_input("Enter database password:", type="password")
        DB_NAME = st.text_input("Enter database name:", "warmachine")

        # Table and column details
        SCHEMA = st.text_input("Enter schema name:", "warmachine")
        TABLE = st.text_input("Enter table name:", "frete_cotacao")
        COLUMN = st.text_input("Enter column name for WHERE condition:", "datahora_criacao")

        # Deletion range and batch size
        START_DATE = st.text_input("Enter start date (YYYY-MM-DD HH:MM:SS):", "2021-10-21 00:00:00")
        END_DATE = st.text_input("Enter end date (YYYY-MM-DD HH:MM:SS):", "2023-12-31 23:59:59")
        BATCH_SIZE = st.number_input("Enter batch size:", min_value=1, value=10000, step=1000)

        if st.button("Start Deletion Process"):
            connection = connect_to_mysql(DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)
            if connection:
                try:
                    run_deletion_process(connection, SCHEMA, TABLE, COLUMN, START_DATE, END_DATE, BATCH_SIZE)
                finally:
                    connection.close()
                    st.info("Database connection closed.")
    except Error as e:
        st.error(f"Unexpected error: {str(e)}")
