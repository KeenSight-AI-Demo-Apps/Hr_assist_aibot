# 🧠 HR Assist AI - Chatbot for HR Benefits FAQs  
This project is a local-first, privacy-friendly HR chatbot designed to handle employee questions about health benefits and HR policies using company-specific documents. It uses Retrieval-Augmented Generation (RAG) powered by LlamaIndex, Ollama, and OpenWebUI, all running inside Docker.

---

## 📁 Project Structure  
```
hr_assist_ai/  
├── backend/  
│   ├── plugins/  
│   │   └── hr_plugin.py         # Core logic for RAG-based Q&A using LlamaIndex + Ollama  
│   └── custom_apps/  
│       └── data_loader.py       # Loads CSV documents into vector store  
├── data/  
│   └── hr_benefits.csv          # HR Q&A dataset  
├── storage/                     # Vector index & docstore persisted here  
├── docker-compose.yml           # Runs Ollama + OpenWebUI  
├── .env                         # (Optional) Environment variables  
├── README.md                    # Project documentation  
```

---

## 🛠️ Technologies Used  
| **Purpose**                | **Tool**                | **Description**                                    |
|---------------------------|-------------------------|----------------------------------------------------|
| LLM Backend               | Ollama + llama3         | Local large language model                         |
| Embeddings                | mxbai-embed-large       | Local embedding model                              |
| RAG & Indexing            | LlamaIndex (0.12.47)    | Handles document parsing and vector store          |
| Chat Interface            | OpenWebUI               | User-facing intranet chatbot                       |
| Containerization          | Docker + docker-compose | To run everything locally                          |
| Programming Language      | Python 3.11             | Core application logic                             |

---

## 🔁 Setup & Installation  

**1. Clone the Repo**  
```bash
git clone https://github.com/yourusername/hr_assist_ai.git  
cd hr_assist_ai  
```

**2. Prepare Documents**  
Put your HR documents (e.g., FAQs, benefit plans) inside the `data/` folder. Start with `hr_benefits.csv`.

**3. Install & Pull Ollama Models**  
Install Ollama and pull required models:  
```bash
ollama pull llama3  
ollama pull mxbai-embed-large  
```

**4. Start Docker Containers**  
```bash
docker-compose up -d --build  
```  
This launches:  
- Ollama at `http://localhost:11434`  
- OpenWebUI at `http://localhost:3000`

**5. (Optional) Rebuild Containers**  
If you change anything in `docker-compose.yml` or `Dockerfile`:  
```bash
docker-compose down -v  
docker-compose up -d --build  
```

---

## 🧠 How It Works  

- **Data Ingestion**: `data_loader.py` loads CSVs and persists them to vector index using `mxbai-embed-large` embeddings.  
- **Query Processing**: `hr_plugin.py` loads the index and runs a retrieval + LLM-based response pipeline.  
- **User Interface**: OpenWebUI provides a chat interface. You connect it with `hr_plugin.chat(query)` so user questions are answered from your HR data.

---

## 🧪 Running in OpenWebUI (In-Browser)  

1. Open `http://localhost:3000`  
2. Start a new chat  
3. Ask questions like:  
   > What health benefits do employees receive?

⚠️ If RAG is not working in the browser yet, test it using this (inside the container):  
```bash
docker exec -it hr_assist_ai-open-webui sh  
export PYTHONPATH=/app  
python3  
>>> from backend.plugins.hr_plugin import main 
>>> main("What are health benefits?")  
```

---

## 🔍 Known Issues & Fixes  

✅ **Fixed**  
- `llama_index` module errors by using correct version (0.12.47)  
- Ensured Ollama and OpenWebUI both access models locally  
- Integrated `mxbai-embed-large` for embeddings  
- Container networking issues fixed by aligning Docker and Ollama ports  

❗**Pending**  
- Ensuring OpenWebUI can call `hr_plugin.py` backend directly  
- Confirming RAG answers display in UI not just via CLI  

---

## 🚀 What's Next  

- Integrate file upload into OpenWebUI chat  
- Allow multiple document types (PDF, DOCX)  
- Add chat history per employee/user  
- Add HR policy documents, SPDs, and medical plan PDFs  

---

## 🤝 Contribution  
Pull requests welcome! This is built for local HR teams wanting private, document-grounded AI without cloud APIs.