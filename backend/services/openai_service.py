"""
OpenAI service for handling AI interactions.
"""
import json
import openai
from typing import List, Dict, Any, Optional
from loguru import logger
from config import get_settings
from models import ConversationMessage, MessageRole


class OpenAIService:
    """Service for OpenAI API interactions."""
    
    def __init__(self):
        self.settings = get_settings()
        self.client = openai.OpenAI(api_key=self.settings.openai_api_key)
        self.model = self.settings.openai_model
        self.embedding_model = self.settings.openai_embedding_model
        
    async def generate_response(
        self, 
        messages: List[ConversationMessage], 
        personal_info: Dict[str, Any],
        conversation_examples: Dict[str, Any]
    ) -> str:
        """Generate AI response based on conversation history and personal info."""
        try:
            # Build system prompt with personal information
            system_prompt = self._build_system_prompt(personal_info, conversation_examples)
            
            # Convert messages to OpenAI format
            openai_messages = [
                {"role": "system", "content": system_prompt}
            ]
            
            for message in messages[-10:]:  # Keep last 10 messages for context
                openai_messages.append({
                    "role": message.role.value,
                    "content": message.content
                })
            
            # Generate response
            response = self.client.chat.completions.create(
                model=self.model,
                messages=openai_messages,
                max_tokens=500,
                temperature=0.7,
                presence_penalty=0.1,
                frequency_penalty=0.1
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"Error generating OpenAI response: {e}")
            # Mock response for testing when API quota is exceeded
            return self._generate_mock_response(messages, personal_info)
    
    def _build_system_prompt(
        self, 
        personal_info: Dict[str, Any], 
        conversation_examples: Dict[str, Any]
    ) -> str:
        """Build the system prompt with personal information and examples."""
        
        # Extract key information
        personal_details = personal_info.get("personal_details", {})
        work_auth = personal_info.get("work_authorization", {})
        prof_summary = personal_info.get("professional_summary", {})
        work_exp = personal_info.get("work_experience", [])
        preferences = personal_info.get("preferences", {})
        availability = personal_info.get("availability", {})
        common_questions = personal_info.get("common_questions", {})
        
        # Get personality traits
        personality = conversation_examples.get("personality_traits", {})
        
        system_prompt = f"""
You are an AI assistant representing {personal_details.get('name', 'the candidate')} in recruiter conversations. 

PERSONAL INFORMATION:
- Name: {personal_details.get('name', 'Not specified')}
- Current Role: {prof_summary.get('title', 'Not specified')}
- Experience: {prof_summary.get('years_experience', 'Not specified')} years
- Location: {personal_details.get('location', 'Not specified')}
- Work Authorization: {work_auth.get('status', 'Not specified')}
- Visa Sponsorship Required: {work_auth.get('sponsorship_required', 'Not specified')}
- Relocation: {work_auth.get('relocation_willingness', 'Not specified')}
- Remote Preference: {work_auth.get('remote_preference', 'Not specified')}

PROFESSIONAL SUMMARY:
{prof_summary.get('summary', 'Not specified')}

KEY SKILLS: {', '.join(prof_summary.get('key_skills', []))}

CURRENT WORK EXPERIENCE:
"""
        
        # Add current work experience
        if work_exp:
            current_job = work_exp[0]
            system_prompt += f"""
- Company: {current_job.get('company', 'Not specified')}
- Position: {current_job.get('position', 'Not specified')}
- Duration: {current_job.get('duration', 'Not specified')}
- Description: {current_job.get('description', 'Not specified')}
- Key Achievements: {', '.join(current_job.get('key_achievements', []))}
- Technologies: {', '.join(current_job.get('technologies', []))}
"""
        
        system_prompt += f"""

PREFERENCES:
- Salary Range: {preferences.get('salary_range', 'Not specified')}
- Job Types: {', '.join(preferences.get('job_types', []))}
- Company Size: {', '.join(preferences.get('company_size', []))}
- Work Environment: {preferences.get('work_environment', 'Not specified')}
- Career Goals: {preferences.get('career_goals', 'Not specified')}

AVAILABILITY:
- Notice Period: {availability.get('notice_period', 'Not specified')}
- Start Date: {availability.get('start_date', 'Not specified')}
- Interview Availability: {availability.get('interview_availability', 'Not specified')}

COMMON RESPONSES:
- Why Leaving: {common_questions.get('why_leaving', 'Not specified')}
- Strengths: {common_questions.get('strengths', 'Not specified')}
- Questions for Them: {', '.join(common_questions.get('questions_for_them', []))}

PERSONALITY & COMMUNICATION STYLE:
- Style: {personality.get('communication_style', 'Professional and friendly')}
- Tone: {personality.get('tone', 'Confident but humble')}
- Response Length: {personality.get('response_length', 'Concise but comprehensive')}

INSTRUCTIONS:
1. Always respond as if you ARE the candidate, not as an AI representing them
2. Be professional, friendly, and enthusiastic about opportunities
3. Keep responses concise but comprehensive (2-3 sentences typically)
4. Always mention work authorization status when relevant
5. Be specific about skills and experience when asked
6. Show genuine interest in the role and company
7. Ask thoughtful questions about the role and company
8. Never mention that you are an AI or bot
9. If you don't know something specific, say you'd be happy to discuss it further
10. Always maintain a positive, professional tone

Remember: You are representing a real person in job interviews. Be authentic, professional, and helpful.
"""
        
        return system_prompt
    
    def _generate_mock_response(self, messages: List[ConversationMessage], personal_info: Dict[str, Any]) -> str:
        """Generate mock responses for testing when API quota is exceeded."""
        if not messages:
            return "Hello! I'm your AI persona, ready to help with recruiter conversations."
        
        last_message = messages[-1].content.lower()
        personal_details = personal_info.get("personal_details", {})
        prof_summary = personal_info.get("professional_summary", {})
        work_auth = personal_info.get("work_authorization", {})
        
        # Simple keyword-based responses
        if "tell me about yourself" in last_message or "about you" in last_message:
            return f"Hi! I'm {personal_details.get('name', 'Abhinav')}, an {prof_summary.get('title', 'AI/ML Engineer')} with {prof_summary.get('years_experience', 2)} years of experience. I specialize in {', '.join(prof_summary.get('key_skills', ['Python', 'Machine Learning'])[:3])} and I'm currently looking for new opportunities in the AI/ML space."
        
        elif "skills" in last_message or "technical" in last_message:
            skills = prof_summary.get('key_skills', ['Python', 'Machine Learning', 'Data Analysis'])
            return f"My key technical skills include {', '.join(skills[:5])}. I have hands-on experience with machine learning frameworks, cloud platforms, and full-stack development."
        
        elif "sponsorship" in last_message or "visa" in last_message:
            return f"I'm authorized to work in the USA under {work_auth.get('visa_type', 'F-1 OPT')}. {work_auth.get('status', 'I can work legally in the US')}."
        
        elif "salary" in last_message or "compensation" in last_message:
            return "I'm open to discussing compensation based on the role, responsibilities, and market rates. I'm looking for a competitive package that reflects my experience and the value I can bring to the team."
        
        elif "start" in last_message or "available" in last_message:
            return "I can start immediately with a 2-week notice period. I'm flexible with interview scheduling and ready to move quickly through the hiring process."
        
        elif "why" in last_message and ("leaving" in last_message or "looking" in last_message):
            return "I'm seeking new challenges and growth opportunities in the AI/ML space. I want to work on cutting-edge projects and contribute to innovative solutions that make a real impact."
        
        else:
            return f"Thanks for your question! I'm {personal_details.get('name', 'Abhinav')}, an experienced {prof_summary.get('title', 'AI/ML Engineer')} with a strong background in {', '.join(prof_summary.get('key_skills', ['Python', 'Machine Learning'])[:3])}. I'd be happy to discuss how my skills and experience can contribute to your team. What specific aspects would you like to know more about?"
    
    async def generate_embeddings(self, text: str) -> List[float]:
        """Generate embeddings for text using OpenAI."""
        try:
            response = self.client.embeddings.create(
                model=self.embedding_model,
                input=text
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            return []
    
    async def text_to_speech(self, text: str) -> bytes:
        """Convert text to speech using OpenAI TTS."""
        try:
            response = self.client.audio.speech.create(
                model="tts-1",
                voice=self.settings.voice_model,
                input=text,
                speed=self.settings.voice_speed
            )
            return response.content
        except Exception as e:
            logger.error(f"Error generating speech: {e}")
            return b""
    
    async def speech_to_text(self, audio_data: bytes) -> str:
        """Convert speech to text using OpenAI Whisper."""
        try:
            # Create a temporary file-like object
            import io
            audio_file = io.BytesIO(audio_data)
            audio_file.name = "audio.wav"
            
            response = self.client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file,
                language="en"
            )
            return response.text
        except Exception as e:
            logger.error(f"Error transcribing speech: {e}")
            return ""
