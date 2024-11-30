from networkx.algorithms import community
import community.community_louvain as community_louvain

def detect_communities(G):
    # 将图转换为无向图
    undirected_G = G.to_undirected()

    # 打印初始消息
    print("Starting community detection using Louvain method...")

    # 使用 Louvain 算法检测社区
    partition = community_louvain.best_partition(undirected_G)
    print("Community detection completed.")

    # 组织社区信息
    communities = {}
    for node, comm_id in partition.items():
        if comm_id not in communities:
            communities[comm_id] = []
        communities[comm_id].append(node)

    print(f"Number of communities detected: {len(communities)}")

    # 打印前 5 个社群的信息
    for i, (comm_id, nodes) in enumerate(list(communities.items())[:5]):
        print(f"Community {i + 1}: {len(nodes)} nodes")

    return communities
def analyze_cross_community_edges(G, communities):
    """
    分析跨社区边的数量。
    """
    print("\nAnalyzing cross-community edges...")
    cross_edges = 0
    total_edges = G.number_of_edges()
    for i, (u, v) in enumerate(G.edges):
        if communities.get(u) != communities.get(v):
            cross_edges += 1
        # 每处理 10,000 条边打印一次进度
        if (i + 1) % 10000 == 0 or i + 1 == total_edges:
            print(f"Processed {i + 1}/{total_edges} edges. Cross-community edges: {cross_edges}")

    cross_edge_percentage = (cross_edges / total_edges) * 100
    print(f"Cross-community edges: {cross_edges} ({cross_edge_percentage:.2f}% of total edges)")
    return cross_edges, cross_edge_percentage
