import React, { useState } from 'react';

const BasePaperSelector = ({ retrievedPapers, paperData, setPaperData, setStep }) => {
    const [selectedIds, setSelectedIds] = useState(new Set());
    const [generating, setGenerating] = useState(false);

    const togglePaper = (id) => {
        const newSet = new Set(selectedIds);
        if (newSet.has(id)) newSet.delete(id);
        else newSet.add(id);
        setSelectedIds(newSet);
    };

    const handleConfirm = () => {
        setGenerating(true);
        const basePapers = retrievedPapers.filter(p => selectedIds.has(p.id));
        setPaperData({ ...paperData, base_papers: basePapers });
        
        // Simulate Generation Process
        setTimeout(() => {
            setPaperData(prev => ({
                ...prev,
                latex_code: "\\documentElement{article}\n\\begin{document}\n\\title{" + (prev.title || "Research Paper") + "}\n\\maketitle\n\n\\section{Introduction}\nBased strictly on the selected papers...\n\\end{document}",
                colab_code: "# Generated Google Colab Code\n!pip install torch transformers\n\nimport torch\nprint('Model initialized directly from Qwen constraints.')",
                literature_survey: "# Literature Survey\nAnalyzed " + basePapers.length + " base papers."
            }));
            setGenerating(false);
            setStep('edit');
        }, 3000);
    };

    return (
        <div className="p-8 h-full overflow-y-auto">
            <h2 className="text-3xl font-bold font-heading mb-6 text-gray-800">Select Base Papers</h2>
            <p className="text-gray-600 mb-8">
                Synthesis uses <strong>Vectorless RAG</strong> to fetch these highly relevant matching papers.
                Select the factual basis for your generated paper to prevent hallucination.
            </p>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-8">
                {retrievedPapers.map((paper) => (
                    <div 
                        key={paper.id} 
                        className={`p-4 rounded-xl border-2 cursor-pointer transition-all ${selectedIds.has(paper.id) ? 'border-primary bg-blue-50' : 'border-gray-200 hover:border-blue-200 bg-white'}`}
                        onClick={() => togglePaper(paper.id)}
                    >
                        <div className="flex items-start">
                            <input 
                                type="checkbox" 
                                className="mt-1 mr-4 h-5 w-5 text-primary rounded" 
                                checked={selectedIds.has(paper.id)}
                                readOnly
                            />
                            <div>
                                <h3 className="font-bold text-gray-900">{paper.title}</h3>
                                <p className="text-sm text-gray-500 mt-1">{paper.authors} • {paper.year}</p>
                                <p className="text-sm text-gray-700 mt-2 line-clamp-3">{paper.abstract}</p>
                            </div>
                        </div>
                    </div>
                ))}
            </div>

            <button 
                onClick={handleConfirm}
                disabled={selectedIds.size === 0 || generating}
                className={`px-8 py-3 rounded-xl font-bold text-white shadow-lg transition-all ${(selectedIds.size === 0 || generating) ? 'bg-gray-400 cursor-not-allowed' : 'bg-primary hover:bg-primary-dark hover:shadow-xl'}`}
            >
                {generating ? 'Generating Paper & Colab Code...' : `Confirm ${selectedIds.size} Papers & Generate`}
            </button>
        </div>
    );
};

export default BasePaperSelector;
