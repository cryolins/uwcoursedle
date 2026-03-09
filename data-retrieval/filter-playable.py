import pandas as pd
import re

# constants
INPUT_FILE = "first-pass.json"
SUBJECTS_FILE = "ucal-subjects.json"
OUTPUT_FILE = "courses-source.json"
FILTER_KEYWORDS = ["special ", "seminar", "capstone", "reading", "ensemble", "thesis",
                   "project", "research", "session", "work-term", "directed", "co-operative",
                   "essay", "abroad", "independent", "production participation", "field course",
                   "apprenticeship", "practicum", "proposal"]
                # "topics" is filtered separately
KW_REGEX = "|".join(FILTER_KEYWORDS)
FILTER_EXCEPTIONS = ["SCI211", "BME587", "BME588", "BME589", "ECON361", "ECON457", "AE400", "COMM431",
                     "ECE198", "GBDA201", "GBDA301", "GBDA202", "GBDA302", "GBDA204", "PHYS263",
                     "THPERF400", "THPERF248", "GEOG481", "PLAN481", "PD5", "COMMST302", "DAC303"
                     ] #notable exceptions to the filter that can be kept

# filter and view function
# just a function to save down queries I used for analyzing the dataframe
def filter_and_view(df: pd.DataFrame):
    """ print(df.dtypes) """
    
    # check for no laurier courses
    """ print(df[df["catalogNumber"].str.endswith("W")]) """

    # check out which descriptions have another course name in them
    """ course_in_desc_df = df[df["description"].str.contains("[0-9]{3}[A-Z]{1,2}")]
    course_in_desc_df.to_json("course-desc-test.json", orient="records", indent=2) """
    # TODO: substitute short descriptions by replacing those with the referenced course's description
    
    # check filters worked
    """ df_check = df[(df["title"].str.lower().str.contains(KW_REGEX, regex=True))]
    df_check.to_json("check-course.json", orient="records", indent=2) """

    return

# a pipeline to find keywords that pop up in courses with redundant/overlapping descs or titles
def find_bad_kws(df: pd.DataFrame):
    # check duplicate description courses by grouping by description
    courses_by_desc_df = df.groupby("description").agg(
        count=("catalogNumber", "count"),
        titles=("title", list),
        subjects=("subjectCode", list),
        ids=("courseId", "/".join)
    )
    courses_by_desc_df.sort_values("count", ascending=False, inplace=True)
    courses_by_desc_df = courses_by_desc_df[courses_by_desc_df["count"] > 1]
    cbd_dup_subs_df = courses_by_desc_df[courses_by_desc_df["subjects"].apply(len) != courses_by_desc_df["subjects"].apply(lambda x: len(set(x)))]
    # print(cbd_dup_subs_df.head(50))
    
    # processing word counts in titles
    df_word_counts = df["title"].str.split().explode().value_counts()
    df_word_counts.rename("allCount", inplace=True)
    cbdds_word_counts = cbd_dup_subs_df["titles"].explode().str.split().explode().value_counts()
    cbdds_word_counts.rename_axis("word", inplace=True)
    cbdds_word_counts.rename("cbddsCount", inplace=True)

    word_counts_df = pd.merge(cbdds_word_counts, df_word_counts, how="inner", left_index=True, right_index=True)
    word_counts_df = word_counts_df[(word_counts_df.index.str.len() > 4) # eliminate common english words
                                    & (word_counts_df["cbddsCount"] > 1) 
                                    & (word_counts_df["allCount"] > 1)]
    word_counts_df["cbddsProportion"] = word_counts_df["cbddsCount"] / word_counts_df["allCount"]
    word_counts_df.sort_values("cbddsCount", ascending=False, inplace=True)
    print(word_counts_df[word_counts_df["cbddsCount"] >= 4].to_string())

    return

df = pd.read_json(INPUT_FILE)
sub_df = pd.read_json(SUBJECTS_FILE)

# print(df.dtypes)
# print(sub_df.dtypes)

