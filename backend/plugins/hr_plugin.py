"""
---
name: HR Assistant
description: HR chatbot plugin answering questions from hr_benefits data via RAG
author: HR Team
version: 1.0.0

requirements:
  - llama-index
  - llama-index-llms-ollama
  - llama-index-embeddings-ollama

functions:
  - name: search_hr_benefits
    description: Search HR benefits and policies information
    parameters:
      type: object
      properties:
        query:
          type: string
          description: The HR-related question to search for
      required:
        - query
---
"""

import os
from typing import Dict, Any
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
    request_timeout=300,
)

Settings.embed_model = OllamaEmbedding(
    model_name="mxbai-embed-large",
    base_url=OLLAMA_HOST,
    request_timeout=160
)

# ------------------- Index Initialization -------------------
query_engine = None

def initialize_index():
    global query_engine
    try:
        # Check if index already exists
        if os.path.exists(STORAGE_DIR) and os.listdir(STORAGE_DIR):
            storage_context = StorageContext.from_defaults(persist_dir=STORAGE_DIR)
            index = load_index_from_storage(storage_context)
        else:
            documents = SimpleDirectoryReader(DATA_DIR).load_data()
            index = VectorStoreIndex.from_documents(documents)
            index.storage_context.persist(persist_dir=STORAGE_DIR)
        
        query_engine = index.as_query_engine()
        return True
    except Exception as e:
        print(f"Error initializing index: {e}")
        return False

# Initialize on import
initialize_index()

# ------------------- Plugin Functions -------------------

def search_hr_benefits(query: str) -> str:
    """Search HR benefits and policies information."""
    global query_engine
    
    if query_engine is None:
        if not initialize_index():
            return "Error: HR system is not available. Please try again later."
    
    try:
        response = query_engine.query(query)
        return str(response)
    except Exception as e:
        return f"Error searching HR information: {e}"

# ------------------- Main Function (Legacy Support) -------------------

def main(query: str) -> str:
    """Main function for backwards compatibility."""
    return search_hr_benefits(query)

# ------------------- Event Handlers -------------------

def on_startup():
    """Called when the plugin is loaded."""
    print("HR Assistant plugin loaded successfully!")
    return initialize_index()

def on_shutdown():
    """Called when the plugin is unloaded."""
    print("HR Assistant plugin shutting down...")

def on_valves_updated():
    """Called when plugin configuration is updated."""
    global query_engine
    query_engine = None
    return initialize_index()