# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "chromadb==0.6.3",
# ]
# ///

import chromadb

chroma_client = chromadb.Client()

collection = chroma_client.create_collection(name="my_collection")

collection.add(
    documents=[
        "This is a document about pineapple",
        "This is a document about oranges",
    ],
    ids=["id3", "id5"],
    metadatas=[{"fruit": ["pineapple"]}, {"fruit": "orange"}],
)
