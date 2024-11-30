from load_data import load_graph
from node_analysis import analyze_node_centrality, plot_top_nodes
from network_structure import detect_communities, analyze_cross_community_edges
from spread_simulation import simulate_spread
import networkx as nx
import random
import matplotlib.pyplot as plt

def analyze_global_properties(G):
    """
    分析图的全局特性并打印结果。
    :param G: NetworkX 图
    """
    print("\nAnalyzing global network properties...")
    degrees = [deg for _, deg in G.degree()]
    print(f"Average degree: {sum(degrees) / len(degrees):.2f}")
    print(f"Maximum degree: {max(degrees)}")

    # 跳过直径计算（如果图太大）
    print("Calculating network diameter...")
    try:
        if nx.is_connected(G.to_undirected()):
            diameter = nx.diameter(G.to_undirected())
        else:
            largest_cc = max(nx.connected_components(G.to_undirected()), key=len)
            subgraph = G.subgraph(largest_cc)
            diameter = nx.diameter(subgraph)
        print(f"Network diameter: {diameter}")
    except Exception as e:
        print(f"Diameter calculation skipped due to: {e}")

    # 平均聚类系数（优化版）
    print("Calculating average clustering coefficient...")
    try:
        sampled_nodes = random.sample(list(G.nodes), min(10000, len(G.nodes)))
        subgraph = G.subgraph(sampled_nodes).copy()
        avg_clustering = nx.average_clustering(subgraph.to_undirected())
        print(f"Sampled average clustering coefficient: {avg_clustering:.4f}")
    except Exception as e:
        print(f"Clustering calculation skipped due to: {e}")

    # 连接成分数量
    print("Calculating number of connected components...")
    components = nx.number_connected_components(G.to_undirected())
    print(f"Number of connected components: {components}")

    return degrees



def plot_degree_distribution(degrees):
    """
    绘制度分布的直方图。
    """
    plt.figure(figsize=(10, 6))
    plt.hist(degrees, bins=50, color="skyblue", edgecolor="black")
    plt.title("Degree Distribution")
    plt.xlabel("Degree")
    plt.ylabel("Frequency")
    plt.yscale("log")
    plt.show()


def sample_graph(G, sample_ratio=0.1):
    """
    抽样图中的部分节点和边。
    """
    sampled_nodes = random.sample(list(G.nodes), int(len(G.nodes) * sample_ratio))
    sampled_G = G.subgraph(sampled_nodes).copy()
    return sampled_G


def plot_cross_community_edges(cross_edge_percentage):
    """
    可视化跨社区边的比例。
    """
    labels = ['Cross-Community Edges', 'Intra-Community Edges']
    sizes = [cross_edge_percentage, 100 - cross_edge_percentage]
    colors = ['skyblue', 'lightgreen']
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.title("Cross-Community vs Intra-Community Edges")
    plt.show()


if __name__ == "__main__":
    # 数据路径
    file_path = "/Users/linransheng/Desktop/networksci/final_project/twitter_rv.net"

    # 加载图数据
    print("Loading graph data...")
    G = load_graph(file_path)
    print(f"Loaded graph with {len(G.nodes)} nodes and {len(G.edges)} edges.")

    # 全局网络特性分析
    print("\nAnalyzing global properties of the original graph...")
    analyze_global_properties(G)

    # 抽样逻辑
    print("\nSampling graph data...")
    sample_ratio = 0.5  # 调整抽样比例
    sampled_G = sample_graph(G, sample_ratio=sample_ratio)
    print(f"Sampled graph has {len(sampled_G.nodes)} nodes and {len(sampled_G.edges)} edges.")

    # 全局特性分析（抽样图）
    print("\nAnalyzing global properties of the sampled graph...")
    sampled_degrees = analyze_global_properties(sampled_G)

    # 绘制度分布
    print("\nPlotting degree distribution for sampled graph...")
    plot_degree_distribution(sampled_degrees)

    # 中心性分析
    print("\nAnalyzing node centrality...")
    top_nodes = analyze_node_centrality(sampled_G)
    print(f"Top 10 nodes by degree centrality: {top_nodes}")

    # 可视化度中心性最高的节点
    print("\nPlotting top nodes...")
    plot_top_nodes(sampled_G, top_nodes)

    # 社群检测
    print("\nDetecting communities...")
    communities = detect_communities(sampled_G)
    print(f"Detected {len(communities)} communities.")

    # 打印社群信息
    print("\nCommunity details:")
    for i, comm_id in enumerate(list(communities.keys())[:5]):  # 打印前 5 个社群
        print(f"Community {i + 1}: {len(communities[comm_id])} nodes")

    # 跨社区分析
    print("\nAnalyzing cross-community edges...")
    cross_edges, cross_edge_percentage = analyze_cross_community_edges(sampled_G, communities)
    plot_cross_community_edges(cross_edge_percentage)

    # 传播模拟
    print("\nSimulating spread...")
    seed_nodes = [node for node, _ in top_nodes[:3]]  # 选择前 3 个度中心性最高的节点
    active_counts = simulate_spread(sampled_G, seed_nodes)

    # 测试不同种子节点数量
    seed_sizes = [1, 3, 5, 10]
    spread_results = {}
    for size in seed_sizes:
        print(f"\nSimulating spread with {size} seed nodes...")
        seed_nodes = [node for node, _ in top_nodes[:size]]
        spread_results[size] = simulate_spread(sampled_G, seed_nodes)

    # 绘制传播结果比较
    plt.figure(figsize=(10, 6))
    for size, counts in spread_results.items():
        plt.plot(counts, marker="o", label=f"{size} Seed Nodes")
    plt.title("Spread Simulation with Different Seed Sizes")
    plt.xlabel("Step")
    plt.ylabel("Number of Active Nodes")
    plt.legend()
    plt.show()

    # 比较社区和跨社区传播能力
    community_seed_nodes = [node for comm in list(communities.values())[:1] for node in comm[:3]]  # 社区内节点
    cross_community_seed_nodes = [node for comm in list(communities.values())[1:2] for node in comm[:3]]  # 跨社区节点

    print("\nSimulating spread with community seed nodes...")
    community_spread = simulate_spread(sampled_G, community_seed_nodes)

    print("\nSimulating spread with cross-community seed nodes...")
    cross_community_spread = simulate_spread(sampled_G, cross_community_seed_nodes)

    plt.figure(figsize=(10, 6))
    plt.plot(community_spread, marker="o", label="Community Seed Nodes")
    plt.plot(cross_community_spread, marker="s", label="Cross-Community Seed Nodes")
    plt.title("Spread Simulation Comparison")
    plt.xlabel("Step")
    plt.ylabel("Number of Active Nodes")
    plt.legend()
    plt.show()
