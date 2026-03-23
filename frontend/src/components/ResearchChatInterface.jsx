import React, { useState } from 'react';

const ResearchChatInterface = ({ setStep, setRetrievedPapers, paperData, setPaperData }) => {
    const [messages, setMessages] = useState([{ role: 'assistant', text: "Hello! I am Synthesis AI. What research topic are you interested in exploring today? Describe your idea, and I'll find relevant papers to use as a factual base." }]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [progress, setProgress] = useState(0);

    const handleSend = async () => {
        if (!input.trim()) return;
        const userMsg = input;
        setInput('');
        setMessages(prev => [...prev, { role: 'user', text: userMsg }]);
        setIsLoading(true);

        try {
            // Simulated chat API call for POC (would connect to backend/api/chat implementation)
            const response = await fetch('http://localhost:8000/api/discovery/similar', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: userMsg, n_results: 5 })
            });
            const data = await response.json();
            
            setRetrievedPapers(data.papers || []);
            
            // Artificial progress visualizer
            let p = 0;
            const interval = setInterval(() => {
                p += 20;
                setProgress(p);
                if (p >= 100) clearInterval(interval);
            }, 500);

            setTimeout(() => {
                setMessages(prev => [...prev, { role: 'assistant', text: `I found ${data.papers?.length || 0} related papers using BM25 indexing! I've populated the "Select Base Papers" stage. Please review them so we can strictly rely on their facts. Also, if you need me to construct a Google Colab ML script, just ask.`}]);
                setPaperData({ ...paperData, title: userMsg.substring(0,30) });
                setProgress(0);
                setIsLoading(false);
                setStep('select');
            }, 3000);

        } catch (error) {
            console.error(error);
            setMessages(prev => [...prev, { role: 'assistant', text: "Sorry, I had trouble reaching the Backend. Are you sure the BM25 vectorless store is running?"}]);
            setIsLoading(false);
        }
    };

    return (
        <div className="flex flex-col h-full bg-white relative">
            {progress > 0 && (
                <div className="absolute top-0 left-0 w-full h-1 bg-gray-200">
                    <div className="h-full bg-primary transition-all duration-300" style={{width: `${progress}%`}}></div>
                </div>
            )}
            <div className="flex-1 p-6 overflow-y-auto space-y-4">
                {messages.map((msg, i) => (
                    <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        <div className={`max-w-[70%] rounded-2xl p-4 ${msg.role === 'user' ? 'bg-primary text-white' : 'bg-gray-100 text-gray-800'}`}>
                            {msg.text}
                        </div>
                    </div>
                ))}
                {isLoading && (
                    <div className="flex justify-start">
                        <div className="max-w-[70%] rounded-2xl p-4 bg-gray-100 text-gray-800 animate-pulse">
                            Thinking...
                        </div>
                    </div>
                )}
            </div>
            
            <div className="p-4 border-t bg-gray-50">
                <div className="flex items-center bg-white rounded-full border shadow-sm px-4 py-2">
                    <input 
                        className="flex-1 appearance-none bg-transparent border-none w-full text-gray-700 mr-3 py-1 px-2 leading-tight focus:outline-none" 
                        type="text" 
                        placeholder="Discuss your research topic..."
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        onKeyPress={(e) => e.key === 'Enter' && handleSend()}
                    />
                    <button 
                        className="flex-shrink-0 bg-primary hover:bg-primary-dark border-primary hover:border-primary-dark text-sm border-4 text-white py-1 px-4 rounded-full transition"
                        onClick={handleSend}
                        disabled={isLoading}
                    >
                        Send
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ResearchChatInterface;
