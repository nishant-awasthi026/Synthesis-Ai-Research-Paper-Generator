import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import {
    Plus,
    Search,
    MessageSquare,
    History,
    Upload,
    FileText,
    Bot,
    Send,
    Brain
} from 'lucide-react';
import { useAuthStore } from '../store';

const Dashboard = () => {
    const navigate = useNavigate();
    const user = useAuthStore((state) => state.user);
    const [papers, setPapers] = useState([]);
    const [searchQuery, setSearchQuery] = useState("");
    const [heroInput, setHeroInput] = useState("");

    // Fetch recent chats (papers)
    useEffect(() => {
        const fetchPapers = async () => {
            try {
                const response = await axios.get('http://localhost:8000/api/papers/list?limit=10');
                setPapers(response.data.papers || []);
            } catch (error) {
                console.error('Error fetching papers:', error);
            }
        };
        fetchPapers();
    }, []);

    const handleCreatePaper = async (title) => {
        if (!title.trim()) return;
        try {
            const payload = {
                title: title,
                domain: "General", // Default domain, can be inferred later
                paper_data: {}
            };
            const response = await axios.post('http://localhost:8000/api/papers/create', payload);
            if (response.data.status === 'success') {
                navigate(`/workflow/${response.data.paper_id}`);
            }
        } catch (error) {
            console.error("Error creating paper:", error);
        }
    };

    return (
        <div className="flex h-screen bg-gray-50 overflow-hidden font-sans">

            {/* SIDEBAR */}
            <aside className="w-[260px] bg-gray-50 flex flex-col border-r border-gray-200">
                {/* Logo Area */}
                <div className="h-16 flex items-center px-4">
                    <div className="flex items-center gap-2 font-semibold text-gray-700 text-lg">
                        <Brain className="h-6 w-6 text-gray-500" />
                        <span>Synthesis.ai</span>
                    </div>
                </div>

                {/* New Chat Button */}
                <div className="px-3 mb-2">
                    <button
                        onClick={() => setHeroInput("")} // Reset to Hero
                        className="flex items-center gap-2 w-full px-3 py-2 bg-white border border-gray-200 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-100 shadow-sm transition-colors text-left"
                    >
                        <Plus className="h-4 w-4" />
                        New Chat
                    </button>
                </div>

                {/* Search Bar */}
                <div className="px-3 mb-4">
                    <div className="relative">
                        <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-gray-400" />
                        <input
                            type="text"
                            placeholder="Find Chats"
                            className="w-full pl-9 pr-3 py-1.5 bg-gray-100 border-none rounded-md text-sm text-gray-700 focus:ring-0 focus:bg-white transition-colors"
                            value={searchQuery}
                            onChange={(e) => setSearchQuery(e.target.value)}
                        />
                    </div>
                </div>

                {/* Recent Chats List */}
                <div className="flex-1 overflow-y-auto px-3 pb-4">
                    <h3 className="text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2 px-1">
                        Recent Chats
                    </h3>
                    <div className="space-y-1">
                        {papers.map((paper) => (
                            <button
                                key={paper.id}
                                onClick={() => navigate(`/paper/${paper.id}`)}
                                className="flex items-center gap-3 w-full px-3 py-2 text-sm text-gray-600 rounded-md hover:bg-gray-200 transition-colors text-left group"
                            >
                                <History className="h-4 w-4 text-gray-400 group-hover:text-gray-600" />
                                <span className="truncate">{paper.title || "Untitled Research"}</span>
                            </button>
                        ))}
                        {papers.length === 0 && (
                            <div className="text-xs text-gray-400 px-3 py-2 italic">
                                No recent history
                            </div>
                        )}
                    </div>
                </div>

                {/* User/Settings Area (Optional) */}
                <div className="p-4 border-t border-gray-200">
                    <div className="flex items-center gap-2 text-sm text-gray-600">
                        <div className="h-8 w-8 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-600 font-semibold">
                            {user?.full_name?.charAt(0) || "U"}
                        </div>
                        <div className="font-medium truncate">{user?.full_name || "User"}</div>
                    </div>
                </div>
            </aside>

            {/* MAIN CONTENT */}
            <main className="flex-1 flex flex-col relative w-full h-full bg-white">

                {/* Scrollable Content Area */}
                <div className="flex-1 overflow-y-auto flex flex-col items-center justify-center p-4 pb-32">

                    {/* Hero Title */}
                    <div className="text-center mb-12 animate-fade-in-up">
                        <h1 className="text-5xl font-semibold text-gray-800 tracking-tight mb-2">
                            Generate Research Paper
                        </h1>
                        <p className="text-gray-400 text-lg font-light">
                            Generated patterns from 2000+ open access Research Paper sources
                        </p>

                        {/* Badges */}
                        <div className="flex flex-wrap justify-center gap-3 mt-6">
                            <span className="px-4 py-1.5 bg-gray-100 rounded-full text-xs font-medium text-gray-500 uppercase tracking-wide">
                                No Fake Generated Facts
                            </span>
                            <span className="px-4 py-1.5 bg-gray-100 rounded-full text-xs font-medium text-gray-500 uppercase tracking-wide">
                                No Fake Citations
                            </span>
                            <span className="px-4 py-1.5 bg-gray-100 rounded-full text-xs font-medium text-gray-500 uppercase tracking-wide">
                                Helping Researchers Not Replacing
                            </span>
                        </div>
                    </div>

                    {/* Action Cards */}
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 w-full max-w-4xl px-4">

                        {/* Option 1: File Upload */}
                        <div className="bg-blue-50 border border-blue-100 rounded-2xl p-6 flex flex-col items-center text-center hover:shadow-md transition-shadow cursor-pointer group">
                            <div className="flex items-center gap-2 text-blue-700 font-semibold text-lg mb-3">
                                <Upload className="h-6 w-6" />
                                <h3>Option 1: Upload File</h3>
                            </div>
                            <p className="text-gray-600 text-sm mb-6">
                                Upload .txt or .ipynb notebook for analysis and paper generation.
                            </p>
                            <button className="px-6 py-2 bg-blue-500 hover:bg-blue-600 text-white rounded-full font-medium text-sm transition-colors shadow-sm">
                                Browse Files
                            </button>
                        </div>

                        {/* Option 2: Chat Notebook */}
                        <div className="bg-green-50 border border-green-100 rounded-2xl p-6 flex flex-col items-center text-center hover:shadow-md transition-shadow cursor-pointer group">
                            <div className="flex items-center gap-2 text-green-700 font-semibold text-lg mb-3">
                                <MessageSquare className="h-6 w-6" />
                                <h3>Option 2: Create Notebook by Chat</h3>
                            </div>
                            <p className="text-gray-600 text-sm mb-6">
                                Interactively build a notebook through conversation.
                            </p>
                            <button className="px-6 py-2 bg-green-500 hover:bg-green-600 text-white rounded-full font-medium text-sm transition-colors shadow-sm">
                                Start Chatting
                            </button>
                        </div>
                    </div>
                </div>

                {/* Bottom Input Area (Fixed) */}
                <div className="absolute bottom-0 left-0 right-0 bg-white p-4 pb-8">
                    <div className="max-w-3xl mx-auto">
                        <div className="relative group">
                            <div className="absolute inset-y-0 left-4 flex items-center pointer-events-none">
                                <Search className="h-5 w-5 text-gray-400 group-focus-within:text-indigo-500 transition-colors" />
                            </div>
                            <input
                                type="text"
                                className="block w-full pl-12 pr-12 py-4 bg-gray-50 border border-gray-200 rounded-2xl text-gray-900 placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 focus:bg-white text-lg shadow-sm transition-all"
                                placeholder="Machine Learning in Oncology"
                                value={heroInput}
                                onChange={(e) => setHeroInput(e.target.value)}
                                onKeyDown={(e) => e.key === 'Enter' && handleCreatePaper(heroInput)}
                            />
                            <button
                                onClick={() => handleCreatePaper(heroInput)}
                                className="absolute inset-y-2 right-2 flex items-center justify-center h-10 w-10 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl transition-colors shadow-sm"
                            >
                                <Send className="h-5 w-5" />
                            </button>
                        </div>

                        {/* Similar Papers Suggestion (Step 1 Requirement) */}
                        {heroInput.length > 5 && (
                            <div className="mt-4 animate-fade-in">
                                <h3 className="text-sm font-semibold text-gray-500 mb-2 pl-1">Existing Similar Research Papers</h3>
                                <div className="space-y-2">
                                    <div className="flex items-center gap-2 p-3 bg-white border border-gray-100 rounded-lg shadow-sm text-sm text-gray-600">
                                        <FileText className="h-4 w-4 text-gray-400" />
                                        <span>Deep Learning Applications in Oncology: A Comprehensive Review (2023) - J. Smith et al.</span>
                                    </div>
                                    <div className="flex items-center gap-2 p-3 bg-white border border-gray-100 rounded-lg shadow-sm text-sm text-gray-600">
                                        <FileText className="h-4 w-4 text-gray-400" />
                                        <span>Predictive Modeling for Cancer Prognosis using Machine Learning (2022) - A. Kumar et al.</span>
                                    </div>
                                    <div className="flex items-center gap-2 p-3 bg-white border border-gray-100 rounded-lg shadow-sm text-sm text-gray-600">
                                        <FileText className="h-4 w-4 text-gray-400" />
                                        <span>AI-Driven Biomarker Discovery in Cancer Research (2024) - L. Chen et al.</span>
                                    </div>
                                </div>
                            </div>
                        )}

                        <div className="text-center mt-3">
                            <p className="text-sm text-gray-400">
                                This system assists in research but does not replace expert review.
                            </p>
                        </div>
                    </div>
                </div>

            </main>
        </div>
    );
};

export default Dashboard;
