"""
---
name: hr_plugin
description: HR chatbot plugin answering questions from hr_benefits data via RAG
parameters:
  - name: query
    type: string
    description: HR benefits question
---
"""

import os
from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
    StorageContext,
    load_index_from_storage,
    Settings,
)
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding

# ------------------- Configuration -------------------

# Set paths for data and storage (mounted into container)
DATA_DIR = "/app/data"
STORAGE_DIR = "/app/storage"

# Ollama server accessible from within Docker container
OLLAMA_HOST = "http://ollama:11434"

# ------------------- Model Settings -------------------

# Set global models
Settings.llm = Ollama(
    model="llama3",
    base_url=OLLAMA_HOST,
    request_timeout=300,  # extend timeout to avoid ReadTimeout
)

Settings.embed_model = OllamaEmbedding(
    model_name="mxbai-embed-large",
    base_url=OLLAMA_HOST,
    request_timeout=160
)

# ------------------- Index Initialization -------------------

# Check if index already exists
if os.path.exists(STORAGE_DIR) and os.listdir(STORAGE_DIR):
    storage_context = StorageContext.from_defaults(persist_dir=STORAGE_DIR)
    index = load_index_from_storage(storage_context)
else:
    documents = SimpleDirectoryReader(DATA_DIR).load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir=STORAGE_DIR)

# Create query engine once
query_engine = index.as_query_engine()

# ------------------- Query Function -------------------

def main(query: str) -> str:
    try:
        response = query_engine.query(query)
        return str(response)
    except Exception as e:
        return f"Error during query: {e}"
