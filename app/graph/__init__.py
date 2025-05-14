
from app.db import get_values_from_table
import pandas as pd


def create_graph(table_name: str
                 , arrow_width_column: str
                 , graph_precision: float):
    df = get_values_as_dataframe(table_name, arrow_width_column)
    filtered_df = filter_dataset(df, graph_precision)
    return

def filter_dataset(df: pd.DataFrame, arrow_width_column: str, graph_precision: float):
    assert 0 < graph_precision <= 1
    cumsum = df[arrow_width_column].cumsum() / df[arrow_width_column].sum()
    return df[cumsum <= graph_precision]

def get_values_as_dataframe(table_name: str, arrow_width_column: str) -> pd.DataFrame:
    # Results are returned ordered for the filtering
    results = get_values_from_table(table_name, arrow_width_column)
    return pd.DataFrame(results, columns=['previous_page', 'page', arrow_width_column])