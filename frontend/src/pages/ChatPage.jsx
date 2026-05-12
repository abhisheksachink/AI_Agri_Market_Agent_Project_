/**
 * Chat Page
 */

import React, { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import ChatBot from '../components/ChatBot';
import { AuthContext } from '../context/AuthContext';

export default function ChatPage() {
  const { token } = useContext(AuthContext);
  const navigate = useNavigate();

  if (!token) {
    return (
      <div className="container-custom py-20 text-center">
        <h1 className="text-3xl font-bold mb-4">Please Log In to Chat</h1>
        <button
          onClick={() => navigate('/login')}
          className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700"
        >
          Go to Login
        </button>
      </div>
    );
  }

  return (
    <div className="container-custom py-12">
      <h1 className="text-3xl font-bold mb-8">AI Agricultural Assistant</h1>
      <ChatBot />
    </div>
  );
}
