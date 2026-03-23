"""
Chat API Routes for conversational paper editing
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime

from backend.database.database import get_db
from backend.database.models import ResearchPaper
from backend.llm.chat_agent import ChatAgent
from backend.llm.ollama_client import OllamaClient

router = APIRouter(prefix="/api/papers", tags=["chat"])


class ChatMessage(BaseModel):
    message: str


class ChatHistoryItem(BaseModel):
    role: str  # user or assistant
    message: str
    timestamp: str


class ApplyEditRequest(BaseModel):
    section: str
    content: str


# Store chat history in memory (in production, use database)
chat_histories: Dict[str, List[ChatHistoryItem]] = {}


@router.post("/{paper_id}/chat")
async def chat_edit(
    paper_id: str,
    chat_msg: ChatMessage,
    db: Session = Depends(get_db)
):
    """
    Chat-based paper editing
    
    Examples:
    - "Make the abstract more concise"
    - "Rephrase the introduction in a more formal tone"
    - "Expand the methodology section with more detail"
    - "Fix grammar in the conclusion"
    """
    # Get paper
    paper = db.query(ResearchPaper).filter(ResearchPaper.id == paper_id).first()
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    # Initialize chat agent
    agent = ChatAgent()
    
    # Parse intent
    intent = agent.parse_intent(chat_msg.message)
    
    # Initialize chat history if not exists
    if paper_id not in chat_histories:
        chat_histories[paper_id] = []
    
    # Add user message to history
    chat_histories[paper_id].append(ChatHistoryItem(
        role="user",
        message=chat_msg.message,
        timestamp=datetime.utcnow().isoformat()
    ))
    
    # Handle different intent types
    if intent.type.value == "unknown":
        response_msg = (
            "I'm not sure what you want to do. Try commands like:\n"
            "- 'Make the abstract shorter'\n"
            "- 'Rephrase the introduction'\n"
            "- 'Expand the methodology section'"
        )
        
        chat_histories[paper_id].append(ChatHistoryItem(
            role="assistant",
            message=response_msg,
            timestamp=datetime.utcnow().isoformat()
        ))
        
        return {
            "response": response_msg,
            "intent": intent.dict(),
            "action": "clarification"
        }
    
    # Execute edit
    try:
        # Get LLM client (optional)
        llm_client = None
        try:
            llm_client = OllamaClient()
        except:
            pass
        
        edit_result = await agent.execute_edit(
            intent,
            paper.paper_data or {},
            llm_client
        )
        
    except Exception as e:
        response_msg = f"Error processing your request: {str(e)}"
        
        chat_histories[paper_id].append(ChatHistoryItem(
            role="assistant",
            message=response_msg,
            timestamp=datetime.utcnow().isoformat()
        ))
        
        raise HTTPException(status_code=500, detail=response_msg)
    
    if not edit_result.get("success"):
        response_msg = edit_result.get("error", "Failed to process edit")
        
        chat_histories[paper_id].append(ChatHistoryItem(
            role="assistant",
            message=response_msg,
            timestamp=datetime.utcnow().isoformat()
        ))
        
        return {
            "response": response_msg,
            "intent": intent.dict(),
            "action": "error",
            "available_sections": edit_result.get("available_sections", [])
        }
    
    # Generate preview
    preview = agent.generate_preview(edit_result)
    
    chat_histories[paper_id].append(ChatHistoryItem(
        role="assistant",
        message=preview,
        timestamp=datetime.utcnow().isoformat()
    ))
    
    return {
        "response": preview,
        "intent": intent.dict(),
        "action": "preview",
        "edit_result": {
            "section": edit_result.get("section"),
            "original_length": len(edit_result.get("original", "")),
            "edited_length": len(edit_result.get("edited", "")),
            "edited_content": edit_result.get("edited")
        }
    }


@router.post("/{paper_id}/apply-edit")
async def apply_edit(
    paper_id: str,
    edit_request: ApplyEditRequest,
    db: Session = Depends(get_db)
):
    """
    Apply an edit to the paper
    """
    # Get paper
    paper = db.query(ResearchPaper).filter(ResearchPaper.id == paper_id).first()
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    # Apply edit
    paper_data = paper.paper_data or {}
    paper_data[edit_request.section] = edit_request.content
    paper.paper_data = paper_data
    
    db.commit()
    db.refresh(paper)
    
    # Add to chat history
    if paper_id not in chat_histories:
        chat_histories[paper_id] = []
    
    chat_histories[paper_id].append(ChatHistoryItem(
        role="assistant",
        message=f"✓ Applied edit to {edit_request.section}",
        timestamp=datetime.utcnow().isoformat()
    ))
    
    return {
        "success": True,
        "message": f"Edit applied to {edit_request.section}",
        "updated_at": paper.updated_at.isoformat() if paper.updated_at else None
    }


@router.get("/{paper_id}/chat/history")
async def get_chat_history(paper_id: str):
    """
    Get chat history for a paper
    """
    history = chat_histories.get(paper_id, [])
    
    return {
        "paper_id": paper_id,
        "message_count": len(history),
        "messages": [msg.dict() for msg in history]
    }


@router.delete("/{paper_id}/chat/history")
async def clear_chat_history(paper_id: str):
    """
    Clear chat history for a paper
    """
    if paper_id in chat_histories:
        del chat_histories[paper_id]
    
    return {
        "success": True,
        "message": "Chat history cleared"
    }