# keep courses where subject code is found in undergrad calendar
df = df.merge(sub_df, on="subjectCode", how="inner")
print("merged with undergraduate calendar subjects")

# filters out transfer credits and those 1X000 courses, 
# though we leave courses that use X to denote a subtype, like ENGL108X, alone
df = df[~df["catalogNumber"].str.contains("X") | df["catalogNumber"].str.fullmatch("[0-9]{3}X")]
print("filtered transfer/X courses")

# filter out empty string courses since those can't be embedded well
df = df[~(df["description"] == "")]
print("filtered empty description courses")

# filter out bad keywords
df = df[(~df["title"].str.lower().str.contains(KW_REGEX, regex=True))
        | (df["title"].str.lower().str.contains("topics")) # filter topics later
        | (df["courseId"].isin(FILTER_EXCEPTIONS))]
print("filtered undesirable keywords")

# topics filter:
""" 
either: does not contain "topics"
OR: >=300 chars description (good sweet spot)
OR: has the word fragment "includ" and has a unique description
OR: in filter exceptions 
AND: does not contain "seminar" or "independent" or "directed" (those have lame descriptions ;)
"""
desc_count = df["description"].value_counts()
desc_count = desc_count.index[desc_count > 1]

df = df[(~df["title"].str.lower().str.contains("topics"))
        | (((df["description"].str.len() >= 300)
            | ((df["description"].str.contains("includ"))
                & (~df["description"].isin(desc_count)))
            | (df["courseId"].isin(FILTER_EXCEPTIONS)))
           & (~df["title"].str.lower().str.contains("seminar|independent|directed", regex=True))
          )]
print("filtered by \"topics\" keyword")

# in preparation for replacing course codes in descriptions, 
# ensure course codes separated by a space aren't anymore
COURSE_ID_PATTERN = re.compile(r"([A-Z]{2,}) ?([0-9]{1,3}[A-Z]?)")
COURSE_ID_PATTERN_UNGROUPED = re.compile(r"[A-Z]{2,} ?[0-9]{1,3}[A-Z]?")
df["description"] = df["description"].str.replace(
    COURSE_ID_PATTERN, r"\1\2", regex=True
)
print("cleaned whitespace between subject codes in descriptions")

# function to expand description
code_to_desc = dict(zip(df["courseId"], df["description"]))
def replace_ids(row):
    desc = row["description"]
    courseId = row["courseId"]

    if(len(desc) > 100):
        return desc
    def replaceFunc(match):
        id_to_replace = match.group(0)
        if(id_to_replace == courseId):
            return id_to_replace
        
        expand_text = code_to_desc.get(id_to_replace)
        if(expand_text is None):
            return id_to_replace
        return f"{id_to_replace}: ({expand_text})"

    return COURSE_ID_PATTERN_UNGROUPED.sub(replaceFunc, desc)

# saving down courseIds of those that need to be changed to compare
""" course_desc = df[df["description"].str.contains(COURSE_ID_PATTERN, regex=True)].sort_values("description", key=lambda x: x.str.len())["courseId"]
 """
# updating descriptions to new version
df["description"] = df.apply(replace_ids, axis=1)

""" test = pd.merge(course_desc, df, how="inner", on="courseId")
test.to_json("course-desc-test.json", orient="records", indent=2) """

print("replaced select courseIds in descriptions with relevant course description")

# final collection: group by title and description
# drop catalog number
collected_df = df.groupby(["title", "description"]).agg({
    "courseId": "/".join,
    "subjectName": list,
    "subjectCode": list
}).reset_index().sort_values("courseId")

# rename columss
collected_df.rename(columns={"subjectCode": "subjectCodes", "subjectName": "subjectNames"}, inplace=True)

print("collected by title & description")

# save to json
collected_df.to_json(OUTPUT_FILE, orient="records", indent=2)
print(f"saved to json: available at {OUTPUT_FILE}")

print("final step done!\n")
collected_df.info()
