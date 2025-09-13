"""
Knowledge service for managing personal information and conversation context.
"""
import json
import uuid
from typing import Dict, Any, List, Optional
from datetime import datetime
from loguru import logger
import chromadb
from chromadb.config import Settings as ChromaSettings
from config import get_settings
from models import PersonalInfo, ConversationExamples, ConversationMessage


class KnowledgeService:
    """Service for managing personal knowledge base and conversation context."""
    
    def __init__(self):
        self.settings = get_settings()
        self.personal_info = self._load_personal_info()
        self.conversation_examples = self._load_conversation_examples()
        self.chroma_client = self._initialize_chroma()
        self.conversations = {}  # In-memory conversation storage
        
    def _load_personal_info(self) -> Dict[str, Any]:
        """Load personal information from JSON file."""
        try:
            with open(self.settings.personal_data_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading personal info: {e}")
            return {}
    
    def _load_conversation_examples(self) -> Dict[str, Any]:
        """Load conversation examples from JSON file."""
        try:
            with open(self.settings.conversation_examples_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading conversation examples: {e}")
            return {}
    
    def _initialize_chroma(self) -> chromadb.ClientAPI:
        """Initialize ChromaDB client."""
        try:
            client = chromadb.PersistentClient(
                path=self.settings.chroma_persist_directory
            )
            
            # Create or get collection
            collection = client.get_or_create_collection(
                name="personal_knowledge",
                metadata={"description": "Personal information for AI persona"}
            )
            
            # Initialize with personal data if collection is empty
            if collection.count() == 0:
                self._populate_knowledge_base(collection)
            
            return client
        except Exception as e:
            logger.error(f"Error initializing ChromaDB: {e}")
            return None
    
    def _populate_knowledge_base(self, collection):
        """Populate the knowledge base with personal information."""
        try:
            # Convert personal info to searchable chunks
            chunks = self._create_knowledge_chunks()
            
            # Add chunks to collection
            for i, chunk in enumerate(chunks):
                collection.add(
                    documents=[chunk["content"]],
                    metadatas=[chunk["metadata"]],
                    ids=[f"chunk_{i}"]
                )
            
            logger.info(f"Added {len(chunks)} knowledge chunks to database")
        except Exception as e:
            logger.error(f"Error populating knowledge base: {e}")
    
    def _create_knowledge_chunks(self) -> List[Dict[str, Any]]:
        """Create searchable chunks from personal information."""
        chunks = []
        
        # Personal details chunk
        personal_details = self.personal_info.get("personal_details", {})
        chunks.append({
            "content": f"Personal Information: Name is {personal_details.get('name', 'Not specified')}, located in {personal_details.get('location', 'Not specified')}, contact email {personal_details.get('email', 'Not specified')}, phone {personal_details.get('phone', 'Not specified')}",
            "metadata": {"type": "personal_details", "section": "contact_info"}
        })
        
        # Work authorization chunk
        work_auth = self.personal_info.get("work_authorization", {})
        chunks.append({
            "content": f"Work Authorization: {work_auth.get('status', 'Not specified')}, visa type {work_auth.get('visa_type', 'Not specified')}, sponsorship required {work_auth.get('sponsorship_required', 'Not specified')}, relocation willingness {work_auth.get('relocation_willingness', 'Not specified')}, remote preference {work_auth.get('remote_preference', 'Not specified')}",
            "metadata": {"type": "work_authorization", "section": "legal_status"}
        })
        
        # Professional summary chunk
        prof_summary = self.personal_info.get("professional_summary", {})
        chunks.append({
            "content": f"Professional Summary: {prof_summary.get('title', 'Not specified')} with {prof_summary.get('years_experience', 'Not specified')} years of experience. {prof_summary.get('summary', 'Not specified')}. Key skills: {', '.join(prof_summary.get('key_skills', []))}",
            "metadata": {"type": "professional_summary", "section": "overview"}
        })
        
        # Work experience chunks
        work_exp = self.personal_info.get("work_experience", [])
        for i, job in enumerate(work_exp):
            chunks.append({
                "content": f"Work Experience {i+1}: {job.get('position', 'Not specified')} at {job.get('company', 'Not specified')} from {job.get('duration', 'Not specified')}. {job.get('description', 'Not specified')}. Key achievements: {', '.join(job.get('key_achievements', []))}. Technologies used: {', '.join(job.get('technologies', []))}",
                "metadata": {"type": "work_experience", "section": f"job_{i+1}", "company": job.get('company', '')}
            })
        
        # Education chunks
        education = self.personal_info.get("education", [])
        for i, edu in enumerate(education):
            chunks.append({
                "content": f"Education {i+1}: {edu.get('degree', 'Not specified')} from {edu.get('institution', 'Not specified')} in {edu.get('graduation_year', 'Not specified')}. GPA: {edu.get('gpa', 'Not specified')}. Relevant coursework: {', '.join(edu.get('relevant_coursework', []))}",
                "metadata": {"type": "education", "section": f"education_{i+1}"}
            })
        
        # Preferences chunk
        preferences = self.personal_info.get("preferences", {})
        chunks.append({
            "content": f"Job Preferences: Salary range {preferences.get('salary_range', 'Not specified')}, job types {', '.join(preferences.get('job_types', []))}, company size preference {', '.join(preferences.get('company_size', []))}, work environment {preferences.get('work_environment', 'Not specified')}, career goals {preferences.get('career_goals', 'Not specified')}",
            "metadata": {"type": "preferences", "section": "job_preferences"}
        })
        
        # Availability chunk
        availability = self.personal_info.get("availability", {})
        chunks.append({
            "content": f"Availability: Notice period {availability.get('notice_period', 'Not specified')}, start date {availability.get('start_date', 'Not specified')}, interview availability {availability.get('interview_availability', 'Not specified')}, timezone {availability.get('timezone', 'Not specified')}",
            "metadata": {"type": "availability", "section": "timing"}
        })
        
        return chunks
    
    def search_knowledge(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Search the knowledge base for relevant information."""
        try:
            if not self.chroma_client:
                return []
            
            collection = self.chroma_client.get_collection("personal_knowledge")
            results = collection.query(
                query_texts=[query],
                n_results=n_results
            )
            
            # Format results
            formatted_results = []
            for i, doc in enumerate(results['documents'][0]):
                formatted_results.append({
                    "content": doc,
                    "metadata": results['metadatas'][0][i],
                    "distance": results['distances'][0][i]
                })
            
            return formatted_results
        except Exception as e:
            logger.error(f"Error searching knowledge base: {e}")
            return []
    
    def get_personal_info(self) -> Dict[str, Any]:
        """Get personal information."""
        return self.personal_info
    
    def get_conversation_examples(self) -> Dict[str, Any]:
        """Get conversation examples."""
        return self.conversation_examples
    
    def start_conversation(self) -> str:
        """Start a new conversation and return conversation ID."""
        conversation_id = str(uuid.uuid4())
        self.conversations[conversation_id] = {
            "messages": [],
            "created_at": datetime.now(),
            "last_updated": datetime.now()
        }
        return conversation_id
    
    def add_message(self, conversation_id: str, message: ConversationMessage):
        """Add a message to a conversation."""
        if conversation_id in self.conversations:
            self.conversations[conversation_id]["messages"].append(message)
            self.conversations[conversation_id]["last_updated"] = datetime.now()
    
    def get_conversation(self, conversation_id: str) -> Optional[Dict[str, Any]]:
        """Get conversation by ID."""
        return self.conversations.get(conversation_id)
    
    def get_conversation_messages(self, conversation_id: str) -> List[ConversationMessage]:
        """Get messages from a conversation."""
        conversation = self.get_conversation(conversation_id)
        if conversation:
            return conversation["messages"]
        return []
