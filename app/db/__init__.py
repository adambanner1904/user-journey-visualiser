import pandas as pd
import sqlite3

DATABASE_PATH = 'temp.db'

# Insert data from pandas dataframe into table
def insert_dataframe_into_table(df: pd.DataFrame) -> None:
    return

# Should create a new table with the name of the project
# Name will be used later for dropdown values
def create_table(name:str) -> None:
    return

# Should return whether that name already exists as a table
def table_exists(name: str) -> bool:
    with sqlite3.connect(DATABASE_PATH) as con:
        cur = con.cursor()

        # Flattened list of table names list
        results: list[str] = [result[0] for result in cur.execute("select name from sqlite_master where type= 'table';").fetchall()]
        if name in results:
            return True

    return False