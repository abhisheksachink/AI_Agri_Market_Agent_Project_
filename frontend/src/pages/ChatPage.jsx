/**
 * Chat Page
 */

import React from 'react';
import ChatBot from '../components/ChatBot';

export default function ChatPage() {
  return (
    <div className="container-custom py-12">
      <h1 className="text-3xl font-bold mb-8">AI Agricultural Assistant</h1>
      <ChatBot />
    </div>
  );
}
