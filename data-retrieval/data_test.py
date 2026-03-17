import json
from pathlib import Path
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#----------------------------------------------------------------
# this is a test file used to collect stats about courses.json
# and run some tests for game balancing purposes
#----------------------------------------------------------------

# cosine calculator
def cos_sim(a, b):
    dot = 0
    for i in range(min(len(a), len(b))):
        dot += a[i] * b[i]
    return dot

def sim_scale(dot_prod):
    # 0.512\ +\ 0.35\arctan\left(14\left(x-0.6\right)\right)
    # where x is (d + 1) / 2, to first scale into the 0-1 range
    return 0.35 * math.atan(14 * ((dot_prod + 1) / 2 - 0.6)) + 0.512

# get json source file locations
rootPath = Path(__file__).resolve().parents[1]
jsonPath = rootPath / "frontend" / "src" / "lib" / "domain" / "server" / "courses.json"

# get data from json
data = []
with open(jsonPath) as fi:
    data = json.load(fi)

df = pd.DataFrame(data)
vectors = [d["vector"] for d in data]
vectors_matrix = np.array(vectors)

# getting some statistics on vector embeddings
scores_matrix = vectors @ vectors_matrix.T
scaled_matrix = 0.35 * np.arctan(14 * ((scores_matrix + 1) / 2 - 0.6)) + 0.512

print("general data on scores:\n----------------------------------------------------------------")
print(f"mean: {scores_matrix.mean()}")
print(f"stdev: {scores_matrix.std()}")
print("")
print(f"scaled mean: {scaled_matrix.mean()}")
print(f"scaled stdev: {scaled_matrix.std()}")
print("")

print("minimum similarity:\n----------------------------------------------------------------")
dot_mins = scores_matrix.min()
print(f"min: {dot_mins}")
print(f"scaled min: {sim_scale(dot_mins)}")
argmin = np.unravel_index(scores_matrix.argmin(), scores_matrix.shape)
minCoursesTitles = [data[i]["courseId"] + ": " + data[i]["title"] for i in argmin]
print(f"min courses: {minCoursesTitles}")
print("")

# plotting scores and scaled scores
scores_freq, scores_edges = np.histogram(scores_matrix, bins="auto")
scaled_freq, scaled_edges = np.histogram(scaled_matrix, bins="auto")

f, axes = plt.subplots(1, 2)
axes[0].bar(scores_edges[:-1], scores_freq, width=np.diff(scores_edges))
axes[0].set_title("Unscaled scores")
axes[0].set_xlabel("Scores")
axes[0].set_ylabel("Frequency")

axes[1].bar(scaled_edges[:-1], scaled_freq, width=np.diff(scaled_edges))
axes[1].set_title("Scaled scores")
axes[1].set_xlabel("Scores")
axes[1].set_ylabel("Frequency")

plt.tight_layout()
plt.savefig("score-figs.png")