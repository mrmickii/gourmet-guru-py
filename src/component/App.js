import React, { useState } from 'react';
import './App.css';
import axios from 'axios';

function App() {
  const [chatHistory, setChatHistory] = useState([]);
  const [userInput, setUserInput] = useState('');

  const handleUserInput = (e) => {
    setUserInput(e.target.value);
  };

  const handleSubmission = async () => {
    if (userInput.trim() === '') return;

    const userMessage = { sender: 'User', text: userInput };
    const newChatHistory = [...chatHistory, userMessage];
    setChatHistory(newChatHistory);

    try {
      const response = await axios.post('http://127.0.0.1:5000/chat', { message: userInput });
      const botMessage = { sender: 'Bot', text: response.data.message };
      setChatHistory([...newChatHistory, botMessage]);
    } catch (error) {
      console.error('Error communicating with backend', error);
    }

    setUserInput('');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      handleSubmission();
    }
  };

  return (
    <div className="app">
      <div className='title'>Gourmet Guru</div>
      <div className='bg-image'></div>
      <div className="chat-window">
        <div className="chat-history">
          {chatHistory.map((msg, index) => (
            <div key={index} className={`chat-message ${msg.sender.toLowerCase()}`}>
              <div className="message-sender">{msg.sender}:</div>
              <div className="message-text">{msg.text}</div>
            </div>
          ))}
        </div>
        <div className="chat-input">
          <input
            type="text"
            value={userInput}
            onChange={handleUserInput}
            onKeyDown={handleKeyDown}
            placeholder="Type your message..."
          />
          <button onClick={handleSubmission}>Send</button>
        </div>
      </div>
      <footer>
          <h4>Created by:</h4>
          <p>Carlo R. Garcia</p>
          <p>Ken Alger Dimaymay</p>
          <p>John Benedict Damalerio</p>
      </footer>
    </div>
  );
}

export default App;
