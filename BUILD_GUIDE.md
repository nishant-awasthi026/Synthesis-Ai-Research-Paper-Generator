# Synthesis AI Research Paper Generator - Build Guide

## Project Status

✅ **Phase 1 - Complete**: Project structure and configuration
- Directory structure created
- Configuration files ready (.env, requirements.txt)
- Database models defined
- Main FastAPI app skeleton created
- Setup automation script created

## What's Been Created

### Configuration & Setup (✅ Complete)
1. `README.md` - Comprehensive documentation
2. `.env.example` - Environment variables template
3. `.gitignore` - Git ignore rules
4. `backend/requirements.txt` - Python dependencies
5. `backend/config.py` - Application configuration
6. `backend/database/models.py` - Database schema
7. `backend/database/database.py` - Database connection
8. `backend/main.py` - FastAPI application
9. `backend/init_db.py` - Database initialization
10. `scripts/setup.py` - Automated setup script

### Directory Structure
```
Synthesis- Ai Research Paper Generator/
├── backend/
│   ├── api/routes/          # API endpoints (to be created)
│   ├── database/            # ✅ Database models & connection
│   ├── rag/                 # RAG system components (to be created)
│   ├── llm/                 # LLM integration (to be created)
│   ├── export/              # Export functionality (to be created)
│   ├── scripts/             # Ingestion scripts (to be created)
│   ├── config.py            # ✅ Configuration
│   ├── main.py              # ✅ FastAPI app
│   └── requirements.txt     # ✅ Dependencies
├── frontend/                # React app (to be created)
├── data/                    # ✅ Data storage directories
├── scripts/setup.py         # ✅ Setup automation
└── README.md                # ✅ Documentation
```

## Quick Start (Use This First!)

### Option 1: Automated Setup (Recommended)

```bash
# Navigate to project directory
cd "d:\Synthesis- Ai Research Paper Generator"

# Run automated setup
python scripts\setup.py
```

This will:
- Check Ollama installation
- Create .env file
- Set up Python virtual environment
- Install all dependencies
- Initialize database
- Install frontend packages

### Option 2: Manual Setup

```bash
# 1. Install Ollama
# Download from https://ollama.ai
ollama pull llama3.1:8b

# 2. Create .env file
copy .env.example .env

# 3. Create virtual environment
python -m venv venv
venv\Scripts\activate

# 4. Install Python dependencies
pip install -r backend\requirements.txt

# 5. Initialize database
python backend\init_db.py
```

## Building the Remaining Components

### Phase 2: RAG System (Next Step)

You need to create these files in `backend/rag/`:

#### 1. Vector Store (`backend/rag/vector_store.py`)
```python
import chromadb
from sentence_transformers import SentenceTransformer
from backend.config import settings

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=settings.CHROMADB_PERSIST_DIR)
        self.collection = self.client.get_or_create_collection(settings.COLLECTION_NAME)
        self.embedding_model = SentenceTransformer(settings.EMBEDDING_MODEL)
    
    def add_papers(self, papers):
        """Add papers to vector store"""
        # Implementation here
        pass
    
    def search_similar(self, query, top_k=10):
        """Search for similar papers"""
        # Implementation here
        pass
```

See `implementation_plan.md` for complete code.

#### 2. Document Loader (`backend/rag/document_loader.py`)

See implementation_plan.md for complete multi-source loader code.

#### 3. Niche Classifier (`backend/rag/niche_classifier.py`)

See implementation_plan.md for complete AI-based classifier.

### Phase 3: LLM Integration

Create `backend/llm/ollama_client.py` - See implementation_plan.md

### Phase 4: API Routes

Create in `backend/api/routes/`:
- `papers.py` - Paper CRUD
- `discovery.py` - Similarity search
- `citations.py` - Citation management
- `admin.py` - Admin dashboard
- `auth.py` - Authentication

### Phase 5: Frontend

Initialize React app:
```bash
cd frontend
npm create vite@latest . -- --template react
npm install
```

