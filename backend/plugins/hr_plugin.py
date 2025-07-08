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

# Define paths
DATA_DIR = "/app/data"
STORAGE_DIR = "/app/storage"

# Set Ollama server URL (important: host.docker.internal allows container to reach Ollama on host)
OLLAMA_HOST = "http://ollama:11434"

# Set global model configuration
Settings.llm = Ollama(model="llama3", base_url=OLLAMA_HOST,request_timeout=60)
Settings.embed_model = OllamaEmbedding(model_name="mxbai-embed-large", base_url=OLLAMA_HOST, request_timeout=60)

# Load or create index
if os.path.exists(STORAGE_DIR) and os.listdir(STORAGE_DIR):
    storage_context = StorageContext.from_defaults(persist_dir=STORAGE_DIR)
    index = load_index_from_storage(storage_context)
else:
    documents = SimpleDirectoryReader(DATA_DIR).load_data()
    index = VectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir=STORAGE_DIR)

# Create query engine
query_engine = index.as_query_engine()

# Main function
def main(query: str) -> str:
    response = query_engine.query(query)
    return str(response)
