import os
import json
from pathlib import Path
import math

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
jsonPath = rootPath / "frontend" / "src" / "lib" / "courses.json"

# get data from json
with open(jsonPath) as fi:
    data = json.load(fi)
    for i in range(len(data)):
        for j in range(i, len(data)):
            print(data[i]["courseId"], data[j]["courseId"], round(sim_scale(cos_sim(data[i]["vector"], data[j]["vector"])), 3))