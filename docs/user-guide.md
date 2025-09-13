# AI Persona - User Guide

Welcome to AI Persona! This guide will help you set up and use your AI assistant for recruiter conversations.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Personalizing Your AI](#personalizing-your-ai)
3. [Using the Interface](#using-the-interface)
4. [Voice Features](#voice-features)
5. [Best Practices](#best-practices)
6. [Troubleshooting](#troubleshooting)

## Getting Started

### Initial Setup

1. **Configure Your Personal Information**
   - Edit `data/personal_info.json` with your details
   - Include work experience, skills, education, and preferences
   - Add your work authorization status and location preferences

2. **Set Up API Keys**
   - Get an OpenAI API key from [OpenAI Platform](https://platform.openai.com/)
   - Add it to your `.env` file: `OPENAI_API_KEY=your_key_here`

3. **Start the Application**
   ```bash
   ./scripts/start-dev.sh  # For development
   # or
   ./scripts/start-prod.sh  # For production
   ```

4. **Access the Interface**
   - Open your browser to http://localhost:3000 (dev) or http://localhost:80 (prod)
   - You should see the AI Persona interface

## Personalizing Your AI

### Personal Information Structure

Your AI persona uses the following information to answer questions:

#### Personal Details
```json
{
  "personal_details": {
    "name": "Your Name",
    "email": "your.email@example.com",
    "phone": "+1-XXX-XXX-XXXX",
    "location": "City, Country",
    "linkedin": "https://linkedin.com/in/yourprofile"
  }
}
```

#### Professional Summary
```json
{
  "professional_summary": {
    "title": "Software Engineer",
    "years_experience": 5,
    "summary": "Experienced software engineer with expertise in...",
    "key_skills": ["Python", "JavaScript", "React", "AWS"],
    "industries": ["Technology", "Finance"]
  }
}
```

#### Work Experience
```json
{
  "work_experience": [
    {
      "company": "Current Company",
      "position": "Senior Software Engineer",
      "duration": "2022 - Present",
      "location": "San Francisco, CA",
      "description": "Lead development of...",
      "key_achievements": [
        "Improved system performance by 40%",
        "Led team of 5 developers"
      ],
      "technologies": ["Python", "React", "AWS", "Docker"],
      "team_size": 8,
      "reporting_to": "Engineering Manager"
    }
  ]
}
```

#### Work Authorization
```json
{
  "work_authorization": {
    "status": "Authorized to work in the US",
    "visa_type": "H-1B",
    "sponsorship_required": false,
    "relocation_willingness": "Open to relocation",
    "remote_preference": "Hybrid preferred"
  }
}
```

#### Job Preferences
```json
{
  "preferences": {
    "salary_range": "$120,000 - $150,000",
    "job_types": ["Full-time", "Contract"],
    "company_size": ["Mid-size", "Enterprise"],
    "work_environment": "Collaborative, innovative, growth-oriented",
    "benefits_important": ["Health Insurance", "401k", "Flexible Hours"],
    "career_goals": "Looking to grow into senior/lead roles"
  }
}
```

### Customizing Responses

You can customize how your AI responds by editing `data/conversation_examples.json`:

```json
{
  "personality_traits": {
    "communication_style": "Professional, friendly, and direct",
    "tone": "Confident but humble, enthusiastic about opportunities",
    "response_length": "Concise but comprehensive, typically 2-3 sentences",
    "key_phrases": [
      "I'm excited about the opportunity",
      "I'm looking for growth opportunities",
      "I can start immediately"
    ]
  }
}
```

## Using the Interface

### Chat Interface

1. **Text Input**
   - Type your message in the input field
   - Press Enter or click Send to submit
   - Use the quick action buttons for common questions

2. **Voice Input**
   - Click the microphone button to start recording
   - Speak your question clearly
   - Click again to stop recording
   - The AI will transcribe and respond

3. **Voice Output**
   - Click the play button next to AI responses to hear them
   - Adjust voice settings in the sidebar
   - Enable auto-play for automatic audio responses

### Quick Actions

Use these pre-configured questions to test your AI:

- **About Me**: "Tell me about yourself"
- **Skills**: "What are your technical skills?"
- **Work Auth**: "Do you require visa sponsorship?"
- **Salary**: "What are your salary expectations?"
- **Availability**: "When can you start?"
- **Why Leaving**: "Why are you looking for a new role?"

### Sidebar Features

1. **Profile Summary**
   - View your key information at a glance
   - Verify that your data is loaded correctly

2. **Quick Actions**
   - One-click access to common recruiter questions
   - Customize these buttons for your specific needs

3. **Settings**
   - Toggle voice responses on/off
   - Enable/disable auto-play audio
   - Adjust other preferences

## Voice Features

### Speech-to-Text (STT)

Your AI can understand spoken questions:

1. **Start Recording**
   - Click the microphone button
   - Grant microphone permissions if prompted
   - Speak clearly and at normal pace

2. **Best Practices**
   - Speak in a quiet environment
   - Use clear pronunciation
   - Keep questions concise
   - Wait for the red recording indicator

### Text-to-Speech (TTS)

Your AI can respond with voice:

1. **Play Responses**
   - Click the play button next to any AI response
   - Adjust volume on your device
   - Use headphones for better audio quality

2. **Voice Settings**
   - Voice model: Choose from different AI voices
   - Speed: Adjust speaking pace
   - Pitch: Modify voice tone

### Voice Training (Optional)

To improve voice recognition:

1. **Record Sample Questions**
   - Save audio files in `data/voice_samples/`
   - Use clear, natural speech
   - Include various question types

2. **Test Recognition**
   - Try different phrasings
   - Note any recognition issues
   - Adjust microphone settings if needed

## Best Practices

### For Recruiters

1. **Test Common Questions**
   - Ask about work authorization early
   - Inquire about salary expectations
   - Check availability and notice period
   - Ask about technical skills

2. **Evaluate Responses**
   - Check for consistency in answers
   - Verify technical accuracy
   - Assess communication style
   - Note enthusiasm and professionalism

### For Job Seekers

1. **Keep Information Updated**
   - Update work experience regularly
   - Refresh skills and certifications
   - Adjust salary expectations as needed
   - Update availability status

2. **Customize for Different Roles**
   - Emphasize relevant skills for each position
   - Adjust career goals based on opportunity
   - Modify communication style if needed
   - Update location preferences

3. **Monitor Conversations**
   - Review AI responses for accuracy
   - Note any areas needing improvement
   - Update personal information as needed
   - Refine conversation examples

### Privacy and Security

1. **Data Protection**
   - Your personal information is stored locally
   - API calls to OpenAI are encrypted
   - No conversation data is permanently stored
   - Use strong passwords for any accounts

2. **API Usage**
   - Monitor OpenAI API usage and costs
   - Set usage limits if needed
   - Review API logs regularly
   - Keep API keys secure

## Troubleshooting

### Common Issues

#### AI Not Responding
1. Check internet connection
2. Verify OpenAI API key is correct
3. Check browser console for errors
4. Restart the application

#### Voice Not Working
1. Grant microphone permissions
2. Check browser audio settings
3. Test with different browsers
4. Verify audio drivers are working

#### Incorrect Responses
1. Review personal information in `data/personal_info.json`
2. Check conversation examples
3. Update system prompts if needed
4. Test with different question phrasings

#### Performance Issues
1. Check system resources
2. Restart Docker containers
3. Clear browser cache
4. Update dependencies

### Getting Help

1. **Check Logs**
   ```bash
   docker-compose logs -f backend
   docker-compose logs -f frontend
   ```

2. **Health Checks**
   - Backend: http://localhost:8000/health
   - Frontend: http://localhost:80

3. **Debug Mode**
   ```bash
   export DEBUG=True
   ./scripts/start-dev.sh
   ```

4. **Reset Application**
   ```bash
   docker-compose down
   docker-compose up --build
   ```

### Support Resources

- **Documentation**: Check the `/docs` folder
- **API Documentation**: http://localhost:8000/docs
- **GitHub Issues**: Report bugs and feature requests
- **Community**: Join discussions and get help

## Advanced Features

### Custom Prompts

You can customize the AI's behavior by modifying the system prompt in `backend/services/openai_service.py`:

```python
def _build_system_prompt(self, personal_info, conversation_examples):
    # Customize this method to change AI behavior
    system_prompt = f"""
    You are an AI assistant representing {personal_info['name']}...
    # Add your custom instructions here
    """
    return system_prompt
```

### Integration with Other Tools

1. **Calendar Integration**
   - Add availability checking
   - Schedule interview reminders
   - Sync with Google Calendar

2. **Job Board Integration**
   - Connect with LinkedIn Jobs
   - Monitor job postings
   - Auto-apply to relevant positions

3. **CRM Integration**
   - Track recruiter interactions
   - Manage application pipeline
   - Generate follow-up reminders

### Analytics and Insights

1. **Conversation Analytics**
   - Track common questions
   - Monitor response quality
   - Identify improvement areas

2. **Performance Metrics**
   - Response time analysis
   - API usage statistics
   - Error rate monitoring

Remember: Your AI persona is a tool to help you in your job search. Always review and approve responses before using them in real conversations, and keep your information updated for the best results!
