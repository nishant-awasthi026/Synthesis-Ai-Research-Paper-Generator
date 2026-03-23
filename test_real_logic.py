import asyncio
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.services.search_service import search_service
from backend.llm.chat_agent import ChatAgent, Intent, IntentType
from backend.config import settings

async def run_brainstorm_loop(iteration, topic):
    print(f"\n--- Loop {iteration}: Testing Topic '{topic}' ---")
    
    # 1. Real Web Search
    print(f"[1] Searching Web for: {topic}...")
    results = search_service.search_papers(topic, limit=3)
    
    if not results:
        print("❌ WEB SEARCH FAILED: No results found.")
        return False
    
    print(f"✅ Found {len(results)} papers.")
    context_text = "\n".join([f"- {r['title']}: {r['snippet']}" for r in results])
    
    # 2. AI Generation (Ollama)
    print(f"[2] Generating Abstract with {settings.OLLAMA_MODEL}...")
    agent = ChatAgent()
    
    prompt_text = f"Based on the following research papers, write a short academic abstract about '{topic}':\n\n{context_text}"
    
    # Create a dummy intent since execute_edit functionality is slightly different
    # We'll use the _generate_edit_with_llm directly or mock the client call structure
    # Actually, ChatAgent.execute_edit expects an intent. Let's make a Direct Call similar to agent internal logic.
    
    # Manually calling requests to simulate what ChatAgent does, to verify connectivity
    import requests
    try:
        payload = {
            "model": settings.OLLAMA_MODEL,
            "prompt": prompt_text,
            "stream": False
        }
        resp = requests.post(f"{settings.OLLAMA_BASE_URL}/api/generate", json=payload)
        
        if resp.status_code == 200:
            ai_text = resp.json().get("response", "")
            if len(ai_text) > 50:
                print(f"✅ AI Generation Successful ({len(ai_text)} chars).")
                print(f"Sample: {ai_text[:100]}...")
                return True
            else:
                 print(f"❌ AI Generation Weak: {ai_text}")
                 return False
        else:
            print(f"❌ AI API Error: {resp.status_code}")
            return False
            
    except Exception as e:
         print(f"❌ AI Connection Error: {e}")
         return False

async def main():
    topics = [
        "Generative AI in Drug Discovery",
        "Quantum Machine Learning Algorithms",
        "Ethical Implications of Autonomous Vehicles",
        "CRISPR Applications in Agriculture",
        "Zero-Knowledge Proofs in Blockchain"
    ]
    
    success_count = 0
    for i, topic in enumerate(topics, 1):
        try:
            passed = await run_brainstorm_loop(i, topic)
            if passed: success_count += 1
        except Exception as e:
            print(f"Loop {i} Crashed: {e}")
            
    print(f"\n\n=== TEST SUMMARY ===")
    print(f"Passed: {success_count}/{len(topics)}")
    
    if success_count == len(topics):
        print("🎉 PASSED: Real World Logic is Operational!")
    else:
        print("⚠️ WARNING: Some checks failed.")

if __name__ == "__main__":
    asyncio.run(main())
