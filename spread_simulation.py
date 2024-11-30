import random

def simulate_spread(G, seed_nodes, max_steps=5):
    """
    模拟信息传播。
    """
    print("\nSimulating spread...")
    active_nodes = set(seed_nodes)
    new_active_nodes = set(seed_nodes)
    active_counts = [len(active_nodes)]

    for step in range(1, max_steps + 1):
        if not new_active_nodes:
            break
        current_new_nodes = set()
        for node in new_active_nodes:
            neighbors = set(G.neighbors(node))
            # 模拟传播
            for neighbor in neighbors - active_nodes:
                if random.random() < 0.1:  # 传播概率
                    current_new_nodes.add(neighbor)
        new_active_nodes = current_new_nodes
        active_nodes.update(new_active_nodes)
        active_counts.append(len(active_nodes))

        # 打印进度
        print(f"Step {step}/{max_steps}: {len(new_active_nodes)} new nodes active, {len(active_nodes)} total active nodes.")

    return active_counts

