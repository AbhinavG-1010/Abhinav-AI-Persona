import React from 'react';

function App() {
  return (
    <div style={{ 
      padding: '20px', 
      backgroundColor: '#1a1a1a', 
      color: 'white', 
      minHeight: '100vh',
      fontFamily: 'Arial, sans-serif'
    }}>
      <h1>AI Abhinav - Test Version</h1>
      <p>If you can see this, the React app is working!</p>
      <p>Backend URL: https://abhinav-ai-persona.onrender.com</p>
      <button 
        onClick={() => {
          fetch('https://abhinav-ai-persona.onrender.com/health')
            .then(response => response.json())
            .then(data => {
              alert('Backend connected: ' + JSON.stringify(data));
            })
            .catch(error => {
              alert('Backend error: ' + error.message);
            });
        }}
        style={{
          padding: '10px 20px',
          backgroundColor: '#10b981',
          color: 'white',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer'
        }}
      >
        Test Backend Connection
      </button>
    </div>
  );
}

export default App;
