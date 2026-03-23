# 🎓 Synthesis AI Research Paper Generator

## Quick Commands Reference

### Start the Server
```bash
# Activate virtual environment
.\venv\Scripts\activate

# Start the backend
python start_server.py

# Server will run at: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Test the System
```bash
# Run automated API tests
python demo_api.py

# Add sample research papers (10 famous AI papers)
python add_sample_papers.py

# Run system tests
python test_system.py
```

### Frontend Setup (Optional)
```bash
cd frontend
npm install
npm run dev

# Visit: http://localhost:5173
```

---

## 📁 Project Structure

```
Synthesis- Ai Research Paper Generator/
├── backend/                    # FastAPI Backend
│   ├── api/routes/            # API endpoints
│   │   ├── discovery.py       # Similarity & novelty
│   │   ├── generate.py        # Content generation
│   │   └── system.py          # Health & config
│   ├── database/              # Database layer
│   │   ├── models.py          # SQLAlchemy models
│   │   └── database.py        # DB connection
│   ├── rag/                   # RAG system
│   │   ├── vector_store.py    # ChromaDB integration
│   │   └── simple_vector_store.py  # Fallback
│   ├── llm/                   # LLM integration
│   │   ├── ollama_client.py   # Ollama API
│   │   ├── prompts.py         # Templates
│   │   └── generator.py       # RAG-enhanced generation
│   ├── config.py              # Configuration
│   ├── main.py                # FastAPI app
│   └── requirements.txt       # Dependencies
├── frontend/                  # React Frontend
│   ├── src/                   # Source files
│   ├── package.json           # NPM dependencies
│   └── vite.config.js         # Vite config
├── data/                      # Data storage
│   ├── chromadb/              # Vector database
│   ├── sqlite/                # SQLite DB
│   └── uploads/               # User uploads
├── start_server.py            # Server startup
├── demo_api.py                # API demo script
├── add_sample_papers.py       # Add sample papers
├── test_system.py             # System tests
├── README.md                  # This file
├── BUILD_GUIDE.md             # Build instructions
├── QUICKSTART.md              # Quick start guide
└── STATUS.md                  # Current status
```

---

## 🚀 What Works Right Now

### ✅ Without Ollama
- System health checks
- Configuration management
- Database operations
- Vector store (simple fallback)
- API documentation

### ⏸️ With Ollama (Install to Enable)
- Research topic generation
- Paper section generation (abstract, intro, etc.)
- RAG-enhanced writing
- LLM-powered features

---

## 🔧 Installation

### Prerequisites
- Python 3.10+
- Node.js 18+ (for frontend)
- 8GB+ RAM
- 10GB+ free storage

### Quick Setup
```bash
# 1. Install Python dependencies
python -m venv venv
.\venv\Scripts\activate
pip install -r backend\requirements.txt

# 2. (Optional) Install Ollama
# Download from: https://ollama.ai
ollama pull llama3.1:8b

# 3. Start server
python start_server.py
```

---

## 📚 API Endpoints

### Discovery (`/api/discovery`)
- `POST /similar` - Find similar papers
- `POST /novelty` - Calculate novelty score
- `GET /stats` - Database statistics

### Generation (`/api/generate`)
- `POST /section` - Generate paper section
- `POST /topics` - Generate topic ideas
- `GET /sections` - List section types

### System (`/api/system`)
- `GET /health` - Health check
- `GET /config` - Configuration

---

## 💡 Quick Examples

### Test the API
```bash
python demo_api.py
```

### Add Research Papers
```bash
python add_sample_papers.py
```

### Generate Research Topics (Requires Ollama)
```python
import requests

response = requests.post("http://localhost:8000/api/generate/topics", json={
    "domain": "Machine Learning",
    "keywords": ["optimization", "efficiency"],
    "user_interest": "Improving neural network training"
})

print(response.json())
```

### Check Research Novelty
```python
response = requests.post("http://localhost:8000/api/discovery/novelty", json={
    "research_idea": "Using quantum computing for AI training"
})

print(response.json())
```

---

## 📖 Documentation

| File | Description |
|------|-------------|
| `README.md` | This file - quick reference |
| `STATUS.md` | Current system status & usage |
| `QUICKSTART.md` | Quick start guide |
| `BUILD_GUIDE.md` | Complete build instructions |
| `implementation_plan.md` | Full implementation details (artifacts) |

---

## 🐛 Troubleshooting

**Server won't start?**
- Check if port 8000 is in use
- Activate virtual environment first
- Reinstall dependencies

**Ollama errors?**
- Install from https://ollama.ai
- Run: `ollama serve`
- Pull model: `ollama pull llama3.1:8b`

**Module not found?**
- Activate venv: `.\venv\Scripts\activate`
- Reinstall: `pip install -r backend\requirements.txt`

---

## 🎯 Next Steps

1. ✅ Server is running
2. ⏸️ Install Ollama for LLM features
3. ⏸️ Add research papers to RAG
4. ⏸️ Test all API endpoints
5. ⏸️ Build frontend components

---

## 📊 Status

- **Backend**: ✅ 75% Complete
- **Frontend**: ⏸️ 40% Complete
- **Documentation**: ✅ 100% Complete
- **Testing**: ✅ Scripts Ready

---

## 🙏 Built With

- FastAPI - Web framework
- SQLAlchemy - ORM
- Sentence Transformers - Embeddings
- Ollama - Local LLM
- React + Vite - Frontend
- Tailwind CSS - Styling

---

## 📞 Support

For detailed information, see:
- `BUILD_GUIDE.md` - Full build guide
- `STATUS.md` - How to use
- `implementation_plan.md` - All code (artifacts)
- API Docs: http://localhost:8000/docs

---

**Made with ❤️ for researchers, by researchers**

*Last Updated: February 1, 2026*
