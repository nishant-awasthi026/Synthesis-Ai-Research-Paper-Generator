import React, { useState } from 'react';
import ResearchChatInterface from '../components/ResearchChatInterface';
import BasePaperSelector from '../components/BasePaperSelector';
import LatexLiveEditor from '../components/LatexLiveEditor';

const InteractiveResearch = () => {
    const [step, setStep] = useState('chat'); // 'chat' | 'select' | 'edit'
    const [paperData, setPaperData] = useState({ title: '', base_papers: [], latex_code: '', colab_code: '' });
    const [retrievedPapers, setRetrievedPapers] = useState([]);

    return (
        <div className="flex h-screen bg-gray-50">
            {/* Sidebar Flow controls */}
            <div className="w-1/4 bg-white border-r shadow-sm p-4 overflow-y-auto">
                <h2 className="text-xl font-bold mb-4 text-primary font-heading">Research Flow</h2>
                <div className="space-y-4">
                    <button 
                        onClick={() => setStep('chat')}
                        className={`w-full p-3 text-left rounded-lg transition-colors ${step === 'chat' ? 'bg-primary text-white shadow' : 'hover:bg-gray-100'}`}>
                        1. Topic Ideation
                    </button>
                    <button 
                        onClick={() => setStep('select')}
                        disabled={retrievedPapers.length === 0}
                        className={`w-full p-3 text-left rounded-lg transition-colors ${(retrievedPapers.length === 0) ? 'opacity-50 cursor-not-allowed' : (step === 'select' ? 'bg-primary text-white shadow' : 'hover:bg-gray-100')}`}>
                        2. Select Base Papers
                    </button>
                    <button 
                        onClick={() => setStep('edit')}
                        disabled={!paperData.latex_code}
                        className={`w-full p-3 text-left rounded-lg transition-colors ${!paperData.latex_code ? 'opacity-50 cursor-not-allowed' : (step === 'edit' ? 'bg-primary text-white shadow' : 'hover:bg-gray-100')}`}>
                        3. Review & Edit
                    </button>
                </div>

                <div className="mt-8 border-t pt-4">
                    <button 
                        className="w-full bg-green-600 text-white p-3 rounded-lg font-bold hover:bg-green-700 transition"
                        disabled={!paperData.latex_code}
                        onClick={async () => {
                            try {
                                const response = await fetch('http://localhost:8000/api/export/zip', {
                                    method: 'POST',
                                    headers: {'Content-Type': 'application/json'},
                                    body: JSON.stringify(paperData)
                                });
                                const blob = await response.blob();
                                const url = window.URL.createObjectURL(blob);
                                const a = document.createElement('a');
                                a.href = url;
                                a.download = `${paperData.title || 'Research'}_package.zip`;
                                document.body.appendChild(a);
                                a.click();
                                a.remove();
                            } catch (e) {
                                console.error("Export failed", e);
                            }
                        }}>
                        Export ZIP Package
                    </button>
                </div>
            </div>

            {/* Main Content Area */}
            <div className="flex-1 overflow-hidden flex flex-col">
                {step === 'chat' && (
                    <ResearchChatInterface 
                        setStep={setStep}
                        setRetrievedPapers={setRetrievedPapers}
                        paperData={paperData}
                        setPaperData={setPaperData}
                    />
                )}
                {step === 'select' && (
                    <BasePaperSelector 
                        retrievedPapers={retrievedPapers}
                        paperData={paperData}
                        setPaperData={setPaperData}
                        setStep={setStep}
                    />
                )}
                {step === 'edit' && (
                    <LatexLiveEditor 
                        paperData={paperData}
                        setPaperData={setPaperData}
                    />
                )}
            </div>
        </div>
    );
};

export default InteractiveResearch;
