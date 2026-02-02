import os
import json
from pathlib import Path
from dotenv import load_dotenv
from langchain_huggingface.embeddings import HuggingFaceEndpointEmbeddings

# get huggingface and model
load_dotenv()
hf_key = os.getenv("HUGGINGFACE_API_KEY")
embeddingsModel = HuggingFaceEndpointEmbeddings(
        model="sentence-transformers/all-MiniLM-L6-v2", huggingfacehub_api_token=hf_key)

# get json source and target file locations
rootPath = Path(__file__).resolve().parents[1]
sourcePath = rootPath / "courses-source.json"
targetPath = rootPath / "courses.json"

# storage structures
documents = []
output = {}

# get data from json
with open(sourcePath) as fi:
    data = json.load(fi)
    for course in data:
        documents.append(course["title"] + ": " + course["description"])

# get embeddings and combine them with the source data
doc_embeddings = embeddingsModel.embed_documents(documents)
for i,course in enumerate(data):
    course["vector"] = doc_embeddings[i]

with open(targetPath, "w") as fo:
    json.dump(data, fo, indent=2)
