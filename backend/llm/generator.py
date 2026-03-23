"""
RAG-enhanced paper generator using LLM + retrieval
"""
from typing import Dict, Any, List
from backend.llm.ollama_client import get_ollama_client
from backend.llm.prompts import get_prompt
from backend.rag.vector_store import get_vector_store

class PaperGenerator:
    def __init__(self):
        """Initialize paper generator with LLM and RAG"""
        self.llm = get_ollama_client()
        self.vector_store = get_vector_store()
        print("📝 Paper generator initialized")
    
    def generate_section(
        self,
        section_type: str,
        user_input: Dict[str, Any],
        use_rag: bool = True,
        rag_top_k: int = 5
    ) -> Dict[str, Any]:
        """
        Generate a paper section using RAG + LLM
        
        Args:
            section_type: Type of section (abstract, introduction, etc.)
            user_input: User-provided content (title, problem, etc.)
            use_rag: Whether to use RAG for context
            rag_top_k: Number of similar papers to retrieve
            
        Returns:
            Dictionary with generated content and metadata
        """
        # Step 1: Retrieve relevant context if RAG is enabled
        rag_context = ""
        rag_sources = []
        
        if use_rag:
            # Create query from user input
            query = self._create_rag_query(section_type, user_input)
            
            # Search vector store
            similar_papers = self.vector_store.search_similar(
                query=query,
                top_k=rag_top_k
            )
            
            # Format context
            rag_context = self._format_rag_context(similar_papers)
            rag_sources = similar_papers
        
        # Step 2: Build prompt
        prompt_vars = {
            **user_input,
            'rag_context': rag_context or "No specific prior work retrieved."
        }
        
        try:
            prompt = get_prompt(section_type, **prompt_vars)
        except ValueError as e:
            return {
                "error": str(e),
                "content": "",
                "rag_sources": []
            }
        
        # Step 3: Generate with LLM
        response = self.llm.generate(prompt)
        
        if "error" in response:
            return {
                "error": response["error"],
                "content": "",
                "rag_sources": []
            }
        
        # Step 4: Return results
        return {
            "content": response.get("response", ""),
            "rag_sources": rag_sources,
            "section_type": section_type,
            "tokens_used": response.get("eval_count", 0)
        }
    
    def _create_rag_query(self, section_type: str, user_input: Dict[str, Any]) -> str:
        """Create appropriate RAG query based on section type"""
        title = user_input.get('title', '')
        domain = user_input.get('domain', '')
        problem = user_input.get('problem', '')
        
        if section_type == "introduction":
            return f"{title} {domain} introduction research"
        elif section_type == "lit_review":
            return f"{title} {domain} literature review related work"
        elif section_type == "methodology":
            return f"{title} methodology approach implementation"
        elif section_type == "results":
            return f"{title} results evaluation performance"
        else:
            return f"{title} {domain}"
    
    def _format_rag_context(self, papers: List[Dict[str, Any]]) -> str:
        """Format retrieved papers into readable context"""
        if not papers:
            return ""
        
        context_parts = []
        for i, paper in enumerate(papers, 1):
            context_parts.append(f"""
[{i}] {paper.get('title', 'Unknown')} ({paper.get('year', 'N/A')})
    Authors: {paper.get('authors', 'Unknown')}
    Summary: {paper.get('abstract', '')[:300]}...
    Relevance Score: {paper.get('similarity_score', 0):.2f}
""")
        
        return "\n".join(context_parts)
    
    def generate_topic_ideas(
        self, 
        domain: str, 
        keywords: List[str], 
        user_interest: str
    ) -> Dict[str, Any]:
        """Generate research topic ideas"""
        prompt = get_prompt(
            "topic_generation",
            domain=domain,
            keywords=", ".join(keywords),
            user_interest=user_interest
        )
        
        response = self.llm.generate(prompt, temperature=0.8)
        
        if "error" in response:
            return {"error": response["error"], "topics": []}
        
        return {
            "topics": response.get("response", ""),
            "domain": domain
        }

# Singleton instance
_generator = None

def get_generator() -> PaperGenerator:
    """Get or create paper generator singleton"""
    global _generator
    if _generator is None:
        _generator = PaperGenerator()
    return _generator
