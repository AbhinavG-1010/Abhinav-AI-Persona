# AI Persona - Recruiter Assistant

An AI-powered assistant that represents you in recruiter conversations, handling questions about your background, work experience, and preferences. Perfect for job seekers who want to streamline their interview process and ensure consistent, professional responses.

## ✨ Features

- 🤖 **AI-Powered Conversations**: GPT-4 powered responses based on your personal information
- 🎤 **Voice Interaction**: Speech-to-text and text-to-speech capabilities
- 📊 **Personal Knowledge Base**: Vector database storing your work history, skills, and preferences
- 🌐 **Modern Web Interface**: React-based chat interface with real-time communication
- 🚀 **Production Ready**: Docker containerization with deployment scripts
- 🔒 **Privacy Focused**: Your data stays local, only AI processing is external
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile devices

## 🏗️ Architecture

```
├── backend/          # FastAPI backend with AI integration
│   ├── services/     # OpenAI, Knowledge, and Voice services
│   ├── models.py     # Data models and schemas
│   ├── config.py     # Configuration management
│   └── main.py       # FastAPI application
├── frontend/         # React TypeScript frontend
│   ├── src/          # React components and logic
│   └── public/       # Static assets
├── data/            # Personal data and knowledge base
│   ├── personal_info.json      # Your personal information
│   └── conversation_examples.json # Response examples
├── scripts/         # Setup and deployment scripts
├── docs/           # Comprehensive documentation
└── docker/         # Docker configurations
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Node.js 16+
- Docker & Docker Compose
- OpenAI API Key

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd ai-persona
chmod +x scripts/*.sh
./scripts/setup.sh
```

### 2. Configure Your Information

Edit `data/personal_info.json` with your details:
- Personal information (name, location, contact)
- Work experience and achievements
- Skills and technologies
- Education and certifications
- Work authorization status
- Salary expectations and preferences

### 3. Set Up API Keys

```bash
cp env.example .env
# Edit .env with your OpenAI API key
OPENAI_API_KEY=your_openai_api_key_here
SECRET_KEY=your_secure_secret_key_here
```

### 4. Start the Application

**Development Mode:**
```bash
./scripts/start-dev.sh
```

**Production Mode:**
```bash
./scripts/start-prod.sh
```

### 5. Access Your AI Persona

- **Web Interface**: http://localhost:3000 (dev) or http://localhost:80 (prod)
- **API Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

## 🎯 How It Works

1. **Personal Data Loading**: Your information is loaded into a vector database for semantic search
2. **AI Processing**: OpenAI GPT-4 generates responses based on your profile and conversation context
3. **Voice Integration**: Speech-to-text converts voice input, text-to-speech provides audio responses
4. **Real-time Chat**: WebSocket-based communication for instant responses
5. **Knowledge Retrieval**: Vector search finds relevant information for each question

## 📖 Usage Examples

### Common Recruiter Questions Your AI Can Handle:

- "Tell me about yourself"
- "What are your technical skills?"
- "Do you require visa sponsorship?"
- "What are your salary expectations?"
- "When can you start?"
- "Why are you looking for a new role?"
- "What's your experience with [technology]?"
- "Tell me about a challenging project you worked on"

### Voice Features:

- **Voice Input**: Click microphone, speak your question
- **Voice Output**: Click play button to hear AI responses
- **Auto-play**: Enable automatic audio responses

## 🛠️ Technology Stack

### Backend
- **FastAPI**: Modern Python web framework
- **OpenAI API**: GPT-4 for conversations, Whisper for STT, TTS for voice
- **ChromaDB**: Vector database for semantic search
- **SQLite**: Local data storage
- **Redis**: Caching and session management

### Frontend
- **React 18**: Modern UI framework
- **TypeScript**: Type-safe development
- **Lucide React**: Beautiful icons
- **Axios**: HTTP client for API calls

### DevOps
- **Docker**: Containerization
- **Docker Compose**: Multi-container orchestration
- **Nginx**: Reverse proxy and static file serving
- **Health Checks**: Application monitoring

## 📚 Documentation

- **[User Guide](docs/user-guide.md)**: Complete guide to using your AI persona
- **[Deployment Guide](docs/deployment.md)**: Production deployment instructions
- **[API Documentation](http://localhost:8000/docs)**: Interactive API reference

## 🔧 Customization

### Personal Information
Edit `data/personal_info.json` to customize:
- Work experience and achievements
- Skills and technologies
- Education and certifications
- Job preferences and salary expectations
- Work authorization and location preferences

### AI Personality
Modify `data/conversation_examples.json` to adjust:
- Communication style and tone
- Response length and format
- Key phrases and expressions
- Conversation examples

### Voice Settings
Configure in `.env`:
- Voice model (alloy, echo, fable, onyx, nova, shimmer)
- Speech speed and pitch
- Auto-play preferences

## 🚀 Deployment Options

### Local Development
```bash
./scripts/start-dev.sh
```

### Docker Production
```bash
./scripts/start-prod.sh
```

### Cloud Deployment
- **AWS**: ECS, App Runner, or EC2
- **Google Cloud**: Cloud Run or GKE
- **Azure**: Container Instances or AKS
- **DigitalOcean**: App Platform or Droplets

See `docs/deployment.md` for detailed cloud deployment instructions.

## 🔒 Privacy & Security

- **Local Data**: Your personal information is stored locally
- **Encrypted Communication**: All API calls use HTTPS
- **No Data Retention**: Conversations are not permanently stored
- **API Key Security**: Secure environment variable management
- **Rate Limiting**: Built-in protection against abuse

## 📊 Monitoring & Analytics

- **Health Checks**: Built-in application monitoring
- **Logging**: Comprehensive application logs
- **Performance Metrics**: Response time and usage tracking
- **Error Handling**: Graceful error recovery

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

- **Documentation**: Check the `/docs` folder
- **Issues**: Report bugs via GitHub Issues
- **Discussions**: Join community discussions
- **Email**: Contact for enterprise support

## 🎉 What's Next?

Your AI Persona is now ready to help with recruiter conversations! Here are some next steps:

1. **Test Common Questions**: Use the quick action buttons to test responses
2. **Refine Your Profile**: Update personal information based on test results
3. **Customize Responses**: Adjust conversation examples for your style
4. **Deploy to Production**: Use the deployment scripts for a live version
5. **Monitor Usage**: Track API usage and optimize costs

**Happy job hunting! 🚀**
