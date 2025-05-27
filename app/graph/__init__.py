
from app.db import get_values_from_table
import pandas as pd
from pyvis.network import Network
import matplotlib.colors as mcolors


def write_graph_html(chosen_project, chosen_edge_width, precision=0.9):
    g = Graph(chosen_project, chosen_edge_width, precision)
    g.create_graph()


class Graph:

    def __init__(self
                 , table_name: str
                 , arrow_width_column: str
                 , graph_precision: float):

        self.table_name = table_name
        self.arrow_width_column = arrow_width_column
        self.graph_precision = graph_precision

        self.df = None
        self.filtered_df = None
        self.width_normaliser = None
        self.nodes = None
        self.network = None

    def create_graph(self):
        # Populates self.df
        self.create_dataframe()
        # Populates self.filtered_df
        self.filter_dataset()
        # Populates nodes with a list of distinct page names
        self.create_nodes()
        # Populates self.network with a pyvis.network.Network object
        self.create_network()

        self.network.show('app/templates/graph.html', notebook=False)

    def create_dataframe(self):
        # Results are returned ordered for the filtering
        results = get_values_from_table(self.table_name, self.arrow_width_column)
        self.df = pd.DataFrame(results, columns=['previous_page', 'page', 'page_views', 'unique_page_views'])
        for col in ["page", "previous_page"]:
            self.df[col] = self.df[col].str.replace("/", "/\n")

    def filter_dataset(self):
        assert 0 < self.graph_precision <= 1
        cumsum = self.df[self.arrow_width_column].cumsum() / self.df[self.arrow_width_column].sum()
        self.filtered_df = self.df[cumsum <= self.graph_precision]

        # Since we have the filtered df we can create the normaliser
        self.width_normaliser = mcolors.Normalize(
            vmin=self.filtered_df[self.arrow_width_column].min(),
            vmax=self.filtered_df[self.arrow_width_column].max()
        )



    def create_nodes(self):
        self.nodes = pd.concat([self.filtered_df.page, self.filtered_df.previous_page]).unique().tolist()

    def create_network(self):
        self.network = Network(height='100%'
                               , width='100%'
                               , directed=True
                               , notebook=False)

        # TODO: Add node attributes
        #  label: edit to remove root url and display in legend
        #  size: page_traffic, unique_page_traffic into node
        #  color: drop_out_rate, time_on_page
        #  title: display all metrics ^^
        # Handle entrance node
        self.network.add_node('(entrance)', '(entrance)', shape='diamond', color='red')
        for node in self.nodes:
            self.network.add_node(n_id=node, title=node)

        for _, row in self.filtered_df.iterrows():
            width = self.width_normaliser(row[self.arrow_width_column])

            # TODO: add colour column

            title = f"{self.arrow_width_column}: {row[self.arrow_width_column]}"
            self.network.add_edge(source=row.previous_page
                                  , to=row.page
                                  , value=width
                                  , title=title)

        self.network.toggle_physics(True)
        self.network.set_edge_smooth("dynamic")
        self.network.set_options(
            f"""var options = {{
                  "nodes": {{
                    "font": {{
                        "size": 18
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

def default_graph():
    return Graph("pay_online", "unique_page_views", 0.9)