Then install dependencies and create components as per implementation_plan.md.

## Using the Full Implementation Plan

**All the complete code is in**: `implementation_plan.md` (in the artifacts folder)

That document contains:
- ✅ Complete RAG system code
- ✅ All API routes with full implementation
- ✅ Frontend components
- ✅ Ingestion scripts
- ✅ Export functionality
- ✅ Testing examples

## Recommended Build Order

1. **✅ Phase 1 DONE**: Project setup (completed)
2. **Phase 2** (Week 1-2): RAG System
   - Copy code from implementation_plan.md
   - Create `backend/rag/vector_store.py`
   - Create `backend/rag/document_loader.py`
   - Create `backend/rag/niche_classifier.py`
   - Create `backend/rag/embeddings.py`
   - Test with sample papers

3. **Phase 3** (Week 2): LLM Integration
   - Create `backend/llm/ollama_client.py`
   - Create `backend/llm/prompts.py`
   - Create `backend/llm/generator.py`
   - Test generation

4. **Phase 4** (Week 3): APIs
   - Create all route files
   - Test endpoints with Postman/Thunder Client

5. **Phase 5** (Week 4-5): Frontend
   - Initialize Vite + React
   - Create components
   - Connect to backend

6. **Phase 6** (Week 6): Ingestion & Export
   - Create bulk ingestion script
   - Create daily ingestion  
   - Create export generators

## Testing the Current Setup

### Test 1: Database
```bash
python backend\init_db.py
```

Expected: "✅ Database initialization complete!"

### Test 2: FastAPI Server
```bash
cd backend
python main.py
```

Expected: Server running at http://localhost:8000

Visit http://localhost:8000/docs to see API documentation.

### Test 3: Check Ollama
```bash
ollama list
```

Expected: Model list (should include llama3.1:8b or mistral:7b)

## Development Workflow

### Daily Development
```bash
# 1. Activate virtual environment
venv\Scripts\activate

# 2. Start backend (Terminal 1)
cd backend
uvicorn main:app --reload

# 3. Start frontend (Terminal 2 - after it's created)
cd frontend
npm run dev

# 4. Start daily ingestion (Terminal 3 - optional)
python backend/scripts/daily_ingest.py
```

### Adding New Features

1. Check `implementation_plan.md` for complete code
2. Copy relevant sections to your files
3. Test the feature
4. Update task.md to track progress

## Need Help?

### Common Issues

**Issue**: "Ollama not found"
**Solution**: Install from https://ollama.ai and run `ollama pull llama3.1:8b`

**Issue**: "Module not found"
**Solution**: Make sure virtual environment is activated and dependencies are installed

**Issue**: "Database error"
**Solution**: Run `python backend/init_db.py` to create tables

### Reference Documents

1. **implementation_plan.md** - Complete code for all components
2. **continuous_ingestion_summary.md** - RAG ingestion details
3. **SRS.txt** - Original requirements
4. **README.md** - User guide

## Progress Tracking

Use `task.md` (in artifacts) to track your progress through each phase.

Current status: **Phase 1 Complete ✅**

Next: Build RAG system (Phase 2) using code from implementation_plan.md

## Quick Copy-Paste Commands

```bash
# Full setup from scratch
cd "d:\Synthesis- Ai Research Paper Generator"
python scripts\setup.py

# After setup, run the app
venv\Scripts\activate
cd backend
python main.py

# Or use uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## Final Notes

This starter package gives you:
- ✅ Working project structure
- ✅ Database setup
- ✅ Basic API server
- ✅ Configuration system
- ✅ Automated setup script

To complete the project:
1. Copy code from `implementation_plan.md` (in artifacts)
2. Create remaining Python files in `backend/`
3. Set up frontend with Vite
4. Run initial data ingestion
5. Test and iterate

**Estimated time to complete**: 4-6 weeks following the implementation plan

**Total cost**: $0 (100% open-source)

Good luck building! 🚀
