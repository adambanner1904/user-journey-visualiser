import pandas as pd
import sqlite3

DATABASE_PATH = 'temp.db'
SCHEMA = "(previous_page TEXT, page TEXT, page_views INT, unique_page_views INT)"


def create_connection():
    return sqlite3.connect(DATABASE_PATH)


def create_table(name: str) -> None:
    with create_connection() as con:
        con.execute(f'CREATE TABLE "{name}" {SCHEMA}')


def drop_table(name: str) -> None:
    with create_connection() as con:
        con.execute(f'DROP TABLE "{name}"')


def get_tables() -> list[str]:
    with create_connection() as con:
        return flatten(
            con.execute("select name from sqlite_master where type= 'table';")
            .fetchall()
        )

def get_values_from_table(table_name: str, arrow_width_column: str) -> list[tuple]:
    with create_connection() as con:
        return con.execute(
            f'select * from "{table_name}" order by {arrow_width_column} DESC').fetchall()


def insert_dataframe_into_table(table_name: str, df: pd.DataFrame) -> None:
    # Convert df to list of tuples
    records = list(df.itertuples(index=False, name=None))
    with create_connection() as con:
        con.executemany(f'INSERT INTO "{table_name}" VALUES(?, ?, ?, ?);', records)


def table_exists(name: str) -> bool:
    # Flattened list of table names list
    results: list[str] = get_tables()
    if name in results:
        return True
    return False


def flatten(results: list[tuple[str]]) -> list[str]:
    return [result[0] for result in results]
