import React from 'react';

const LatexLiveEditor = ({ paperData, setPaperData }) => {
    return (
        <div className="flex flex-col h-full bg-gray-900 text-gray-100">
            <div className="p-4 bg-gray-800 border-b border-gray-700 flex justify-between items-center">
                <h3 className="font-bold text-xl uppercase tracking-wider text-gray-300">Live LaTeX Editor</h3>
                <span className="bg-primary/20 text-blue-400 px-3 py-1 rounded-full text-sm font-semibold">Qwen 2.5 Accelerated</span>
            </div>
            <div className="flex-1 flex overflow-hidden">
                {/* Editor pane */}
                <textarea 
                    className="w-1/2 h-full bg-gray-900 text-green-400 p-6 font-mono focus:outline-none resize-none"
                    value={paperData.latex_code}
                    onChange={(e) => setPaperData({...paperData, latex_code: e.target.value})}
                    spellCheck="false"
                />
                
                {/* Colab code pane */}
                <div className="w-1/2 h-full border-l border-gray-700 flex flex-col">
                    <div className="bg-gray-800 p-2 text-xs text-gray-400 uppercase tracking-widest font-bold">Generated Colab ML Script</div>
                    <textarea 
                        className="flex-1 bg-gray-900 text-yellow-300 p-6 font-mono focus:outline-none resize-none"
                        value={paperData.colab_code}
                        onChange={(e) => setPaperData({...paperData, colab_code: e.target.value})}
                        spellCheck="false"
                    />
                </div>
            </div>
        </div>
    );
};

export default LatexLiveEditor;
