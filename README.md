# Synthesis AI Research Paper Generator

## 🎓 About

An AI-powered research paper generation platform with RAG (Retrieval Augmented Generation) system that helps researchers, students, and academics create high-quality research papers while maintaining academic integrity.

## ✨ Features

- **Vectorless RAG (BM25 PageIndex)**: Exact fact retrieval across 50+ papers
- **Fine-Tuned AI Writing**: Local Qwen LLM integration for expert section generation
- **Interactive Chat Flow**: Ideate topics and select base papers iteratively
- **Live Editors**: Real-time dual-pane LaTeX and Google Colab ML Code editors
- **Systematic Export**: One-click ZIP export containing code, papers, and formatted LaTeX
- **Similarity Detection**: Check novelty of research ideas
- **Zero Cloud Costs**: 100% local deployment

## 🏗️ Architecture

```
├── Backend (FastAPI + Python)
│   ├── Vectorless RAG System (BM25 PageIndex)
│   ├── LLM Integration (Fine-tuned Qwen)
│   ├── Multi-source ingestion (arXiv, Semantic Scholar, PubMed, CORE)
│   └── RESTful API
│
├── Frontend (React + Vite)
│   ├── Paper Editor (TipTap)
│   ├── Admin Dashboard
│   └── Real-time UI updates
│
└── Data
    ├── vectorless_store.json (BM25 Index)
    ├── SQLite (Metadata)
    └── User uploads
```

## 📋 Prerequisites

- **Python 3.10+**
- **Node.js 18+**
- **Ollama** - [Install from ollama.ai](https://ollama.ai)
- **16GB RAM** (recommended) or 8GB minimum
- **50GB+ free storage** for RAG database

## 🚀 Quick Start

### 1. Install Ollama & Pull Qwen Model

```bash
# Download Ollama from https://ollama.ai
# Then pull the Qwen model for improved factuality:
ollama pull qwen2.5:7b

# Or if you have more VRAM:
ollama pull qwen2.5:14b
```

### 2. Clone & Setup Backend

```bash
cd "d:\Synthesis- Ai Research Paper Generator"

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r backend\requirements.txt
```

### 3. Setup Frontend

```bash
cd frontend
npm install
```

### 4. Initialize RAG Database (One-Time)

```bash
# This will fetch 2000+ research papers (4-6 hours)
cd backend
python scripts\bulk_ingest.py --total-target 2000
```

### 5. Run the Application

**Terminal 1** - Backend (FastAPI):
```bash
cd backend
uvicorn main:app --reload --port 8000
```

**Terminal 2** - Frontend (React):
```bash
cd frontend
npm run dev
```

**Terminal 3** - Daily Ingestion (Optional):
```bash
cd backend
python scripts\daily_ingest.py
```

### 6. Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Admin Dashboard**: http://localhost:5173/admin

## 📊 System Requirements

### Minimum
- CPU: 4 cores
- RAM: 8GB
- Storage: 20GB free
- GPU: Not required (CPU inference)

### Recommended
- CPU: 8+ cores
- RAM: 16GB+
- Storage: 50GB+ SSD
- GPU: NVIDIA with 6GB+ VRAM (for faster generation)

## 📚 Documentation

- [Implementation Plan](./docs/implementation_plan.md)
- [API Documentation](http://localhost:8000/docs) (when running)
- [Continuous Ingestion Guide](./docs/continuous_ingestion_summary.md)
- [SRS Document](./SRS.txt)

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Web framework
- **rank_bm25** - Vectorless Search (PageIndex)
- **Ollama** - Local LLM (Qwen)
- **SQLite** - Metadata storage
- **LangChain** - LLM orchestration

### Frontend
- **React** - UI framework
- **Vite** - Build tool
- **TailwindCSS + DaisyUI** - Styling
- **TipTap** - Rich text editor
- **Axios** - HTTP client
- **Zustand** - State management

### Data Sources (All Free)
- **arXiv** - Computer science, physics, math
- **Semantic Scholar** - Multi-disciplinary
- **PubMed Central** - Biomedical sciences
- **CORE** - Open-access aggregator

## 📖 Usage Examples

### Create a New Research Paper

1. Navigate to Dashboard
2. Click "New Paper"
3. Enter research topic and domain
4. System suggests similar papers (RAG)
5. Generate sections with AI assistance
6. Add citations
7. Export to PDF/DOCX/LaTeX

### Check Research Novelty

```bash
curl -X POST http://localhost:8000/api/discovery/novelty \
  -H "Content-Type: application/json" \
  -d '{"research_idea": "AI-based cryptocurrency prediction using sentiment analysis"}'
```

### Manual Paper Ingestion

```bash
curl -X POST http://localhost:8000/api/admin/ingest/manual \
  -H "Content-Type: application/json" \
  -d '{
    "source": "arxiv",
    "query": "quantum computing",
    "max_results": 100
  }'
```

## 🔧 Configuration

Edit `backend/config.py` to customize:

```python
# LLM Configuration
OLLAMA_MODEL = "qwen2.5:7b"
OLLAMA_BASE_URL = "http://localhost:11434"

# Vector Database
# Using Vectorless RAG (BM25) fallback storage

# Ingestion
DAILY_INGESTION_TIME = "02:00"
PAPERS_PER_NICHE = 40
```

## 📈 Performance

### Generation Times
- **Without GPU**: 10-45 seconds per section
- **With GPU (NVIDIA)**: 3-10 seconds per section
- **Embedding generation**: 1-3 seconds per 1000 papers

### Storage Growth
- **Per 1000 papers**: ~1-1.5 GB
- **Monthly** (50 papers/day): ~1.5-2 GB
- **Annual**: ~18-24 GB

## 🤝 Contributing

This is a local-first, zero-budget project. Contributions welcome!

## 📝 License

MIT License - Feel free to use and modify

## 🙏 Acknowledgments

- **Ollama** - Local LLM inference
- **ChromaDB** - Vector database
- **Hugging Face** - sentence-transformers
- **arXiv, Semantic Scholar, PubMed, CORE** - Research paper APIs

## 🐛 Troubleshooting

### Ollama not running
```bash
# Check if Ollama is running
ollama list

# Start Ollama service (runs in background)
ollama serve
```

### Low on storage
```bash
# View RAG database size
python backend/scripts/check_storage.py

# Remove old papers (optional)
python backend/scripts/cleanup_old_papers.py --older-than 2years
```

### Slow generation
```bash
# Use smaller model
ollama pull tinyllama:1.1b

# Update config.py
OLLAMA_MODEL = "tinyllama:1.1b"
```

## 📧 Support

For issues, questions, or feedback, please open an issue on GitHub or contact the development team.

---

**Built with ❤️ for researchers, by researchers.**
