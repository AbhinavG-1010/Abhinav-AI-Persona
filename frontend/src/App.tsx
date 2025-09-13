import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { Send, Mic, MicOff, Play, User, Bot, Settings, Linkedin, FileText, ExternalLink } from 'lucide-react';
import './App.css';

// Types
interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  audioUrl?: string;
}

interface PersonalInfo {
  personal_details: {
    name: string;
    location: string;
    email: string;
    phone: string;
  };
  professional_summary: {
    title: string;
    years_experience: number;
    summary: string;
    key_skills: string[];
  };
  work_authorization: {
    status: string;
    visa_type: string;
    sponsorship_required: boolean;
  };
}

const API_BASE_URL = 'https://abhinav-ai-persona.onrender.com';

function App() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: "Hello! I'm AI Abhinav. I'm ready to help with answering any question about Abhinav's background, work experience, and preferences. How can I assist you today?",
      timestamp: new Date()
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isRecording, setIsRecording] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [personalInfo, setPersonalInfo] = useState<PersonalInfo | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [showSidebar, setShowSidebar] = useState(true);
  
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioRef = useRef<HTMLAudioElement>(null);

  // Scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Check API connection and load personal info
  useEffect(() => {
    checkConnection();
    loadPersonalInfo();
  }, []);

  const checkConnection = async () => {
    try {
      console.log('Checking connection to:', `${API_BASE_URL}/health`);
      const response = await axios.get(`${API_BASE_URL}/health`);
      console.log('Connection successful:', response.data);
      setIsConnected(true);
    } catch (error: any) {
      console.error('API connection failed:', error);
      console.error('Error details:', error.response?.data);
      setIsConnected(false);
    }
  };

  const loadPersonalInfo = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/personal-info`);
      setPersonalInfo(response.data as PersonalInfo);
    } catch (error) {
      console.error('Failed to load personal info:', error);
    }
  };

  const sendMessage = async (content: string) => {
    if (!content.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: content.trim(),
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await axios.post(`${API_BASE_URL}/conversation`, {
        message: content.trim(),
        conversation_id: conversationId,
        include_voice: true
      });

      const responseData = response.data as any;

      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: responseData.message,
        timestamp: new Date(),
        audioUrl: responseData.audio_url
      };

      setMessages(prev => [...prev, aiMessage]);
      setConversationId(responseData.conversation_id);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: "I apologize, but I'm having trouble connecting to the server. Please try again.",
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    sendMessage(inputMessage);
  };

  const handleQuickAction = (message: string) => {
    sendMessage(message);
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      
      const audioChunks: BlobPart[] = [];
      
      mediaRecorder.ondataavailable = (event) => {
        audioChunks.push(event.data);
      };
      
      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        const formData = new FormData();
        formData.append('audio_file', audioBlob, 'recording.wav');
        
        try {
          const response = await axios.post(`${API_BASE_URL}/voice/transcribe`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
          });
          
          const responseData = response.data as any;
          if (responseData.text) {
            sendMessage(responseData.text);
          }
        } catch (error) {
          console.error('Error transcribing audio:', error);
        }
        
        stream.getTracks().forEach(track => track.stop());
      };
      
      mediaRecorder.start();
      setIsRecording(true);
    } catch (error) {
      console.error('Error accessing microphone:', error);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && isRecording) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const playAudio = (audioUrl: string) => {
    if (audioRef.current) {
      audioRef.current.src = audioUrl;
      audioRef.current.play();
    }
  };

  return (
    <div className="app">
      {/* Header */}
      <header className="app-header">
        <div className="header-content">
          <div className="header-left">
            <button 
              className="sidebar-toggle"
              onClick={() => setShowSidebar(!showSidebar)}
            >
              <Settings size={20} />
            </button>
            <div className="header-brand">
              <div className="profile-avatar-header">
                <img 
                  src="/profile-picture.jpg" 
                  alt="Abhinav Gupta" 
                  className="profile-img"
                  onError={(e) => {
                    const target = e.target as HTMLImageElement;
                    target.style.display = 'none';
                    target.nextElementSibling?.classList.remove('hidden');
                  }}
                />
                <div className="profile-fallback hidden">
                  <User size={20} />
                </div>
              </div>
              <div className="brand-text">
                <h1>AI Abhinav</h1>
              </div>
            </div>
          </div>
          <div className="status-indicator">
            <div className={`status-dot ${isConnected ? 'connected' : 'disconnected'}`} />
            <span>{isConnected ? 'Connected' : 'Disconnected'}</span>
          </div>
        </div>
      </header>

      <div className="app-body">
        {/* Sidebar */}
        {showSidebar && (
          <aside className="sidebar">
            <div className="sidebar-content">
              {/* Profile Section */}
              <div className="profile-section">
                <div className="profile-avatar-large">
                  <img 
                    src="/profile-picture.jpg" 
                    alt="Abhinav Gupta" 
                    className="profile-img-large"
                    onError={(e) => {
                      const target = e.target as HTMLImageElement;
                      target.style.display = 'none';
                      target.nextElementSibling?.classList.remove('hidden');
                    }}
                  />
                  <div className="profile-fallback-large hidden">
                    <User size={40} />
                  </div>
                </div>
                
                {personalInfo && (
                  <div className="profile-info">
                    <h2 className="profile-name">{personalInfo.personal_details.name}</h2>
                    <p className="profile-title">{personalInfo.professional_summary.title}</p>
                    <p className="profile-location">{personalInfo.personal_details.location}</p>
                    
                    {/* Contact Information */}
                    <div className="contact-info">
                      <p className="contact-item">
                        <span className="contact-label">Email:</span>
                        <span className="contact-value">{personalInfo.personal_details.email}</span>
                      </p>
                      <p className="contact-item">
                        <span className="contact-label">Phone:</span>
                        <span className="contact-value">{personalInfo.personal_details.phone}</span>
                      </p>
                    </div>
                  </div>
                )}

                {/* Social Links */}
                <div className="social-links">
                  <a 
                    href="https://www.linkedin.com/in/abhinavg22/" 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="social-btn linkedin"
                  >
                    <Linkedin size={18} />
                    LinkedIn
                    <ExternalLink size={14} />
                  </a>
                  <a 
                    href="/resume.pdf" 
          target="_blank"
          rel="noopener noreferrer"
                    className="social-btn resume"
                  >
                    <FileText size={18} />
                    Resume
                    <ExternalLink size={14} />
                  </a>
                </div>
              </div>

            </div>
          </aside>
        )}

        {/* Main Chat */}
        <main className="chat-container">
          <div className="chat-messages">
            {messages.map((message) => (
              <div key={message.id} className={`message ${message.role}-message`}>
                <div className="message-avatar">
                  {message.role === 'user' ? (
                    <User size={16} />
                  ) : (
                    <img 
                      src="/profile-picture.jpg" 
                      alt="AI Abhinav" 
                      className="ai-avatar-img"
                      onError={(e) => {
                        const target = e.target as HTMLImageElement;
                        target.style.display = 'none';
                        target.nextElementSibling?.classList.remove('hidden');
                      }}
                    />
                  )}
                  {message.role === 'assistant' && (
                    <div className="ai-avatar-fallback hidden">
                      <Bot size={16} />
                    </div>
                  )}
                </div>
                <div className="message-content">
                  <p>{message.content}</p>
                  <div className="message-footer">
                    <span className="message-time">
                      {message.timestamp.toLocaleTimeString()}
                    </span>
                    {message.audioUrl && (
                      <button 
                        className="play-audio-btn"
                        onClick={() => playAudio(message.audioUrl!)}
                        title="Play audio"
                      >
                        <Play size={14} />
                      </button>
                    )}
                  </div>
                </div>
              </div>
            ))}
            
            {isLoading && (
              <div className="message assistant-message">
                <div className="message-avatar">
                  <img 
                    src="/profile-picture.jpg" 
                    alt="AI Abhinav" 
                    className="ai-avatar-img"
                    onError={(e) => {
                      const target = e.target as HTMLImageElement;
                      target.style.display = 'none';
                      target.nextElementSibling?.classList.remove('hidden');
                    }}
                  />
                  <div className="ai-avatar-fallback hidden">
                    <Bot size={16} />
                  </div>
                </div>
                <div className="message-content">
                  <div className="typing-indicator">
                    <span>AI is typing</span>
                    <div className="typing-dots">
                      <div className="typing-dot"></div>
                      <div className="typing-dot"></div>
                      <div className="typing-dot"></div>
                    </div>
                  </div>
                </div>
              </div>
            )}
            
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="input-container">
            <form onSubmit={handleSubmit} className="input-form">
              <div className="input-wrapper">
                <button
                  type="button"
                  className={`voice-btn ${isRecording ? 'recording' : ''}`}
                  onClick={isRecording ? stopRecording : startRecording}
                  disabled={isLoading}
                >
                  {isRecording ? <MicOff size={16} /> : <Mic size={16} />}
                </button>
                
                <textarea
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  placeholder="Type your message or ask about your background..."
                  className="message-input"
                  rows={1}
                  disabled={isLoading}
                />
                
                <button 
                  type="submit" 
                  className="send-btn"
                  disabled={!inputMessage.trim() || isLoading}
                >
                  <Send size={16} />
                </button>
              </div>
            </form>
            
            {/* Quick Actions */}
            <div className="quick-actions-bottom">
              <h4>Quick Questions</h4>
              <div className="quick-actions-grid">
                <button 
                  className="quick-btn-bottom"
                  onClick={() => handleQuickAction("Tell me about yourself")}
                >
                  About Me
                </button>
                <button 
                  className="quick-btn-bottom"
                  onClick={() => handleQuickAction("What are your technical skills?")}
                >
                  Skills
                </button>
                <button 
                  className="quick-btn-bottom"
                  onClick={() => handleQuickAction("Do you require visa sponsorship?")}
                >
                  Work Auth
                </button>
                <button 
                  className="quick-btn-bottom"
                  onClick={() => handleQuickAction("What are your salary expectations?")}
                >
                  Salary
                </button>
                <button 
                  className="quick-btn-bottom"
                  onClick={() => handleQuickAction("When can you start?")}
                >
                  Availability
                </button>
                <button 
                  className="quick-btn-bottom"
                  onClick={() => handleQuickAction("Why are you looking for a new role?")}
                >
                  Why Leaving
                </button>
              </div>
            </div>
          </div>
        </main>
      </div>

      {/* Audio element for playback */}
      <audio ref={audioRef} />
    </div>
  );
}

export default App;