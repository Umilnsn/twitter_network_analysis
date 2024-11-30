import networkx as nx
import matplotlib.pyplot as plt

def analyze_node_centrality(G):
    degree_centrality = nx.degree_centrality(G)
    top_degree_nodes = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:10]
    print("Top 10 nodes by degree centrality:")
    for node, centrality in top_degree_nodes:
        print(f"Node: {node}, Degree Centrality: {centrality}")
    return top_degree_nodes

def plot_top_nodes(G, top_nodes):
    subgraph = G.subgraph([node for node, _ in top_nodes])
    node_sizes = [centrality * 1000 for _, centrality in top_nodes]
    pos = nx.spring_layout(subgraph)
    nx.draw(subgraph, pos, with_labels=True, node_size=node_sizes, node_color="skyblue")
    plt.title("Top Nodes by Degree Centrality")
    plt.show()
