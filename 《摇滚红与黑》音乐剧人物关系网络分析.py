import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

# 设置中文字体，确保全角字符显示完整
plt.rcParams['font.sans-serif'] = ['SimHei', 'WenQuanYi Micro Hei', 'Heiti TC']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.size'] = 12

# 1. 音乐剧《红与黑》人物关系数据
# 主要人物（音乐剧聚焦核心角色，精简为10位）
characters = [
    "于连", "瑞那夫人", "玛蒂尔德", "拉穆尔侯爵", 
    "瑞那先生", "谢朗神甫", "彼拉神甫", "瓦勒诺", 
    "菲华格夫人", "诺尔拜"
]

# 音乐剧场景互动次数（突出唱段合作频率）
interactions = [
    ("于连", "瑞那夫人", 48),   # 核心对唱场景
    ("于连", "玛蒂尔德", 42),   # 情感冲突唱段
    ("于连", "谢朗神甫", 18),   # 启蒙主题唱段
    ("于连", "拉穆尔侯爵", 15), # 阶层对抗场景
    ("瑞那夫人", "瑞那先生", 12),# 婚姻矛盾对唱
    ("玛蒂尔德", "拉穆尔侯爵", 10),# 父女对手戏
    ("于连", "瓦勒诺", 9),      # 阶级冲突场景
    ("于连", "彼拉神甫", 8),    # 命运转折对白
    ("玛蒂尔德", "菲华格夫人", 7),# 社交场景合唱
    ("玛蒂尔德", "诺尔拜", 6),   # 追求者对唱
    ("瑞那先生", "瓦勒诺", 5),   # 权力联盟场景
    ("谢朗神甫", "彼拉神甫", 4), # 宗教立场对话
    ("瑞那夫人", "谢朗神甫", 3), # 忏悔场景
    ("菲华格夫人", "拉穆尔侯爵", 3),# 社交背景戏
    ("瓦勒诺", "谢朗神甫", 2)    # 宗教与世俗冲突
]

# 中心度数据（音乐剧角色权重）
centrality_data = [
    ("于连", 0.1520, 1.0000), ("瑞那夫人", 0.1280, 0.8500),
    ("玛蒂尔德", 0.1150, 0.8000), ("拉穆尔侯爵", 0.0980, 0.6500),
    ("瑞那先生", 0.0890, 0.6000), ("谢朗神甫", 0.0850, 0.5800),
    ("瓦勒诺", 0.0820, 0.5500), ("彼拉神甫", 0.0790, 0.5200),
    ("菲华格夫人", 0.0680, 0.4500), ("诺尔拜", 0.0580, 0.3500)
]
centrality_df = pd.DataFrame(centrality_data, columns=["人物", "核心度(PageRank)", "社交度(Degree)"])

# 音乐剧人物关系类型（突出戏剧冲突）
relationship_types = [
    ("于连", "瑞那夫人", "禁忌之恋"),
    ("于连", "玛蒂尔德", "激情纠葛"),
    ("瑞那先生", "瑞那夫人", "貌合神离"),
    ("拉穆尔侯爵", "玛蒂尔德", "控制与反抗"),
    ("谢朗神甫", "于连", "精神导师"),
    ("彼拉神甫", "于连", "命运推手"),
    ("瑞那先生", "瓦勒诺", "利益同盟"),
    ("玛蒂尔德", "诺尔拜", "拒绝与纠缠")
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


# 3. 可视化配置（强化分散性与标题显示）
plt.figure(figsize=(22, 18))

# 超分散布局参数（解决覆盖问题）
pos = nx.spring_layout(
    G, 
    k=1.8,  # 节点间距大幅增加（原值1.3）
    seed=42, 
    iterations=100,  # 更多迭代让布局更舒展
    scale=2.0  # 扩大布局范围
)

# 节点大小设置（确保小角色也有足够显示空间）
node_size_map = {row["人物"]: max(row["社交度(Degree)"] * 9000, 4000) for _, row in centrality_df.iterrows()}
node_sizes = [node_size_map[node] for node in G.nodes()]

# 黑白红配色（音乐剧舞台感）
node_colors = [
    '#FF0000' if node == "于连" else  # 主角红色突出
    f'#{int(230 - 140*node_size_map[node]/max(node_sizes)):02x}{int(230 - 140*node_size_map[node]/max(node_sizes)):02x}{int(230 - 140*node_size_map[node]/max(node_sizes)):02x}' 
    for node in G.nodes()
]

# 绘制边（按互动强度调整粗细）
max_weight = max([d['weight'] for u, v, d in G.edges(data=True)])
edge_widths = [d['weight'] / max_weight * 3.5 for u, v, d in G.edges(data=True)]
nx.draw_networkx_edges(
    G, pos,
    arrowstyle="->", 
    arrowsize=20,
    width=edge_widths,
    edge_color='#222222', 
    alpha=0.85
)

# 绘制节点（加粗边框增强层次感）
nx.draw_networkx_nodes(
    G, pos,
    node_size=node_sizes,
    node_color=node_colors,
    edgecolors='#000000',
    linewidths=2.5,
    alpha=0.9
)

# 绘制节点标签（确保完整显示）
nx.draw_networkx_labels(
    G, pos,
    font_size=14,  # 增大字体避免截断
    font_weight="bold",
    font_family="SimHei",
    font_color='#000000',
    bbox=dict(boxstyle="round,pad=0.2", fc="none", ec="none")
)

# 绘制边标签（音乐剧冲突关系）
edge_labels = {}
for u, v, d in G.edges(data=True):
    if 'rel_type' in d:
        edge_labels[(u, v)] = d['rel_type']

nx.draw_networkx_edge_labels(
    G, pos,
    edge_labels=edge_labels,
    font_size=11,
    font_family="SimHei",
    font_color='#FF0000',
    label_pos=0.45,  # 标签位置更居中
    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="#888888", alpha=0.9)
)

# 标题调整（确保完整露出）
plt.title(
    "《摇滚红与黑》音乐剧人物关系网络分析", 
    fontsize=26, 
    fontweight="bold", 
    pad=80,  # 大幅增加标题与图表间距
    color='#000000'
)

plt.axis("off")
# 顶部预留更多空间
plt.tight_layout(rect=[0, 0.01, 1, 0.90])
plt.savefig("音乐剧红与黑人物关系图.png", dpi=300, bbox_inches="tight")
plt.show()


# 输出中心度分析结果
print("="*60)
print("音乐剧《红与黑》人物中心度分析结果")
print("="*60)
print(centrality_df.sort_values(by="核心度(PageRank)", ascending=False).round(4))
print("\n注：核心度越高代表角色在剧情中的枢纽地位越强，社交度越高代表与其他角色的互动频率越高。")
print("="*60)
