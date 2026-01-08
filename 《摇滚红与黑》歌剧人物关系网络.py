import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 1. 数据（同前，确保人物/互动准确）
characters = ["于", "别人", "德瑞纳先", "拉穆尔侯", "杰洛尼", "法", "爱丽", "玛娣儿", "瑞那夫", "瓦勒", "瓦勒诺夫"]
interactions = [
    ("于", "玛娣儿", 48), ("于", "瑞那夫", 34), ("德瑞纳先", "瑞那夫", 32),
    ("于", "杰洛尼", 17), ("爱丽", "瑞那夫", 16), ("拉穆尔侯", "玛娣儿", 14),
    ("杰洛尼", "瓦勒", 11), ("瓦勒", "瓦勒诺夫", 10), ("德瑞纳先", "瓦勒", 10),
    ("于", "德瑞纳先", 8), ("于", "瓦勒", 8), ("于", "法", 5),
    ("德瑞纳先", "爱丽", 5), ("瑞那夫", "瓦勒", 4), ("玛娣儿", "瓦勒", 3),
    ("玛娣儿", "瑞那夫", 2), ("法", "瓦勒", 2), ("德瑞纳先", "杰洛尼", 2),
    ("于", "拉穆尔侯", 1), ("于", "瓦勒诺夫", 1), ("于", "爱丽", 1),
    ("别人", "德瑞纳先", 1), ("别人", "瓦勒", 1), ("杰洛尼", "瑞那夫", 1),
    ("拉穆尔侯", "瓦勒", 1), ("拉穆尔侯", "杰洛尼", 1), ("杰洛尼", "玛娣儿", 1),
    ("拉穆尔侯", "瓦勒诺夫", 1), ("法", "瑞那夫", 1)
]
centrality_df = pd.DataFrame([
    ("瓦勒", 0.1496, 0.9), ("于", 0.1477, 0.9), ("瑞那夫", 0.1168, 0.7),
    ("德瑞纳先", 0.1041, 0.6), ("杰洛尼", 0.0997, 0.6), ("拉穆尔侯", 0.0862, 0.5),
    ("玛娣儿", 0.0847, 0.5), ("爱丽", 0.0565, 0.3), ("瓦勒诺夫", 0.0564, 0.3),
    ("法", 0.0559, 0.3), ("别人", 0.0425, 0.2)
], columns=["人物", "核心度(PageRank)", "社交度(Degree)"])
relationship_types = [
    ("于", "瑞那夫", "秘密情人"), ("德瑞纳先", "瑞那夫", "夫妻"),
    ("于", "玛娣儿", "秘密情人/未婚夫妇"), ("拉穆尔侯", "玛娣儿", "父女"),
    ("德瑞纳先", "瓦勒", "政治对手/地方权贵"), ("杰洛尼", "于", "朋友/引导者/歌者"),
    ("爱丽", "瑞那夫", "雇主/女仆"), ("法", "于", "辩护关系")
]


# 2. 构建网络
G = nx.DiGraph()
G.add_nodes_from(characters)
for u, v, w in interactions: G.add_edge(u, v, weight=w)
for u, v, t in relationship_types:
    if G.has_edge(u, v): G[u][v]['rel_type'] = t
    else: G.add_edge(u, v, weight=0, rel_type=t)


# 3. 可视化（解决重叠+标签错位）
plt.figure(figsize=(18, 14))
# 强制分散核心节点的布局
pos = {
    "于": (0.2, 0.5), "德瑞纳先": (0.35, 0.5), "瑞那夫": (0.2, 0.65),
    "玛娣儿": (0.05, 0.5), "瓦勒": (0.5, 0.5), "杰洛尼": (0.4, 0.65),
    "拉穆尔侯": (0.05, 0.35), "爱丽": (0.05, 0.65), "法": (0.2, 0.8),
    "别人": (0.7, 0.5), "瓦勒诺夫": (0.65, 0.5)
}

# 绘制元素
node_size_map = {row["人物"]: row["社交度(Degree)"] * 5000 for _, row in centrality_df.iterrows()}
nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=20, width=[d['weight']/max([e[2]['weight'] for e in G.edges(data=True)])*8 for u, v, d in G.edges(data=True)], edge_color="#888", alpha=0.7)
nodes = nx.draw_networkx_nodes(G, pos, node_size=[node_size_map[n] for n in G.nodes()], node_color=range(len(G.nodes())), cmap=LinearSegmentedColormap.from_list("c", ['#FF3366', '#3366FF', '#33CC99', '#FFCC00', '#9966FF', '#FF6666', '#66CCFF', '#FF9900', '#CC6699', '#33CC66', '#999999'], N=11), alpha=0.8)
nx.draw_networkx_labels(G, pos, font_size=13, font_weight="bold")

# 精准匹配边标签
edge_labels = {}
for u, v, d in G.edges(data=True):
    if d['weight'] >= 5:
        edge_labels[(u, v)] = f"{d.get('rel_type', '互动')}\n({d['weight']}次)"
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=10, label_pos=0.4, bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="gray", alpha=0.9))

# 标题与图例
plt.title("《摇滚红与黑》歌剧人物关系网络分析", fontsize=20, pad=35)
cbar = plt.colorbar(nodes, orientation="vertical", shrink=0.7)
cbar.set_ticklabels(G.nodes())
cbar.set_label("人物节点", fontsize=13)
plt.axis("off")
plt.tight_layout(rect=[0, 0.05, 1, 0.95])
plt.savefig("摇滚红与黑人物关系优化版.png", dpi=300, bbox_inches="tight")
plt.show()
