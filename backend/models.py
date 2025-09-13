"""
Data models for the AI Persona application.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime
from enum import Enum


class MessageRole(str, Enum):
    """Message roles in conversation."""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class ConversationMessage(BaseModel):
    """Individual message in a conversation."""
    role: MessageRole
    content: str
    timestamp: datetime = Field(default_factory=datetime.now)
    metadata: Optional[Dict[str, Any]] = None


class ConversationRequest(BaseModel):
    """Request to start or continue a conversation."""
    message: str
    conversation_id: Optional[str] = None
    include_voice: bool = False
    context: Optional[Dict[str, Any]] = None


class ConversationResponse(BaseModel):
    """Response from the AI persona."""
    message: str
    conversation_id: str
    audio_url: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class VoiceRequest(BaseModel):
    """Request for voice processing."""
    audio_data: str  # Base64 encoded audio
    format: str = "wav"
    language: str = "en"


class VoiceResponse(BaseModel):
    """Response from voice processing."""
    text: str
    confidence: float
    language: str


class PersonalInfo(BaseModel):
    """Personal information structure."""
    personal_details: Dict[str, Any]
    work_authorization: Dict[str, Any]
    professional_summary: Dict[str, Any]
    work_experience: List[Dict[str, Any]]
    education: List[Dict[str, Any]]
    certifications: List[Dict[str, Any]]
    projects: List[Dict[str, Any]]
    preferences: Dict[str, Any]
    availability: Dict[str, Any]
    common_questions: Dict[str, Any]


class ConversationExample(BaseModel):
    """Example conversation for training."""
    scenario: str
    recruiter_question: str
    ai_response: str
    context: str


class ConversationExamples(BaseModel):
    """Collection of conversation examples."""
    recruiter_conversations: List[ConversationExample]
    personality_traits: Dict[str, Any]


class HealthCheck(BaseModel):
    """Health check response."""
    status: str
    timestamp: datetime = Field(default_factory=datetime.now)
    version: str
    services: Dict[str, str]


class ErrorResponse(BaseModel):
    """Error response model."""
    error: str
    detail: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)
