import networkx as nx

def load_graph(file_path, max_edges=5000000):
    G = nx.DiGraph()
    edge_count = 0

    # 加载文件，逐行读取
    with open(file_path, "r") as file:
        for line in file:
            nodes = line.strip().split()
            if len(nodes) == 2:  # 确保每行包含两个节点
                G.add_edge(int(nodes[0]), int(nodes[1]))
                edge_count += 1

            if edge_count % 100000 == 0:
                print(f"Progress: Loaded {edge_count} edges...")

            if edge_count == max_edges:  # 达到指定边数量，停止加载
                print(f"Loaded {edge_count} edges. Stopping early.")
                break

    print(f"Graph loaded with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")
    return G
