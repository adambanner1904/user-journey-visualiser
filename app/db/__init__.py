import pandas as pd
import sqlite3

DATABASE_PATH = 'temp.db'
SCHEMA = "(previous_page TEXT, page TEXT, page_views INT, unique_page_views INT)"

def create_connection():
    con = sqlite3.connect(DATABASE_PATH)
    con.row_factory = sqlite3.Row
    return con


# Insert data from pandas dataframe into table
def insert_dataframe_into_table(table_name: str, df: pd.DataFrame) -> None:
    # Convert df to list of tuples
    records = list(df.itertuples(index=False, name=None))

    with create_connection() as con:
        con.executemany(f'INSERT INTO "{table_name}" VALUES(?, ?, ?, ?);', records)


# Should create a new table with the name of the project
# Name will be used later for dropdown values
def create_table(name: str) -> None:
    with create_connection() as con:
        con.execute(f'CREATE TABLE {name} {SCHEMA}')
    return


# Should return whether that name already exists as a table
def table_exists(name: str) -> bool:
    with create_connection() as con:
        # Flattened list of table names list
        results: list[str] = [result[0] for result in
                              con.execute("select name from sqlite_master where type= 'table';").fetchall()]
        if name in results:
            return True

    return False
