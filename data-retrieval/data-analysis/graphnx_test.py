from pathlib import Path
import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

# get json source file locations
rootPath = Path(__file__).resolve().parents[2]
jsonPath = rootPath / "frontend" / "src" / "lib" / "domain" / "server" / "courses.json"

# get data from json
df = pd.read_json(jsonPath)
vectors = np.stack(df["vector"].to_numpy())
scores_matrix = vectors @ vectors.T
scaled_matrix = 0.35 * np.arctan(14 * ((scores_matrix + 1) / 2 - 0.6)) + 0.512
print("collected vectors and vector matrices")

# set up graph
MIN_CLOSENESS = 0.9
g = nx.Graph()
for i, r in df.iterrows():
    g.add_node(i)

df_len = len(df)
for i in range(df_len):
    for j in range(i+1, df_len):
        if scaled_matrix[i, j] > MIN_CLOSENESS:
            g.add_edge(i, j)
print("set up graph")

# analyze for degree, closeness, and between centralities
TOP_TO_VIEW = 10
deg_centrality = nx.degree_centrality(g)
top_d_cent_idxs = sorted(deg_centrality.items(), key=lambda x: x[1], reverse=True)[:TOP_TO_VIEW]

print("top degree centrality: most connected")
for i, (df_i, centrality) in enumerate(top_d_cent_idxs):
    row = df.iloc[df_i]
    print(f"{i+1}. {row["courseId"]}: {row["title"]}")
print("")

cls_centrality = nx.closeness_centrality(g)
top_c_cent_idxs = sorted(cls_centrality.items(), key=lambda x: x[1], reverse=True)[:TOP_TO_VIEW]

print("top closeness centrality: how short of paths to connect to other nodes")
for i, (df_i, centrality) in enumerate(top_c_cent_idxs):
    row = df.iloc[df_i]
    print(f"{i+1}. {row["courseId"]}: {row["title"]}")
print("")

betw_centrality = nx.betweenness_centrality(g)
top_b_cent_idxs = sorted(betw_centrality.items(), key=lambda x: x[1], reverse=True)[:TOP_TO_VIEW]

print("top betweeness centrality: most interdisciplinary")
for i, (df_i, centrality) in enumerate(top_b_cent_idxs):
    row = df.iloc[df_i]
    print(f"{i+1}. {row["courseId"]}: {row["title"]}")
print("")
