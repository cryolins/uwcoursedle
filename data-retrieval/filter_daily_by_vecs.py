from pathlib import Path
import numpy as np
import pandas as pd

# further filter what's allowed on the daily list by 

rootPath = Path(__file__).resolve().parents[1]
COURSES_FILE = rootPath / "frontend" / "src" / "lib" / "domain" / "server" / "courses.json"
PLAYABLES_FILE = "playable-list.json"
OUTPUT_FILE = rootPath / "frontend" / "src" / "lib" / "domain" / "server" / "playable-list.json"

df = pd.read_json(COURSES_FILE)
play_ser = pd.read_json(PLAYABLES_FILE, typ="series")
play_ser.name = "courseId"

# get vectors then trim df columns
vectors = df["vector"]
df = df[["courseId"]]

vectors_matrix = np.stack(vectors.to_numpy())
scores_matrix = vectors_matrix @ vectors_matrix.T
print("collected vectors matrix and collected_df courseIds")

# get top k averages
K = 25
top_k_avgs = []
for i in range(len(scores_matrix)):
    course_scores = scores_matrix[i]
    course_scores = np.delete(course_scores, i) # remove itself
    top_k = np.sort(course_scores)[-K:]
    scaled_top_k = 0.35 * np.arctan(14 * ((top_k + 1) / 2 - 0.6)) + 0.512

    avg_sim = np.mean(scaled_top_k)
    top_k_avgs.append(avg_sim)
print(f"obtained top {K} averages")

# get qth percentile of top k averages
Q = 10
qth_percentile = np.percentile(top_k_avgs, Q)
df["topKAvg"] = top_k_avgs
df = df[df["topKAvg"] > qth_percentile]
filtered_df = pd.merge(df, play_ser, how="inner", on="courseId")
print(f"filtered by top {K} averages in addition to filter-playable's filters")
print(filtered_df.info())

filtered_df["courseId"].to_json(OUTPUT_FILE, orient="records", indent=2)
print(f"saved to json: available at {OUTPUT_FILE}")
