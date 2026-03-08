import requests
import os
from dotenv import load_dotenv
import pandas as pd
from io import StringIO

# consts
TERM_CODES = ["1259", "1261", "1265"] # termcodes for fall, winter, and spring of 2025-2026
OUTPUT_FILE = "first-pass.json"

# get api key
load_dotenv()
UW_API_KEY = os.getenv("UW_API_KEY")

termDfs: list[pd.DataFrame] = []

for code in TERM_CODES:
    url = f"https://openapi.data.uwaterloo.ca/v3/Courses/{code}"
    termResponse = requests.get(url, headers={ "x-api-key" : UW_API_KEY })

    if(termResponse.status_code == 200):
        termDf = pd.read_json(StringIO(termResponse.text))
        termDfs.append(termDf)
    else:
        raise Exception(f"failed to load term {code}")
    
print("fetched all 3 terms successfully!")

df = pd.concat(termDfs, ignore_index=True)

# keep only relevant columns
df = df[["associatedAcademicCareer", "subjectCode", "catalogNumber", "title", "description"]]

# drop duplicate course codes (likely due to duplicate courses over 3 terms)
df.drop_duplicates(subset=["subjectCode", "catalogNumber"], keep="last", inplace=True)

# filter out WLU courses and non undergraduate courses
df = df[~df["catalogNumber"].str.endswith("W") & (df["associatedAcademicCareer"] == "UG")]

# remove associatedAcademicCareer as it is no longer needed
df.drop(["associatedAcademicCareer"], axis="columns", inplace=True)

# make a new column combining subject and catalog number
df["courseId"] = df["subjectCode"] + df["catalogNumber"]

# sort by the column
df.sort_values("courseId", inplace=True)

# output to a json
df.to_json(OUTPUT_FILE, orient="records", indent=2)

# completion message
print(f"first pass filtering complete! resulting json found at {OUTPUT_FILE}")