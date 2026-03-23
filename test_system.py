"""
Quick test script to verify the setup
Run this after dependencies are installed
"""
import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

def test_imports():
    """Test that all modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from backend.config import settings
        print("✅ Config module loaded")
        print(f"   Project: {settings.PROJECT_NAME}")
        print(f"   Environment: {settings.ENV}")
    except Exception as e:
        print(f"❌ Config error: {e}")
        return False
    
    try:
        from backend.database.database import init_db
        print("✅ Database module loaded")
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False
    
    try:
        from backend.rag.vector_store import get_vector_store
        print("✅ RAG vector store module loaded")
    except Exception as e:
        print(f"❌ RAG error: {e}")
        return False
    
    try:
        from backend.llm.ollama_client import get_ollama_client
        print("✅ LLM client module loaded")
    except Exception as e:
        print(f"❌ LLM error: {e}")
        return False
    
    try:
        from backend.llm.generator import get_generator
        print("✅ Generator module loaded")
    except Exception as e:
        print(f"❌ Generator error: {e}")
        return False
    
    return True

def test_database():
    """Test database initialization"""
    print("\n🗄️  Testing database...")
    
    try:
        from backend.database.database import init_db
        init_db()
        print("✅ Database initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Database initialization error: {e}")
        return False

def test_ollama():
    """Test Ollama connection"""
    print("\n🤖 Testing Ollama...")
    
    try:
        from backend.llm.ollama_client import get_ollama_client
        
        client = get_ollama_client()
        health = client.check_health()
        
        if health.get("ollama_running"):
            print("✅ Ollama is running")
            if health.get("model_available"):
                print(f"✅ Model available: {health.get('model')}")
            else:
                print(f"⚠️  Model not found: {health.get('model')}")
                print(f"   Available models: {health.get('available_models', [])}")
        else:
            print("❌ Ollama is not running")
            print("   Please start Ollama and run: ollama pull llama3.1:8b")
        
        return health.get("ollama_running", False)
    except Exception as e:
        print(f"❌ Ollama error: {e}")
        return False

def test_vector_store():
    """Test vector store initialization"""
    print("\n📦 Testing vector store...")
    
    try:
        from backend.rag.vector_store import get_vector_store
        
        vs = get_vector_store()
        count = vs.count()
        print(f"✅ Vector store initialized")
        print(f"   Papers in database: {count}")
        return True
    except Exception as e:
        print(f"❌ Vector store error: {e}")
        return False

def main():
    print("="*60)
    print("  Synthesis AI Research Paper Generator - System Test")
    print("="*60)
    
    results = {
        "imports": test_imports(),
        "database": test_database(),
        "vector_store": test_vector_store(),
        "ollama": test_ollama()
    }
    
    print("\n" + "="*60)
    print("  Test Summary")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{test_name.capitalize():<20}: {status}")
    
    all_critical_passed = results["imports"] and results["database"] and results["vector_store"]
    
    print("\n" + "="*60)
    if all_critical_passed:
        print("✅ Core system is functional!")
        if not results["ollama"]:
            print("\n⚠️  Note: Ollama needs to be set up for LLM features")
            print("   1. Install Ollama from: https://ollama.ai")
            print("   2. Run: ollama pull llama3.1:8b")
        print("\n🚀 You can now start the backend:")
        print("   cd backend")
        print("   python main.py")
    else:
        print("❌ Some core components failed. Please check errors above.")
    print("="*60)

if __name__ == "__main__":
    main()
