// src/components/ChatBox.js

import React, { useState } from 'react';
import axios from 'axios';
import { TextField, Button, Box, Typography } from '@mui/material';

const ChatBox = () => {
  const [messages, setMessages] = useState([]); // To store conversation
  const [input, setInput] = useState(''); // To manage user input

  // Send message to backend and receive response
  const sendMessage = async () => {
    if (!input) return; // Don't send empty messages

    // Add user message to chat
    setMessages([...messages, { text: input, sender: 'user' }]);

    try {
      // Call backend API
      const response = await axios.post('/api/query', { message: input });

      // Add bot response to chat
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: response.data.reply, sender: 'bot' }
      ]);
    } catch (error) {
      console.error("Error fetching response:", error);
      setMessages((prevMessages) => [
        ...prevMessages,
        { text: "Error connecting to server", sender: 'bot' }
      ]);
    }

    // Clear input field
    setInput('');
  };

  return (
    <Box sx={{ p: 2, maxWidth: '600px', margin: 'auto', border: '1px solid #ccc', borderRadius: '8px' }}>
      <Typography variant="h4" gutterBottom>Chat</Typography>

      {/* Chat Messages */}
      <Box sx={{ maxHeight: '400px', overflowY: 'auto', mb: 2 }}>
        {messages.map((msg, index) => (
          <Box
            key={index}
            sx={{
              textAlign: msg.sender === 'user' ? 'right' : 'left',
              mb: 1,
              padding: '8px',
              borderRadius: '5px',
              bgcolor: msg.sender === 'user' ? 'primary.light' : 'grey.200'
            }}
          >
            <Typography>{msg.text}</Typography>
          </Box>
        ))}
      </Box>

      {/* Input Field and Send Button */}
      <Box sx={{ display: 'flex', alignItems: 'center' }}>
        <TextField
          fullWidth
          variant="outlined"
          placeholder="Type a message..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' ? sendMessage() : null}
        />
        <Button variant="contained" color="primary" onClick={sendMessage} sx={{ ml: 1 }}>
          Send
        </Button>
      </Box>
    </Box>
  );
};

export default ChatBox;
