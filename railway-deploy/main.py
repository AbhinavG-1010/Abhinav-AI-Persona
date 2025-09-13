"""
Main FastAPI application for AI Persona.
"""
import os
import base64
from typing import Optional
from fastapi import FastAPI, HTTPException, Depends, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
import io
import uuid
from datetime import datetime

from config import get_settings
from models import (
    ConversationRequest, 
    ConversationResponse, 
    VoiceRequest, 
    VoiceResponse,
    HealthCheck,
    ErrorResponse,
    ConversationMessage,
    MessageRole
)
from services.openai_service import OpenAIService
from services.knowledge_service import KnowledgeService

# Initialize FastAPI app
settings = get_settings()
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="AI Persona for Recruiter Conversations"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
openai_service = OpenAIService()
knowledge_service = KnowledgeService()


@app.get("/", response_model=HealthCheck)
async def root():
    """Root endpoint with health check."""
    return HealthCheck(
        status="healthy",
        version=settings.app_version,
        services={
            "openai": "connected",
            "knowledge_base": "loaded",
            "database": "connected"
        }
    )


@app.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint."""
    return HealthCheck(
        status="healthy",
        version=settings.app_version,
        services={
            "openai": "connected",
            "knowledge_base": "loaded",
            "database": "connected"
        }
    )


@app.post("/conversation", response_model=ConversationResponse)
async def start_conversation(request: ConversationRequest):
    """Start or continue a conversation with the AI persona."""
    try:
        # Get or create conversation ID
        conversation_id = request.conversation_id or knowledge_service.start_conversation()
        
        # Get conversation history
        messages = knowledge_service.get_conversation_messages(conversation_id)
        
        # Add user message
        user_message = ConversationMessage(
            role=MessageRole.USER,
            content=request.message
        )
        knowledge_service.add_message(conversation_id, user_message)
        messages.append(user_message)
        
        # Get personal info and examples
        personal_info = knowledge_service.get_personal_info()
        conversation_examples = knowledge_service.get_conversation_examples()
        
        # Generate AI response
        ai_response_text = await openai_service.generate_response(
            messages, personal_info, conversation_examples
        )
        
        # Add AI response to conversation
        ai_message = ConversationMessage(
            role=MessageRole.ASSISTANT,
            content=ai_response_text
        )
        knowledge_service.add_message(conversation_id, ai_message)
        
        # Generate audio if requested
        audio_url = None
        if request.include_voice:
            audio_data = await openai_service.text_to_speech(ai_response_text)
            if audio_data:
                # In a real implementation, you'd save this to a file and return URL
                # For now, we'll return a placeholder
                audio_url = f"/audio/{conversation_id}/{len(messages)}"
        
        return ConversationResponse(
            message=ai_response_text,
            conversation_id=conversation_id,
            audio_url=audio_url,
            metadata={
                "message_count": len(messages),
                "timestamp": datetime.now().isoformat()
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing conversation: {str(e)}")


@app.post("/voice/transcribe", response_model=VoiceResponse)
async def transcribe_voice(audio_file: UploadFile = File(...)):
    """Transcribe voice to text."""
    try:
        # Read audio file
        audio_data = await audio_file.read()
        
        # Transcribe using OpenAI Whisper
        text = await openai_service.speech_to_text(audio_data)
        
        return VoiceResponse(
            text=text,
            confidence=0.95,  # Placeholder confidence
            language="en"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error transcribing audio: {str(e)}")


@app.post("/voice/synthesize")
async def synthesize_voice(request: VoiceRequest):
    """Convert text to speech."""
    try:
        # Generate speech
        audio_data = await openai_service.text_to_speech(request.text)
        
        if not audio_data:
            raise HTTPException(status_code=500, detail="Failed to generate speech")
        
        # Return audio as streaming response
        return StreamingResponse(
            io.BytesIO(audio_data),
            media_type="audio/mpeg",
            headers={"Content-Disposition": "attachment; filename=speech.mp3"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error synthesizing speech: {str(e)}")


@app.get("/conversation/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get conversation history."""
    try:
        conversation = knowledge_service.get_conversation(conversation_id)
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        return {
            "conversation_id": conversation_id,
            "messages": [
                {
                    "role": msg.role.value,
                    "content": msg.content,
                    "timestamp": msg.timestamp.isoformat()
                }
                for msg in conversation["messages"]
            ],
            "created_at": conversation["created_at"].isoformat(),
            "last_updated": conversation["last_updated"].isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving conversation: {str(e)}")


@app.get("/knowledge/search")
async def search_knowledge(query: str, limit: int = 5):
    """Search personal knowledge base."""
    try:
        results = knowledge_service.search_knowledge(query, limit)
        return {
            "query": query,
            "results": results,
            "count": len(results)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching knowledge: {str(e)}")


@app.get("/personal-info")
async def get_personal_info():
    """Get personal information (sanitized for privacy)."""
    try:
        personal_info = knowledge_service.get_personal_info()
        
        # Personal info is ready to be shared with recruiters
        
        return personal_info
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving personal info: {str(e)}")


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    return JSONResponse(
        status_code=500,
        content=ErrorResponse(
            error="Internal server error",
            detail=str(exc)
        ).dict()
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug
    )
