from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.ollama import OllamaEmbedding
from pathlib import Path
import os

# Set up paths
DATA_DIR = "data"
STORAGE_DIR = "storage"

if not os.path.exists(DATA_DIR):
    raise FileNotFoundError(f"Data directory '{DATA_DIR}' does not exist.")

print("Loading documents...")
documents = SimpleDirectoryReader(DATA_DIR).load_data()
print(f"Loaded {len(documents)} documents.")

print("Building embedding model (Ollama - mxbai-embed-large)...")
embed_model = OllamaEmbedding(model_name="mxbai-embed-large")

print("Creating index...")
index = VectorStoreIndex.from_documents(documents, embed_model=embed_model)

print(f"Persisting index to {STORAGE_DIR}...")
index.storage_context.persist(persist_dir=STORAGE_DIR)
print("Done.")
