import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { api } from '../api';
import {
    Send, Paperclip, FileText, FileDown,
    MessageSquare, PlusCircle, LayoutDashboard,
    Brain, FileSearch, Sparkles
} from 'lucide-react';

const ChatApp = () => {
    const [sessions, setSessions] = useState([]);
    const [currentSessionId, setCurrentSessionId] = useState(null);
    const [messages, setMessages] = useState([]);
    const [currentDocId, setCurrentDocId] = useState(null);
    const [currentDocName, setCurrentDocName] = useState(null);

    const [inputMessage, setInputMessage] = useState('');
    const [isUploading, setIsUploading] = useState(false);
    const [isThinking, setIsThinking] = useState(false);

    const fileInputRef = useRef(null);
    const messagesEndRef = useRef(null);

    // Initial load
    useEffect(() => {
        fetchHistory();
    }, []);

    // Auto-scroll
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages, isThinking]);

    const fetchHistory = async () => {
        try {
            const res = await api.getHistory();
            setSessions(res.data);
        } catch (e) {
            console.error(e);
        }
    };

    const handleNewChat = () => {
        setCurrentSessionId(null);
        setMessages([]);
        setCurrentDocId(null);
        setCurrentDocName(null);
    };

    const loadSession = async (id) => {
        try {
            const res = await api.loadSession(id);
            setCurrentSessionId(id);
            setMessages(res.data.messages || []);
            // Reset doc context on old chat load
            setCurrentDocId(null);
        } catch (e) {
            console.error(e);
        }
    };

    const handleFileUpload = async (e) => {
        const file = e.target.files[0];
        if (!file) return;

        setIsUploading(true);
        try {
            const res = await api.uploadDocument(file);
            setCurrentDocId(res.data.document_id);
            setCurrentDocName(file.name);

            // Optional: Add a system message notifying user of upload
            setMessages(prev => [...prev, {
                role: 'assistant',
                isSystemMessage: true,
                content: `Successfully uploaded ${file.name}. You can now query it.`,
            }]);
        } catch (err) {
            alert("Error uploading file");
        } finally {
            setIsUploading(false);
            e.target.value = null; // reset input
        }
    };

    const handleSendMessage = async (e) => {
        e.preventDefault();
        if (!inputMessage.trim() || isThinking) return;

        const userMsg = inputMessage;
        setInputMessage('');

        // Add user message to UI immediately
        setMessages(prev => [...prev, { role: 'user', content: userMsg }]);
        setIsThinking(true);

        try {
            const res = await api.chatWithDocs(userMsg, currentSessionId, currentDocId);

            if (!currentSessionId && res.data.session_id) {
                setCurrentSessionId(res.data.session_id);
                fetchHistory(); // refresh sidebar list
            }

            // Add assistant response
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: res.data.answer,
                sources: res.data.sources
            }]);
        } catch (err) {
            console.error(err);
            setMessages(prev => [...prev, {
                role: 'assistant',
                isError: true,
                content: "Sorry, I encountered an error communicating with the server."
            }]);
        } finally {
            setIsThinking(false);
        }
    };

    const handleSummarize = async () => {
        if (!currentDocId) return;
        setIsThinking(true);
        try {
            const res = await api.summarizeDoc(currentDocId);
            setMessages(prev => [...prev, {
                role: 'assistant',
                isSystemMessage: true,
                content: `**Summary of ${currentDocName}:**\n\n${res.data.summary}`
            }]);
        } catch (e) {
            alert("Failed to summarize");
        } finally {
            setIsThinking(false);
        }
    };

    return (
        <div className="flex h-screen w-full bg-pastel-background">

            {/* Sidebar Navigation */}
            <aside className="w-80 border-r border-pastel-pink/50 bg-white/60 backdrop-blur-xl flex flex-col shadow-sm z-10">
                <div className="p-6 border-b border-gray-100 flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-400 to-pastel-purple flex items-center justify-center text-white shadow-md">
                        <Brain size={24} />
                    </div>
                    <span className="font-bold text-xl tracking-tight text-pastel-dark">Retrievia</span>
                </div>

                <div className="p-4 flex-1 flex flex-col gap-6 overflow-y-auto">
                    {/* Action Area */}
                    <div className="space-y-3">
                        <button
                            onClick={handleNewChat}
                            className="w-full flex items-center justify-center gap-2 bg-pastel-deep text-white px-4 py-3 rounded-xl font-medium shadow-sm hover:bg-pastel-dark transition-colors"
                        >
                            <PlusCircle size={18} /> New Conversation
                        </button>
                        <input
                            type="file"
                            className="hidden"
                            ref={fileInputRef}
                            onChange={handleFileUpload}
                            accept=".txt,.pdf,.md"
                        />
                        <button
                            onClick={() => fileInputRef.current?.click()}
                            disabled={isUploading}
                            className="w-full flex items-center justify-center gap-2 bg-white border border-gray-200 text-pastel-gray px-4 py-3 rounded-xl font-medium shadow-sm hover:border-pastel-purple hover:text-pastel-deep transition-colors disabled:opacity-50"
                        >
                            <Paperclip size={18} /> {isUploading ? "Uploading..." : "Attach Document"}
                        </button>
                    </div>

                    {/* Context Display */}
                    <AnimatePresence>
                        {currentDocId && (
                            <motion.div
                                initial={{ opacity: 0, height: 0 }}
                                animate={{ opacity: 1, height: 'auto' }}
                                exit={{ opacity: 0, height: 0 }}
                                className="bg-indigo-50/50 rounded-xl p-4 border border-indigo-100"
                            >
                                <div className="flex items-center gap-2 mb-2">
                                    <FileText size={16} className="text-pastel-deep" />
                                    <span className="text-sm font-semibold text-pastel-dark truncate">Active File</span>
                                </div>
                                <p className="text-xs text-pastel-gray truncate mb-3">{currentDocName}</p>
                                <button
                                    onClick={handleSummarize}
                                    className="w-full bg-white text-xs font-medium px-3 py-2 rounded-lg border border-indigo-100 text-indigo-600 hover:bg-indigo-50 transition-colors flex items-center justify-center gap-1"
                                >
                                    <Sparkles size={14} /> Quick Summary
                                </button>
                            </motion.div>
                        )}
                    </AnimatePresence>

                    {/* History List */}
                    <div className="flex-1">
                        <h3 className="text-xs font-semibold uppercase tracking-wider text-gray-400 mb-3 px-2">History</h3>
                        <div className="space-y-1">
                            {sessions.map(s => (
                                <button
                                    key={s.id}
                                    onClick={() => loadSession(s.id)}
                                    className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-xl text-sm transition-colors text-left ${currentSessionId === s.id
                                            ? 'bg-pastel-deep/10 text-pastel-dark font-medium'
                                            : 'text-gray-600 hover:bg-gray-50'
                                        }`}
                                >
                                    <MessageSquare size={16} className={currentSessionId === s.id ? 'text-pastel-deep' : 'text-gray-400'} />
                                    <span className="truncate">{s.title}</span>
                                </button>
                            ))}
                        </div>
                    </div>
                </div>
            </aside>

            {/* Main Chat Area */}
            <main className="flex-1 flex flex-col relative bg-white m-4 rounded-3xl shadow-xl border border-gray-100 overflow-hidden">
                {/* Chat History View */}
                <div className="flex-1 overflow-y-auto p-6 md:p-8 space-y-6">
                    {messages.length === 0 ? (
                        <div className="h-full flex flex-col items-center justify-center text-center text-gray-400">
                            <div className="w-16 h-16 bg-gray-50 rounded-full flex items-center justify-center mb-4">
                                <LayoutDashboard size={32} className="text-pastel-purple" />
                            </div>
                            <p className="font-medium text-lg text-gray-500 mb-1">Welcome to a fresh space</p>
                            <p className="text-sm">Attach a document on the left, or just say hello!</p>
                        </div>
                    ) : (
                        messages.map((msg, idx) => (
                            <motion.div
                                key={idx}
                                initial={{ opacity: 0, y: 10 }}
                                animate={{ opacity: 1, y: 0 }}
                                className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}
                            >
                                <div
                                    className={`
                    max-w-[80%] rounded-2xl px-5 py-4 
                    ${msg.isSystemMessage
                                            ? 'bg-amber-50 border border-amber-100 text-amber-900 mx-auto w-full text-center text-sm'
                                            : msg.isError
                                                ? 'bg-red-50 text-red-600 border border-red-100'
                                                : msg.role === 'user'
                                                    ? 'bg-gradient-to-br from-pastel-deep to-indigo-500 text-white shadow-md'
                                                    : 'bg-pastel-pink/20 text-pastel-dark border border-pastel-pink/30 shadow-sm'
                                        }
                  `}
                                >
                                    <div className="prose prose-sm max-w-none break-words" dangerouslySetInnerHTML={{ __html: msg.content.replace(/\n/g, '<br/>') }} />

                                    {/* Sources Accordion */}
                                    {msg.sources && msg.sources.length > 0 && (
                                        <div className="mt-4 pt-3 border-t border-black/5">
                                            <details className="text-xs group">
                                                <summary className="cursor-pointer font-medium text-pastel-deep flex items-center gap-1 select-none">
                                                    <FileSearch size={14} /> Show {msg.sources.length} Reference(s)
                                                </summary>
                                                <ul className="mt-2 space-y-2 list-disc list-inside">
                                                    {msg.sources.map((s, i) => (
                                                        <li key={i} className="text-gray-500 italic bg-white/50 p-2 rounded border border-white">
                                                            <span className="font-semibold text-gray-700 not-italic mr-1">Doc {s.document_id.substring(0, 6)}:</span>
                                                            {s.text}
                                                        </li>
                                                    ))}
                                                </ul>
                                            </details>
                                        </div>
                                    )}
                                </div>
                            </motion.div>
                        ))
                    )}

                    {isThinking && (
                        <motion.div
                            initial={{ opacity: 0 }} animate={{ opacity: 1 }}
                            className="flex justify-start"
                        >
                            <div className="bg-gray-100 rounded-2xl px-5 py-4 flex gap-2 items-center text-gray-500">
                                <div className="w-2 h-2 bg-pastel-deep rounded-full animate-bounce" />
                                <div className="w-2 h-2 bg-pastel-deep rounded-full animate-bounce delay-100" />
                                <div className="w-2 h-2 bg-pastel-deep rounded-full animate-bounce delay-200" />
                            </div>
                        </motion.div>
                    )}
                    <div ref={messagesEndRef} />
                </div>

                {/* Input Area */}
                <div className="p-4 bg-white/80 backdrop-blur-md border-t border-gray-100 absolute bottom-0 w-full left-0 z-10">
                    <form onSubmit={handleSendMessage} className="max-w-4xl mx-auto relative">
                        <input
                            type="text"
                            value={inputMessage}
                            onChange={(e) => setInputMessage(e.target.value)}
                            placeholder="Ask Retrievia..."
                            className="w-full bg-gray-50 border border-gray-200 text-gray-800 rounded-full pl-6 pr-14 py-4 focus:outline-none focus:ring-2 focus:ring-pastel-purple/50 focus:border-pastel-purple transition-all shadow-inner"
                            disabled={isThinking}
                        />
                        <button
                            type="submit"
                            disabled={!inputMessage.trim() || isThinking}
                            className="absolute right-2 top-2 bottom-2 aspect-square bg-pastel-deep text-white rounded-full flex items-center justify-center hover:bg-pastel-dark transition-colors disabled:opacity-40 shadow-sm"
                        >
                            <Send size={18} className="translate-x-[-1px] translate-y-[1px]" />
                        </button>
                    </form>
                </div>
            </main>
        </div>
    );
};

export default ChatApp;
