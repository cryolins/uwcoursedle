import os
import json
from pathlib import Path
from dotenv import load_dotenv
from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings

# get huggingface and model
load_dotenv()
hf_key = os.getenv("HUGGINGFACE_API_KEY")
embeddings_model = HuggingFaceEndpointEmbeddings(
        model="sentence-transformers/all-MiniLM-L6-v2", huggingfacehub_api_token=hf_key)

# get json source and target file locations
root_path = Path(__file__).resolve().parents[1]
SOURCE_PATH = "courses-source.json"
TARGET_PATH = root_path / "frontend" / "src" / "lib" / "courses.json"

# storage structures
documents = []
output = {}

# get data from json
with open(SOURCE_PATH) as fi:
    data = json.load(fi)
    for course in data:
        documents.append(course["title"] + ": " + course["description"])

# get embeddings and combine them with the source data
# also delete descriptions as they are no longer needed
doc_embeddings = embeddings_model.embed_documents(documents)
for i,course in enumerate(data):
    course["vector"] = doc_embeddings[i]
    del course["description"]

with open(TARGET_PATH, "w") as fo:
    json.dump(data, fo, indent=2)
