"""
Plagiarism and Ethics Checking System
"""
from typing import List, Dict, Any
from backend.rag.vector_store import get_vector_store
import re

class PlagiarismChecker:
    """
    Detects potential plagiarism using RAG database
    """
    
    def __init__(self):
        self.vector_store = get_vector_store()
        self.similarity_threshold = 0.85  # >85% = potential plagiarism
    
    def check_paper(self, paper_text: str) -> Dict[str, Any]:
        """
        Check paper against RAG database for plagiarism
        
        Args:
            paper_text: Full paper text
            
        Returns:
            Dictionary with plagiarism analysis
        """
        # Split into paragraphs for checking
        paragraphs = self._split_into_paragraphs(paper_text)
        
        matches = []
        max_similarity = 0.0
        
        for i, para in enumerate(paragraphs):
            if len(para.split()) < 10:  # Skip very short paragraphs
                continue
            
            # Search for similar content
            similar = self.vector_store.search_similar(para, top_k=3)
            
            for match in similar:
                similarity = match.get('similarity_score', 0)
                
                if similarity > self.similarity_threshold:
                    matches.append({
                        "paragraph_number": i + 1,
                        "text_snippet": para[:200] + "...",
                        "matched_paper": match.get('title', 'Unknown'),
                        "similarity": similarity,
                        "severity": "high" if similarity > 0.95 else "medium"
                    })
                    
                max_similarity = max(max_similarity, similarity)
        
        # Determine overall status
        status = "clear"
        if max_similarity > 0.95:
            status = "high_risk"
        elif max_similarity > 0.85:
            status = "medium_risk"
        
        return {
            "status": status,
            "max_similarity": max_similarity,
            "matches_found": len(matches),
            "matches": matches,
            "recommendation": self._get_recommendation(status)
        }
    
    def _split_into_paragraphs(self, text: str) -> List[str]:
        """Split text into paragraphs"""
        # Split on double newlines
        paragraphs = re.split(r'\n\s*\n', text)
        return [p.strip() for p in paragraphs if p.strip()]
    
    def _get_recommendation(self, status: str) -> str:
        """Get recommendation based on status"""
        if status == "high_risk":
            return "⚠️ HIGH RISK: Very high similarity detected. Review all matches carefully."
        elif status == "medium_risk":
            return "⚠️ MEDIUM RISK: Significant similarity found. Ensure proper citation and paraphrasing."
        else:
            return "✓ CLEAR: No significant plagiarism detected."


class AIContentDetector:
    """
    Detects likely AI-generated content
    """
    
    def __init__(self):
        # Common AI phrases and patterns
        self.ai_indicators = [
            "as a large language model",
            "as an ai",
            "i am an ai",
            "i cannot",
            "i don't have personal",
            "in conclusion, it is important to note",
            "it is worth noting that",
            "moreover, it is essential to",
            "furthermore, one must consider"
        ]
        
        self.generic_transitions = [
            "it is important to note",
            "it should be mentioned",
            "it is worth noting",
            "one must consider",
            "furthermore",
            "moreover",
            "additionally",
            "in summary"
        ]
    
    def detect(self, text: str) -> Dict[str, Any]:
        """
        Detect AI-generated content
        
        Args:
            text: Paper text
            
        Returns:
            Detection results
        """
        text_lower = text.lower()
        
        issues = []
        ai_score = 0.0
        
        # Check for direct AI indicators
        for indicator in self.ai_indicators:
            if indicator in text_lower:
                issues.append(f"Contains AI self-reference: '{indicator}'")
                ai_score += 0.3
        
        # Check for excessive generic phrases
        generic_count = sum(1 for phrase in self.generic_transitions 
                          if text_lower.count(phrase) > 2)
        
        if generic_count > 3:
            issues.append(f"Excessive generic AI phrases (found {generic_count})")
            ai_score += 0.2
        
        # Check for lack of specific details
        if not self._has_specific_details(text):
            issues.append("Lacks specific technical details")
            ai_score += 0.1
        
        # Determine status
        if ai_score > 0.4:
            status = "likely_ai"
        elif ai_score > 0.2:
            status = "possibly_ai"
        else:
            status = "likely_human"
        
        return {
            "status": status,
            "ai_score": min(ai_score, 1.0),
            "issues": issues,
            "recommendation": self._get_ai_recommendation(status)
        }
    
    def _has_specific_details(self, text: str) -> bool:
        """Check if text has specific technical details"""
        # Look for numbers, equations, specific methodology
        has_numbers = bool(re.search(r'\d+\.?\d*', text))
        has_equations = bool(re.search(r'[=<>≈±∑∫]', text))
        has_citations = bool(re.search(r'\(\d{4}\)|et al\.|[[\d+\]]', text))
        
        return has_numbers or has_equations or has_citations
    
    def _get_ai_recommendation(self, status: str) -> str:
        """Get recommendation based on AI detection"""
        if status == "likely_ai":
            return "⚠️ High probability of AI-generated content. Add specific details and real experimental results."
        elif status == "possibly_ai":
            return "⚠️ Text may be AI-assisted. Ensure all claims are backed by real experiments."
        else:
            return "✓ Text appears human-written with specific details."


class EthicsChecker:
    """
    Validates paper against ethical research standards
    """
    
    def check_paper(self, paper_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check paper for ethical compliance
        
        Args:
            paper_data: Paper information including sections and metadata
            
        Returns:
            Ethics check results
        """
        checks = {}
        issues = []
        
        # Check 1: Has methodology section
        checks["has_methodology"] = "methodology" in paper_data
        if not checks["has_methodology"]:
            issues.append("Missing methodology section")
        
        # Check 2: Has citations
        checks["has_citations"] = paper_data.get("citation_count", 0) > 0
        if not checks["has_citations"]:
            issues.append("No citations found - must cite prior work")
        
        # Check 3: Includes limitations
        text = str(paper_data.get("content", "")).lower()
        checks["has_limitations"] = any(word in text for word in ["limitation", "limitations", "constraint"])
        if not checks["has_limitations"]:
            issues.append("Should discuss limitations of the research")
        
        # Check 4: Has results section
        checks["has_results"] = "results" in paper_data or "experimental_results" in paper_data
        if not checks["has_results"]:
            issues.append("Missing results section")
        
        # Check 5: Methodology is detailed
        if "methodology" in paper_data:
            method_text = str(paper_data["methodology"])
            checks["methodology_detailed"] = len(method_text.split()) > 100
            if not checks["methodology_detailed"]:
                issues.append("Methodology section seems too brief")
        
        # Calculate compliance score
        passed_checks = sum(1 for v in checks.values() if v)
        total_checks = len(checks)
        compliance_score = passed_checks / total_checks if total_checks > 0 else 0.0
        
        # Determine status
        if compliance_score >= 0.8:
            status = "compliant"
        elif compliance_score >= 0.6:
            status = "needs_improvement"
        else:
            status = "non_compliant"
        
        return {
            "status": status,
            "compliance_score": compliance_score,
            "checks": checks,
            "issues": issues,
            "recommendation": self._get_ethics_recommendation(status, issues)
        }
    
    def _get_ethics_recommendation(self, status: str, issues: List[str]) -> str:
        """Get ethics recommendation"""
        if status == "compliant":
            return "✓ Paper meets ethical research standards."
        elif status == "needs_improvement":
            return f"⚠️ Address these issues: {'; '.join(issues[:3])}"
        else:
            return f"❌ Major ethical issues: {'; '.join(issues)}"
