import sqlite3


def execute_query(query, params=None):
    """
    Execute a given query on the SQLite database.

    Parameters:
    - query (str): The SQL query to be executed.
    - params (tuple, optional): The parameters to be used with the query.

    Returns:
    - list: The fetched results from the query if it is a SELECT query.
    - None: If the query is not a SELECT query.
    """
    conn = sqlite3.connect('assets/data.db')
    cursor = conn.cursor()

    try:
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)

        if query.strip().lower().startswith('select'):
            results = cursor.fetchall()
            conn.close()
            return results
        else:
            conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        conn.close()


# Create table query
create_table_query = '''
CREATE TABLE IF NOT EXISTS stb (
    id INTEGER PRIMARY KEY,
    odoo_id INTEGER,
    name VARCHAR(255)
);
'''

# Execute the create table query
execute_query(create_table_query)
