from sklearn.cluster import KMeans
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import umap.umap_ as umap

# get json source file locations
rootPath = Path(__file__).resolve().parents[2]
jsonPath = rootPath / "frontend" / "src" / "lib" / "domain" / "server" / "courses.json"

# get data from json
df = pd.read_json(jsonPath)
vectors = np.stack(df["vector"].to_numpy())
print("collected vectors")

# setting up KMeans
K = 20
km = KMeans(n_clusters=K)

# fit_predict using KMeans
labels = km.fit_predict(vectors)
df["cluster"] = labels
print("predicted labels via KMeans")

# clusters in text form (top 10 sample)
""" for c in range(K):
    print(f"\nCluster {c}")
    sample = df[df["cluster"] == c]["title"].head(10)
    print(sample.tolist())
"""

# umap processing
reducer = umap.UMAP(n_neighbors=30, n_components=2)
coords2D = reducer.fit_transform(vectors)
df["x"] = coords2D[:, 0] # first col
df["y"] = coords2D[:, 1] # second col
print("reduced to 2D via umap")

# plot on scatter
plt.scatter(df["x"], df["y"], s=5, c=df["cluster"], cmap="tab20")
plt.axis("off")
plt.show()
