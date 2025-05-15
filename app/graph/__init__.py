
from app.db import get_values_from_table, get_distinct_pages
import pandas as pd
from pyvis.network import Network

class Graph:

    def __init__(self
                 , table_name: str
                 ,arrow_width_column: str
                 ,graph_precision:float):

        self.table_name = table_name
        self.arrow_width_column = arrow_width_column
        self.graph_precision = graph_precision

        self.df = None
        self.filtered_df = None
        self.nodes = None
        self.network = None

    def create_graph(self):
        # Populates self.df
        self.create_dataframe()
        # Populates self.filtered_df
        self.filter_dataset()
        # Populates nodes with a list of distinct page names
        self.nodes = get_distinct_pages()
        # Populates self.network with a pyvis.network.Network object
        self.create_network()




    def filter_dataset(self):
        assert 0 < self.graph_precision <= 1
        cumsum = self.df[self.arrow_width_column].cumsum() / self.df[self.arrow_width_column].sum()
        self.filtered_df = self.df[cumsum <= self.graph_precision]

    def create_dataframe(self):
        # Results are returned ordered for the filtering
        results = get_values_from_table(self.table_name, self.arrow_width_column)
        self.df = pd.DataFrame(results, columns=['previous_page', 'page', self.arrow_width_column])

    def create_network(self):
        self.network = Network(height='100%'
                     , width='100%'
                     , directed=True
                     , notebook=False)

        self.network.add_nodes(self.nodes, title=self.nodes)

        for _, row in self.filtered_df.iterrows():
            # TODO: normalise width first
            width = row[self.arrow_width_column]

            # TODO: add colour column

            title = f"{self.arrow_width_column}: {row[self.arrow_width_column]}"
            self.network.add_edge(source=row.previous_page
                        , to=row.page
                        , value=width)
        self.network.set_edge_smooth("dynamic")
        self.network.set_options(
            f"""var options = {{
                  "nodes": {{
                    "font": {{
                        "size": 10
                        }}
                    }},
                  "physics": {{
                    "barnesHut": {{
                      "gravitationalConstant": -15000,
                      "springLength": 85,
                      "springConstant": 0.155
                    }},
                    "maxVelocity": 50,
                    "minVelocity": 0.75
                  }}
                }}
                """)
