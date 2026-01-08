import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei', 'WenQuanYi Micro Hei', 'Heiti TC']
plt.rcParams['axes.unicode_minus'] = False

# 1. 导入数据（同之前）
characters = [
    "于连", "傅凯", "彼拉神甫", "拉穆尔侯爵", "爱丽莎", 
    "玛蒂尔德", "瑞那先生", "瑞那夫人", "瓦勒诺", 
    "菲华格夫人", "诺尔拜", "谢朗神甫", "阿尔泰米拉"
]

interactions = [
    ("于连", "瑞那夫人", 124), ("于连", "玛蒂尔德", 100), ("于连", "瑞那先生", 42),
    ("于连", "彼拉神甫", 30), ("于连", "瓦勒诺", 30), ("于连", "菲华格夫人", 29),
    ("于连", "拉穆尔侯爵", 28), ("于连", "傅凯", 23), ("于连", "谢朗神甫", 21),
    ("玛蒂尔德", "菲华格夫人", 18), ("于连", "诺尔拜", 16), ("瑞那先生", "瓦勒诺", 14),
    ("于连", "阿尔泰米拉", 10), ("爱丽莎", "瑞那夫人", 9), ("于连", "爱丽莎", 8),
    ("瑞那夫人", "瓦勒诺", 7), ("傅凯", "玛蒂尔德", 6), ("彼拉神甫", "拉穆尔侯爵", 6),
    ("玛蒂尔德", "阿尔泰米拉", 6), ("拉穆尔侯爵", "玛蒂尔德", 5), ("瑞那先生", "瑞那夫人", 5),
    ("爱丽莎", "瓦勒诺", 5), ("彼拉神甫", "谢朗神甫", 5), ("玛蒂尔德", "诺尔拜", 4),
    ("瑞那先生", "谢朗神甫", 4), ("彼拉神甫", "玛蒂尔德", 3), ("瓦勒诺", "谢朗神甫", 3),
    ("拉穆尔侯爵", "菲华格夫人", 2), ("瑞那夫人", "谢朗神甫", 2), ("傅凯", "谢朗神甫", 2),
    ("玛蒂尔德", "瑞那夫人", 2), ("拉穆尔侯爵", "谢朗神甫", 1), ("彼拉神甫", "瑞那夫人", 1),
    ("傅凯", "瑞那先生", 1), ("傅凯", "爱丽莎", 1), ("傅凯", "瓦勒诺", 1),
    ("傅凯", "瑞那夫人", 1), ("拉穆尔侯爵", "瓦勒诺", 1), ("拉穆尔侯爵", "瑞那先生", 1),
    ("彼拉神甫", "阿尔泰米拉", 1), ("爱丽莎", "玛蒂尔德", 1), ("拉穆尔侯爵", "阿尔泰米拉", 1),
    ("爱丽莎", "瑞那先生", 1), ("菲华格夫人", "阿尔泰米拉", 1)
]

centrality_data = [
    ("于连", 0.1311, 1.0000), ("玛蒂尔德", 0.1025, 0.7500), ("拉穆尔侯爵", 0.0895, 0.6667),
    ("瑞那夫人", 0.0877, 0.6667), ("傅凯", 0.0778, 0.5833), ("谢朗神甫", 0.0777, 0.5833),
    ("瑞那先生", 0.0776, 0.5833), ("瓦勒诺", 0.0776, 0.5833), ("彼拉神甫", 0.0691, 0.5000),
    ("爱丽莎", 0.0681, 0.5000), ("阿尔泰米拉", 0.0605, 0.4167), ("菲华格夫人", 0.0503, 0.3333),
    ("诺尔拜", 0.0305, 0.1667)
]
centrality_df = pd.DataFrame(centrality_data, columns=["人物", "核心度(PageRank)", "社交度(Degree)"])

