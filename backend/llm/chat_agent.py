"""
Chat-based Editing System
Allows conversational editing of research papers
"""
from typing import Dict, Any, Optional
from enum import Enum
from pydantic import BaseModel
from backend.config import settings


class IntentType(str, Enum):
    """Types of editing intents"""
    EDIT_SECTION = "edit_section"
    ADD_SECTION = "add_section"
    REPHRASE = "rephrase"
    SUMMARIZE = "summarize"
    EXPAND = "expand"
    ADD_CITATION = "add_citation"
    FIX_GRAMMAR = "fix_grammar"
    UNKNOWN = "unknown"


class Intent(BaseModel):
    """Parsed intent from user message"""
    type: IntentType
    section: Optional[str] = None
    instruction: str
    parameters: Dict[str, Any] = {}


class ChatAgent:
    """Processes chat messages and executes paper edits"""
    
    def __init__(self):
        # Keywords for intent matching
        self.intent_keywords = {
            IntentType.EDIT_SECTION: ["edit", "modify", "change", "update"],
            IntentType.ADD_SECTION: ["add", "insert", "include", "create"],
            IntentType.REPHRASE: ["rephrase", "reword", "rewrite"],
            IntentType.SUMMARIZE: ["summarize", "shorten", "condense", "concise"],
            IntentType.EXPAND: ["expand", "elaborate", "add more", "detail"],
            IntentType.ADD_CITATION: ["cite", "citation", "reference"],
            IntentType.FIX_GRAMMAR: ["grammar", "spelling", "typo", "fix"]
        }
        
        # Common section names
        self.sections = [
            "abstract", "introduction", "related work", "methodology",
            "results", "discussion", "conclusion", "limitations", "future work"
        ]
    
    def parse_intent(self, message: str) -> Intent:
        """
        Parse user message to determine intent
        
        Args:
            message: User's chat message
            
        Returns:
            Parsed Intent object
        """
        message_lower = message.lower()
        
        # Detect intent type
        detected_type = IntentType.UNKNOWN
        for intent_type, keywords in self.intent_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                detected_type = intent_type
                break
        
        # Detect section
        detected_section = None
        for section in self.sections:
            if section in message_lower:
                detected_section = section.replace(" ", "_")
                break
        
        # Build parameters
        parameters = {}
        
        if "more concise" in message_lower or "shorter" in message_lower:
            parameters["style"] = "concise"
        elif "more detail" in message_lower or "longer" in message_lower:
            parameters["style"] = "detailed"
        
        if "formal" in message_lower:
            parameters["tone"] = "formal"
        elif "informal" in message_lower or "casual" in message_lower:
            parameters["tone"] = "informal"
        
        return Intent(
            type=detected_type,
            section=detected_section,
            instruction=message,
            parameters=parameters
        )
    
    async def execute_edit(
        self,
        intent: Intent,
        paper_data: Dict[str, Any],
        llm_client: Any = None
    ) -> Dict[str, Any]:
        """
        Execute the editing action based on intent
        
        Args:
            intent: Parsed intent
            paper_data: Current paper data
            llm_client: LLM client for generating edits
            
        Returns:
            Dictionary with edit results
        """
        if not intent.section or intent.section not in paper_data:
            return {
                "success": False,
                "error": f"Section '{intent.section}' not found in paper",
                "available_sections": list(paper_data.keys())
            }
        
        current_content = paper_data[intent.section]
        
        # Generate edit using LLM
        if llm_client:
            try:
                new_content = await self._generate_edit_with_llm(
                    intent, current_content, llm_client
                )
            except Exception as e:
                return {
                    "success": False,
                    "error": f"Failed to generate edit: {str(e)}"
                }
        else:
            # Fallback: simple text manipulation
            new_content = self._simple_edit(intent, current_content)
        
        return {
            "success": True,
            "section": intent.section,
            "original": current_content,
            "edited": new_content,
            "preview": True  # Indicates this needs user approval
        }
    
    async def _generate_edit_with_llm(
        self,
        intent: Intent,
        current_content: str,
        llm_client: Any
    ) -> str:
        """
        Use LLM to generate edited content
        """
        # Build prompt based on intent type
        if intent.type == IntentType.SUMMARIZE:
            prompt = f"Make this text more concise while preserving key information:\n\n{current_content}"
        
        elif intent.type == IntentType.EXPAND:
            prompt = f"Expand this text with more detail and elaboration:\n\n{current_content}"
        
        elif intent.type == IntentType.REPHRASE:
            style = intent.parameters.get("tone", "academic")
            prompt = f"Rephrase this text in a {style} style:\n\n{current_content}"
        
        elif intent.type == IntentType.FIX_GRAMMAR:
            prompt = f"Fix any grammar, spelling, or punctuation errors in this text:\n\n{current_content}"
        
        else:
            prompt = f"{intent.instruction}\n\nCurrent text:\n{current_content}"
        
        # Call LLM (assuming ollama client)
        try:
            # Construct Ollama payload
            payload = {
                "model": settings.OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": settings.OLLAMA_TEMPERATURE
                }
            }
            
            # Call Ollama API
            import requests
            response = requests.post(f"{settings.OLLAMA_BASE_URL}/api/generate", json=payload)
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", current_content)
            else:
                print(f"Ollama Error: {response.text}")
                return current_content
                
        except Exception as e:
            print(f"LLM Generation Failed: {e}")
            return current_content
    
    def _simple_edit(self, intent: Intent, content: str) -> str:
        """
        Fallback: simple text manipulation without LLM
        """
        if intent.type == IntentType.SUMMARIZE:
            # Simple summarize: take first 50% of sentences
            sentences = content.split('. ')
            half = len(sentences) // 2
            return '. '.join(sentences[:half]) + '.'
        
        elif intent.type == IntentType.EXPAND:
            # Can't expand without LLM
            return content
        
        else:
            return content
    
    def generate_preview(self, edit_result: Dict[str, Any]) -> str:
        """
        Generate a preview of the edit
        """
        if not edit_result.get("success"):
            return f"Error: {edit_result.get('error', 'Unknown error')}"
        
        original = edit_result.get("original", "")
        edited = edit_result.get("edited", "")
        
        preview = f"**Section**: {edit_result.get('section', 'Unknown')}\n\n"
        preview += "**Original** (first 200 chars):\n"
        preview += f"{original[:200]}...\n\n"
        preview += "**Edited** (first 200 chars):\n"
        preview += f"{edited[:200]}...\n\n"
        preview += "Do you want to apply this edit? (yes/no)"
        
        return preview
