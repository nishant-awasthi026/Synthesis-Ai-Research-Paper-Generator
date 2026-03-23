"""
Demo Script - Test the Synthesis API
Run this to see the API in action!
"""
import sys
sys.path.insert(0, ".")

import requests
import json
from pprint import pprint

BASE_URL = "http://localhost:8000"

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def test_root():
    """Test root endpoint"""
    print_header("TEST 1: Root Endpoint")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    pprint(response.json())

def test_health():
    """Test health check"""
    print_header("TEST 2: System Health Check")
    response = requests.get(f"{BASE_URL}/api/system/health")
    print(f"Status: {response.status_code}")
    pprint(response.json())

def test_config():
    """Test configuration"""
    print_header("TEST 3: System Configuration")
    response = requests.get(f"{BASE_URL}/api/system/config")
    print(f"Status: {response.status_code}")
    pprint(response.json())

def test_sections():
    """List available sections"""
    print_header("TEST 4: Available Section Types")
    response = requests.get(f"{BASE_URL}/api/generate/sections")
    print(f"Status: {response.status_code}")
    pprint(response.json())

def test_novelty():
    """Test novelty calculation"""
    print_header("TEST 5: Research Novelty Check")
    data = {
        "research_idea": "Using quantum computing to accelerate machine learning model training",
        "domain": "Quantum Computing & AI"
    }
    response = requests.post(f"{BASE_URL}/api/discovery/novelty", json=data)
    print(f"Status: {response.status_code}")
    pprint(response.json())

def test_topic_generation():
    """Test topic generation (requires Ollama)"""
    print_header("TEST 6: Generate Research Topics (Requires Ollama)")
    data = {
        "domain": "Artificial Intelligence",
        "keywords": ["machine learning", "optimization", "efficiency"],
        "user_interest": "I want to improve the training efficiency of large neural networks"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/generate/topics", json=data, timeout=30)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if "error" in result:
                print(f"❌ Error: {result['error']}")
                print("\n💡 Tip: Install Ollama from https://ollama.ai")
                print("   Then run: ollama pull llama3.1:8b")
            else:
                print("✅ Success!")
                pprint(result)
        else:
            print(f"❌ HTTP Error: {response.status_code}")
    except requests.exceptions.Timeout:
        print("⏱️  Request timed out - Ollama might be processing")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_section_generation():
    """Test section generation (requires Ollama)"""
    print_header("TEST 7: Generate Abstract (Requires Ollama)")
    data = {
        "section_type": "abstract",
        "title": "Efficient Neural Network Training Using Sparse Gradients",
        "domain": "Machine Learning",
        "problem": "Training large neural networks is computationally expensive and time-consuming",
        "methodology": "Novel sparse gradient descent algorithm with adaptive sparsity",
        "results": "50% reduction in training time with minimal accuracy loss",
        "use_rag": False  # Set to True when papers are added
    }
    
    try:
        response = requests.post(f"{BASE_URL}/api/generate/section", json=data, timeout=60)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            if "error" in result:
                print(f"❌ Error: {result['error']}")
                print("\n💡 Tip: Install Ollama from https://ollama.ai")
            else:
                print("✅ Success!")
                print(f"\nGenerated Content:\n{'-'*60}")
                print(result.get('content', 'No content'))
                print(f"{'-'*60}")
                print(f"\nTokens used: {result.get('tokens_used', 0)}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
    except requests.exceptions.Timeout:
        print("⏱️  Request timed out - Generation might take longer")
    except Exception as e:
        print(f"❌ Error: {e}")

def main():
    print("\n" + "="*60)
    print("  🎓 Synthesis AI Research Paper Generator - API Demo")
    print("="*60)
    print(f"\nTesting API at: {BASE_URL}")
    print("Press Ctrl+C to stop at any time\n")
    
    try:
        # Basic tests (always work)
        test_root()
        test_health()
        test_config()
        test_sections()
        test_novelty()
        
        # LLM tests (require Ollama)
        print("\n" + "="*60)
        print("  LLM-Powered Tests (Ollama Required)")
        print("="*60)
        
        test_topic_generation()
        test_section_generation()
        
        # Summary
        print("\n" + "="*60)
        print("  🎉 Demo Complete!")
        print("="*60)
        print("\n✅ Basic endpoints working!")
        print("💡 Install Ollama for full LLM features:")
        print("   1. Download from https://ollama.ai")
        print("   2. Run: ollama pull llama3.1:8b")
        print("   3. Restart this demo\n")
        print("📚 API Docs: http://localhost:8000/docs\n")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Demo stopped by user")
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to API server")
        print("   Make sure the server is running:")
        print("   python start_server.py\n")

if __name__ == "__main__":
    main()