relationship_types = [
    ("于连", "瑞那夫人", "秘密情人"), ("瑞那先生", "瑞那夫人", "夫妻"),
    ("于连", "玛蒂尔德", "秘密情人/未婚夫妇"), ("拉穆尔侯爵", "玛蒂尔德", "父女"),
    ("于连", "索雷尔老爹", "父子"), ("谢朗神甫", "于连", "启蒙导师/师生"),
    ("瑞那先生", "瓦勒诺", "政治对手/地方权贵"), ("彼拉神甫", "于连", "推荐人/导师"),
    ("玛蒂尔德", "诺尔拜", "朋友/追求者")
]


# 2. 构建人物关系网络
G = nx.DiGraph()
G.add_nodes_from(characters)

for u, v, weight in interactions:
    G.add_edge(u, v, weight=weight)

for u, v, rel_type in relationship_types:
    if G.has_edge(u, v):
        G[u][v]['rel_type'] = rel_type
    else:
        G.add_edge(u, v, weight=0, rel_type=rel_type)


# 3. 可视化配置
node_size_map = {row["人物"]: row["社交度(Degree)"] * 5000 for _, row in centrality_df.iterrows()}
node_sizes = [node_size_map.get(node, 1000) for node in G.nodes()]

max_weight = max([d['weight'] for u, v, d in G.edges(data=True)])
edge_widths = [d['weight'] / max_weight * 8 for u, v, d in G.edges(data=True)]

colors = ['#FF6B6B', '#4ECDC4', '#9B59B6', '#F1C40F', '#3498DB', '#E74C3C', '#2ECC71',
          '#1ABC9C', '#34495E', '#95A5A6', '#F39C12', '#D35400', '#C0392B', '#8E44AD']
cmap = LinearSegmentedColormap.from_list("custom_cmap", colors, N=len(G.nodes()))


# 4. 绘制人物关系网络图（修复标题截断）
plt.figure(figsize=(16, 13))  # 增加图的高度，给标题留空间

pos = nx.spring_layout(G, k=0.8, seed=42)

nx.draw_networkx_edges(
    G, pos,
    arrowstyle="->", arrowsize=20,
    width=edge_widths,
    edge_color="#888888", alpha=0.7
)

nodes = nx.draw_networkx_nodes(
    G, pos,
    node_size=node_sizes,
    node_color=range(len(G.nodes())),
    cmap=cmap, alpha=0.8
)

nx.draw_networkx_labels(
    G, pos,
    font_size=11, font_weight="bold",
    font_family="SimHei"
)

edge_labels = {}
for u, v, d in G.edges(data=True):
    if d['weight'] >= 5:
        rel_type = d.get('rel_type', '互动')
        edge_labels[(u, v)] = f"{rel_type}\n({d['weight']}次)"

nx.draw_networkx_edge_labels(
    G, pos,
    edge_labels=edge_labels,
    font_size=8, font_family="SimHei",
    label_pos=0.35,
    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8)
)

# 调整标题位置和边距，确保完整显示
plt.title("《红与黑》剧本人物关系网络分析", fontsize=18, fontweight="bold", pad=30)
cbar = plt.colorbar(nodes, orientation="vertical", shrink=0.75)
cbar.set_ticks(range(len(G.nodes())))
cbar.set_ticklabels(G.nodes())
cbar.set_label("人物节点", fontsize=12)

plt.axis("off")
plt.tight_layout(rect=[0, 0.05, 1, 0.95])  # 调整布局范围，给标题预留顶部空间
plt.savefig("红与黑人物关系网络图.png", dpi=300, bbox_inches="tight")
plt.show()


# 5. 输出中心度分析结果
print("="*50)
print("《红与黑》人物中心度分析结果")
print("="*50)
print(centrality_df.sort_values(by="核心度(PageRank)", ascending=False).round(4))
print("\n注：核心度(PageRank)越高，代表在关系网络中影响力越大；社交度(Degree)越高，代表直接互动对象越多。")
print("="*50)
