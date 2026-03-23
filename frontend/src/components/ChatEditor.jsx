import React, { useState, useEffect, useRef } from 'react';
import { chatAPI } from '../api/client';
import { useChatStore } from '../store';

const ChatEditor = ({ paperId }) => {
    const [message, setMessage] = useState('');
    const [loading, setLoading] = useState(false);
    const [pendingEdit, setPendingEdit] = useState(null);

    const chatHistory = useChatStore((state) => state.chatHistory[paperId] || []);
    const addMessage = useChatStore((state) => state.addMessage);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    };

    useEffect(() => {
        scrollToBottom();
    }, [chatHistory]);

    useEffect(() => {
        // Load chat history on mount
        const loadHistory = async () => {
            try {
                const response = await chatAPI.getHistory(paperId);
                if (response.data.messages) {
                    useChatStore.setState((state) => ({
                        chatHistory: {
                            ...state.chatHistory,
                            [paperId]: response.data.messages,
                        },
                    }));
                }
            } catch (error) {
                console.error('Failed to load chat history:', error);
            }
        };
        loadHistory();
    }, [paperId]);

    const handleSend = async () => {
        if (!message.trim()) return;

        const userMessage = {
            role: 'user',
            message: message,
            timestamp: new Date().toISOString(),
        };

        addMessage(paperId, userMessage);
        setMessage('');
        setLoading(true);

        try {
            const response = await chatAPI.sendMessage(paperId, message);

            const assistantMessage = {
                role: 'assistant',
                message: response.data.response,
                timestamp: new Date().toISOString(),
            };

            addMessage(paperId, assistantMessage);

            // Check if there's a pending edit
            if (response.data.action === 'preview' && response.data.edit_result) {
                setPendingEdit(response.data.edit_result);
            }
        } catch (error) {
            const errorMessage = {
                role: 'assistant',
                message: `Error: ${error.response?.data?.detail || 'Failed to process message'}`,
                timestamp: new Date().toISOString(),
            };
            addMessage(paperId, errorMessage);
        } finally {
            setLoading(false);
        }
    };

    const handleApplyEdit = async () => {
        if (!pendingEdit) return;

        setLoading(true);

        try {
            await chatAPI.applyEdit(
                paperId,
                pendingEdit.section,
                pendingEdit.edited_content
            );

            const successMessage = {
                role: 'assistant',
                message: `✓ Edit applied to ${pendingEdit.section}`,
                timestamp: new Date().toISOString(),
            };

            addMessage(paperId, successMessage);
            setPendingEdit(null);
        } catch (error) {
            const errorMessage = {
                role: 'assistant',
                message: `Error applying edit: ${error.response?.data?.detail || 'Unknown error'}`,
                timestamp: new Date().toISOString(),
            };
            addMessage(paperId, errorMessage);
        } finally {
            setLoading(false);
        }
    };

    const handleKeyPress = (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    };

    const exampleCommands = [
        "Make the abstract more concise",
        "Rephrase the introduction in a formal tone",
        "Expand the methodology with more detail",
        "Fix grammar in the conclusion",
    ];

    return (
        <div className="bg-white rounded-lg shadow-md flex flex-col h-[600px]">
            {/* Header */}
            <div className="p-4 border-b bg-gradient-to-r from-indigo-600 to-purple-600 text-white rounded-t-lg">
                <h3 className="text-xl font-semibold mb-1">AI Paper Editor</h3>
                <p className="text-sm text-indigo-100">
                    Chat with AI to edit your paper sections
                </p>
            </div>

            {/* Chat Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
                {chatHistory.length === 0 ? (
                    <div className="text-center py-8">
                        <div className="text-gray-400 mb-4">
                            <svg className="mx-auto h-16 w-16" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
                            </svg>
                        </div>
                        <p className="text-gray-600 mb-4">Start editing with natural language!</p>
                        <div className="text-left max-w-md mx-auto">
                            <p className="text-sm font-semibold text-gray-700 mb-2">Try these commands:</p>
                            <ul className="text-sm text-gray-600 space-y-1">
                                {exampleCommands.map((cmd, idx) => (
                                    <li key={idx} className="flex items-start">
                                        <span className="text-indigo-600 mr-2">•</span>
                                        <button
                                            onClick={() => setMessage(cmd)}
                                            className="text-left hover:text-indigo-600"
                                        >
                                            "{cmd}"
                                        </button>
                                    </li>
                                ))}
                            </ul>
                        </div>
                    </div>
                ) : (
                    chatHistory.map((msg, idx) => (
                        <div
                            key={idx}
                            className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                        >
                            <div
                                className={`max-w-[80%] rounded-lg px-4 py-2 ${msg.role === 'user'
                                        ? 'bg-indigo-600 text-white'
                                        : 'bg-gray-100 text-gray-800'
                                    }`}
                            >
                                <p className="text-sm whitespace-pre-wrap">{msg.message}</p>
                                <p className={`text-xs mt-1 opacity-70`}>
                                    {new Date(msg.timestamp).toLocaleTimeString()}
                                </p>
                            </div>
                        </div>
                    ))
                )}

                {loading && (
                    <div className="flex justify-start">
                        <div className="bg-gray-100 rounded-lg px-4 py-2">
                            <div className="flex space-x-2">
                                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" />
                                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }} />
                                <div className="w-2 h-2 bg-gray-500 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }} />
                            </div>
                        </div>
                    </div>
                )}

                <div ref={messagesEndRef} />
            </div>

            {/* Pending Edit Action */}
            {pendingEdit && (
                <div className="p-4 bg-yellow-50 border-t border-yellow-200">
                    <div className="flex items-center justify-between">
                        <div className="text-sm">
                            <p className="font-semibold text-yellow-800">Edit Preview Ready</p>
                            <p className="text-yellow-700">
                                Section: {pendingEdit.section} ({pendingEdit.original_length} → {pendingEdit.edited_length} chars)
                            </p>
                        </div>
                        <div className="flex space-x-2">
                            <button
                                onClick={() => setPendingEdit(null)}
                                className="px-3 py-1 bg-gray-200 text-gray-700 text-sm rounded hover:bg-gray-300"
                            >
                                Cancel
                            </button>
                            <button
                                onClick={handleApplyEdit}
                                disabled={loading}
                                className="px-3 py-1 bg-green-600 text-white text-sm rounded hover:bg-green-700 disabled:opacity-50"
                            >
                                Apply Edit
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {/* Input Area */}
            <div className="p-4 border-t bg-gray-50 rounded-b-lg">
                <div className="flex space-x-2">
                    <textarea
                        value={message}
                        onChange={(e) => setMessage(e.target.value)}
                        onKeyPress={handleKeyPress}
                        placeholder="Type your editing command... (e.g., 'Make abstract shorter')"
                        rows={2}
                        className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500 resize-none"
                    />
                    <button
                        onClick={handleSend}
                        disabled={loading || !message.trim()}
                        className="px-6 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                    >
                        <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                        </svg>
                    </button>
                </div>
                <p className="text-xs text-gray-500 mt-2">
                    Press Enter to send, Shift+Enter for new line
                </p>
            </div>
        </div>
    );
};

export default ChatEditor;
