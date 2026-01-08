Python 3.13.2 (tags/v3.13.2:4f8bb39, Feb  4 2025, 15:23:48) [MSC v.1942 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 设置中文字体，确保标签完整显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'WenQuanYi Micro Hei', 'Heiti TC']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 12  # 增大基础字体大小

# 1. 导入数据
characters = [
    "于连", "傅凯", "彼拉神甫", "拉穆尔侯爵", "爱丽莎", 
    "玛蒂尔德", "瑞那先生", "瑞那夫人", "瓦勒诺", "菲华格夫人", 
    "诺尔拜", "谢朗神甫", "阿尔泰米拉"
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
    ("谢朗神甫", "于连", "启蒙导师/师生"), ("瑞那先生", "瓦勒诺", "政治对手"),
    ("彼拉神甫", "于连", "推荐人/导师"), ("玛蒂尔德", "诺尔拜", "朋友/追求者")
]


# 2. 构建网络
G = nx.DiGraph()
G.add_nodes_from(characters)
for u, v, weight in interactions:
    G.add_edge(u, v, weight=weight)
for u, v, rel_type in relationship_types:
    if G.has_edge(u, v):
        G[u][v]['rel_type'] = rel_type
    else:
        G.add_edge(u, v, weight=0, rel_type=rel_type)


# 3. 可视化配置（重点解决标签显示不全）
plt.figure(figsize=(22, 18))  # 增大画布尺寸

# 更分散的布局，避免标签重叠
pos = nx.spring_layout(G, k=1.3, seed=42, iterations=50)  # 增加迭代次数让布局更稳定

# 节点大小调整：确保小节点也能容纳标签
node_size_map = {row["人物"]: max(row["社交度(Degree)"] * 8000, 3000) for _, row in centrality_df.iterrows()}
node_sizes = [node_size_map[node] for node in G.nodes()]

# 节点颜色：于连红色，其他灰度（确保节点足够大以显示标签）
node_colors = ['#FF0000' if node == "于连" else f'#{int(220 - 120*node_size_map[node]/max(node_sizes)):02x}{int(220 - 120*node_size_map[node]/max(node_sizes)):02x}{int(220 - 120*node_size_map[node]/max(node_sizes)):02x}' for node in G.nodes()]

# 绘制边
max_weight = max([d['weight'] for u, v, d in G.edges(data=True)])
edge_widths = [d['weight'] / max_weight * 3 for u, v, d in G.edges(data=True)]
nx.draw_networkx_edges(
    G, pos,
    arrowstyle="->", arrowsize=18,
    width=edge_widths,
    edge_color='#333333', alpha=0.8
)

# 绘制节点（增大边框，确保标签在节点内）
nx.draw_networkx_nodes(
    G, pos,
    node_size=node_sizes,
    node_color=node_colors,
    edgecolors='#000000',
    linewidths=2,
    alpha=0.9
)

# 绘制节点标签（强制完整显示，调整字体大小和位置）
nx.draw_networkx_labels(
    G, pos,
    font_size=13,  # 进一步增大标签字体
    font_weight="bold",
    font_family="SimHei",
    font_color='#000000',
    bbox=dict(boxstyle="round,pad=0.1", fc="none", ec="none")  # 标签背景透明，避免遮挡
... )
... 
... # 绘制边标签（简化关系描述，避免过长）
... edge_labels = {}
... for u, v, d in G.edges(data=True):
...     if 'rel_type' in d:
...         # 简化关系标签，确保显示清晰
...         short_rel = d['rel_type'].replace("/", "\n")  # 换行显示长关系
...         edge_labels[(u, v)] = short_rel
... 
... nx.draw_networkx_edge_labels(
...     G, pos,
...     edge_labels=edge_labels,
...     font_size=10,
...     font_family="SimHei",
...     font_color='#FF0000',
...     label_pos=0.4,
...     bbox=dict(boxstyle="round,pad=0.2", fc="white", ec="#999999", alpha=0.8)
... )
... 
... # 标题调整
... plt.title("《红与黑》小说人物关系网络分析", fontsize=24, fontweight="bold", pad=60, color='#000000')
... 
... plt.axis("off")
... plt.tight_layout(rect=[0, 0.01, 1, 0.92])  # 更多顶部空间
... plt.savefig("红与黑小说人物关系标签完整版.png", dpi=300, bbox_inches="tight")
... plt.show()
... 
... 
... # 输出中心度分析结果
... print("="*60)
... print("《红与黑》小说人物中心度分析结果")
... print("="*60)
... print(centrality_df.sort_values(by="核心度(PageRank)", ascending=False).round(4))
... print("\n注：核心度(PageRank)越高，代表在关系网络中影响力越大；社交度(Degree)越高，代表直接互动对象越多。")
