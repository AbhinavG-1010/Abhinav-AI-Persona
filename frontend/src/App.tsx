import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Send, User, Bot, Linkedin, FileText, ExternalLink } from 'lucide-react';
import './App.css';

// Types
interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
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
  const [isConnected, setIsConnected] = useState(false);

  // Check API connection
  useEffect(() => {
    checkConnection();
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
        conversation_id: null
      });

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: (response.data as any).response,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error: any) {
      console.error('Failed to send message:', error);
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
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

  return (
    <div className="app">
      {/* Header */}
      <header className="app-header">
        <div className="header-content">
          <div className="profile-section">
            <img 
              src="/profile-picture.jpg" 
              alt="AI Abhinav" 
              className="profile-picture"
              onError={(e) => {
                e.currentTarget.style.display = 'none';
              }}
            />
            <div className="profile-info">
              <h1>AI Abhinav</h1>
              <div className="connection-status">
                <div className={`status-dot ${isConnected ? 'connected' : 'disconnected'}`}></div>
                <span>{isConnected ? 'Connected' : 'Disconnected'}</span>
              </div>
            </div>
          </div>
          
          {/* Social Links */}
          <div className="social-links">
            <a 
              href="https://www.linkedin.com/in/abhinavg22/" 
              target="_blank" 
              rel="noopener noreferrer"
              className="social-link linkedin"
            >
              <Linkedin size={20} />
              <span>LinkedIn</span>
              <ExternalLink size={14} />
            </a>
            <a 
              href="/resume.pdf" 
              target="_blank" 
              rel="noopener noreferrer"
              className="social-link resume"
            >
              <FileText size={20} />
              <span>Resume</span>
              <ExternalLink size={14} />
            </a>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="app-main">
        {/* Chat Area */}
        <div className="chat-container">
          <div className="messages">
            {messages.map((message) => (
              <div key={message.id} className={`message ${message.role}`}>
                <div className="message-avatar">
                  {message.role === 'user' ? (
                    <User size={20} />
                  ) : (
                    <Bot size={20} />
                  )}
                </div>
                <div className="message-content">
                  <p>{message.content}</p>
                </div>
              </div>
            ))}
            {isLoading && (
              <div className="message assistant">
                <div className="message-avatar">
                  <Bot size={20} />
                </div>
                <div className="message-content">
                  <div className="typing-indicator">
                    <span></span>
                    <span></span>
                    <span></span>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Input Area */}
          <form onSubmit={handleSubmit} className="input-form">
            <div className="input-container">
              <input
                type="text"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                placeholder="Type your message or ask about your background..."
                className="message-input"
                disabled={isLoading}
              />
              <button 
                type="submit" 
                className="send-button"
                disabled={isLoading || !inputMessage.trim()}
              >
                <Send size={20} />
              </button>
            </div>
          </form>

          {/* Quick Actions */}
          <div className="quick-actions">
            <h3>QUICK QUESTIONS</h3>
            <div className="quick-buttons">
              {[
                "About Me",
                "Skills", 
                "Work Ex",
                "Salary",
                "Availability",
                "Why Leaving"
              ].map((question) => (
                <button
                  key={question}
                  onClick={() => sendMessage(question)}
                  className="quick-button"
                  disabled={isLoading}
                >
                  {question}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;