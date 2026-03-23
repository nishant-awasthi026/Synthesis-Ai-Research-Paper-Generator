import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { papersAPI } from '../api/client';
import { usePaperStore } from '../store';
import FileUpload from '../components/FileUpload';
import ValidationDashboard from '../components/ValidationDashboard';
import ChatEditor from '../components/ChatEditor';
import ExportPanel from '../components/ExportPanel';

const PaperEditor = () => {
    const { paperId } = useParams();
    const [activeTab, setActiveTab] = useState('upload');
    const [loading, setLoading] = useState(true);

    const currentPaper = usePaperStore((state) => state.currentPaper);
    const setCurrentPaper = usePaperStore((state) => state.setCurrentPaper);

    useEffect(() => {
        // Load paper data
        const loadPaper = async () => {
            try {
                const response = await papersAPI.getOne(paperId);
                setCurrentPaper(response.data);
            } catch (error) {
                console.error('Failed to load paper:', error);
            } finally {
                setLoading(false);
            }
        };

        if (paperId) {
            loadPaper();
        }
    }, [paperId, setCurrentPaper]);

    const tabs = [
        { id: 'upload', label: 'Upload Results', icon: '📤' },
        { id: 'validate', label: 'Validation', icon: '✓' },
        { id: 'chat', label: 'AI Editor', icon: '💬' },
        { id: 'export', label: 'Export', icon: '📄' },
    ];

    if (loading) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="text-center">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
                    <p className="mt-4 text-gray-600">Loading paper...</p>
                </div>
            </div>
        );
    }

    if (!currentPaper) {
        return (
            <div className="flex items-center justify-center min-h-screen">
                <div className="text-center text-red-600">
                    <p className="text-xl font-semibold">Paper not found</p>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gray-50">
            {/* Header */}
            <div className="bg-white shadow">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
                    <div className="flex items-center justify-between">
                        <div>
                            <h1 className="text-2xl font-bold text-gray-900">
                                {currentPaper.title}
                            </h1>
                            <p className="text-sm text-gray-600 mt-1">
                                {currentPaper.domain || 'No domain specified'} • Status: {currentPaper.status}
                            </p>
                        </div>
                        <div className="flex items-center space-x-2">
                            <span className={`px-3 py-1 rounded-full text-xs font-semibold ${currentPaper.status === 'published'
                                    ? 'bg-green-100 text-green-800'
                                    : currentPaper.status === 'review'
                                        ? 'bg-yellow-100 text-yellow-800'
                                        : 'bg-gray-100 text-gray-800'
                                }`}>
                                {currentPaper.status?.toUpperCase() || 'DRAFT'}
                            </span>
                        </div>
                    </div>
                </div>
            </div>

            {/* Tabs */}
            <div className="bg-white border-b">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <nav className="flex space-x-8" aria-label="Tabs">
                        {tabs.map((tab) => (
                            <button
                                key={tab.id}
                                onClick={() => setActiveTab(tab.id)}
                                className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${activeTab === tab.id
                                        ? 'border-indigo-600 text-indigo-600'
                                        : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                                    }`}
                            >
                                <span className="mr-2">{tab.icon}</span>
                                {tab.label}
                            </button>
                        ))}
                    </nav>
                </div>
            </div>

            {/* Content */}
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
                    {/* Main Content Area */}
                    <div className="lg:col-span-2">
                        {activeTab === 'upload' && <FileUpload paperId={paperId} />}
                        {activeTab === 'validate' && <ValidationDashboard paperId={paperId} />}
                        {activeTab === 'chat' && <ChatEditor paperId={paperId} />}
                        {activeTab === 'export' && <ExportPanel paperId={paperId} paperTitle={currentPaper.title} />}
                    </div>

                    {/* Sidebar */}
                    <div className="space-y-6">
                        {/* Paper Info Card */}
                        <div className="bg-white rounded-lg shadow-md p-6">
                            <h3 className="font-semibold text-gray-900 mb-4">Paper Info</h3>
                            <dl className="space-y-3 text-sm">
                                <div>
                                    <dt className="text-gray-600">Created</dt>
                                    <dd className="text-gray-900">
                                        {new Date(currentPaper.created_at).toLocaleDateString()}
                                    </dd>
                                </div>
                                <div>
                                    <dt className="text-gray-600">Last Updated</dt>
                                    <dd className="text-gray-900">
                                        {new Date(currentPaper.updated_at).toLocaleDateString()}
                                    </dd>
                                </div>
                                {currentPaper.novelty_score !== undefined && (
                                    <div>
                                        <dt className="text-gray-600">Novelty Score</dt>
                                        <dd className="text-gray-900">
                                            {(currentPaper.novelty_score * 100).toFixed(0)}%
                                        </dd>
                                    </div>
                                )}
                                {currentPaper.plagiarism_score !== undefined && (
                                    <div>
                                        <dt className="text-gray-600">Plagiarism Score</dt>
                                        <dd className={`font-semibold ${currentPaper.plagiarism_score < 0.3
                                                ? 'text-green-600'
                                                : currentPaper.plagiarism_score < 0.7
                                                    ? 'text-yellow-600'
                                                    : 'text-red-600'
                                            }`}>
                                            {(currentPaper.plagiarism_score * 100).toFixed(0)}%
                                        </dd>
                                    </div>
                                )}
                            </dl>
                        </div>

                        {/* Quick Actions */}
                        <div className="bg-white rounded-lg shadow-md p-6">
                            <h3 className="font-semibold text-gray-900 mb-4">Quick Actions</h3>
                            <div className="space-y-2">
                                <button
                                    onClick={() => setActiveTab('upload')}
                                    className="w-full text-left px-4 py-2 text-sm bg-gray-50 hover:bg-gray-100 rounded transition-colors"
                                >
                                    📤 Upload Results
                                </button>
                                <button
                                    onClick={() => setActiveTab('validate')}
                                    className="w-full text-left px-4 py-2 text-sm bg-gray-50 hover:bg-gray-100 rounded transition-colors"
                                >
                                    ✓ Run Validation
                                </button>
                                <button
                                    onClick={() => setActiveTab('chat')}
                                    className="w-full text-left px-4 py-2 text-sm bg-gray-50 hover:bg-gray-100 rounded transition-colors"
                                >
                                    💬 Edit with AI
                                </button>
                                <button
                                    onClick={() => setActiveTab('export')}
                                    className="w-full text-left px-4 py-2 text-sm bg-gray-50 hover:bg-gray-100 rounded transition-colors"
                                >
                                    📄 Export Paper
                                </button>
                            </div>
                        </div>

                        {/* Workflow Guide */}
                        <div className="bg-gradient-to-br from-indigo-50 to-purple-50 rounded-lg border border-indigo-200 p-6">
                            <h3 className="font-semibold text-indigo-900 mb-3">Responsible Workflow</h3>
                            <ol className="space-y-2 text-sm text-indigo-800">
                                <li className="flex items-start">
                                    <span className="mr-2">1.</span>
                                    <span>Upload real experimental results</span>
                                </li>
                                <li className="flex items-start">
                                    <span className="mr-2">2.</span>
                                    <span>Run validation checks</span>
                                </li>
                                <li className="flex items-start">
                                    <span className="mr-2">3.</span>
                                    <span>Refine with AI chat editor</span>
                                </li>
                                <li className="flex items-start">
                                    <span className="mr-2">4.</span>
                                    <span>Verify ethics & plagiarism</span>
                                </li>
                                <li className="flex items-start">
                                    <span className="mr-2">5.</span>
                                    <span>Export to LaTeX/PDF</span>
                                </li>
                            </ol>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default PaperEditor;
