import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import {
    ArrowRight,
    CheckCircle,
    FileText,
    Code,
    Upload,
    BookOpen,
    Download,
    Cpu,
    Search,
    RefreshCw,
    Play,
    Save,
    ExternalLink
} from 'lucide-react';
import { useAuthStore } from '../store';

const ResearchWorkflow = () => {
    const { paperId } = useParams();
    const navigate = useNavigate();
    const [currentStep, setCurrentStep] = useState(2); // Start at Step 2
    const [paper, setPaper] = useState(null);
    const [loading, setLoading] = useState(false);
    const [similarPapers, setSimilarPapers] = useState([]);

    // Step 2 Data: Discovery
    // Step 3 & 4 Data: Outline + Path Selection
    const [outline, setOutline] = useState({ title: '', abstract: '', introduction: '' });

    // Step 5 Data: Notebook
    const [notebookCode, setNotebookCode] = useState('');

    useEffect(() => {
        const initWorkflow = async () => {
            try {
                // 1. Fetch Paper Details
                const paperResp = await axios.get(`http://localhost:8000/api/papers/${paperId}`);
                setPaper(paperResp.data);

                // 2. Mock Outline Env (or fetch real)
                if (paperResp.data.title) {
                    generateOutline(paperResp.data.title);

                    // 3. Fetch Similar Papers (Real Context)
                    try {
                        const simResp = await axios.post('http://localhost:8000/api/discovery/similar', {
                            research_idea: paperResp.data.title,
                            top_k: 5
                        });
                        if (simResp.data.status === 'success') {
                            setSimilarPapers(simResp.data.papers || []);
                        }
                    } catch (err) {
                        console.error("Error fetching similar papers:", err);
                    }
                }
            } catch (error) {
                console.error("Error initializing workflow:", error);
            }
        };

        if (paperId) {
            initWorkflow();
        }
    }, [paperId]);

    const generateOutline = async (title) => {
        setLoading(true);
        try {
            // Generate Abstract
            const absResp = await axios.post('http://localhost:8000/api/papers/generate/section', {
                section: "Abstract",
                context: title
            });

            // Generate Intro
            const introResp = await axios.post('http://localhost:8000/api/papers/generate/section', {
                section: "Introduction",
                context: title
            });

            setOutline({
                title: title,
                abstract: absResp.data.content || "Generating abstract...",
                introduction: introResp.data.content || "Generating introduction..."
            });
        } catch (e) {
            console.error(e);
        } finally {
            setLoading(false);
        }
    };

    const generateNotebook = async () => {
        setLoading(true);
        try {
            const response = await axios.post('http://localhost:8000/api/papers/generate/code', {
                title: paper?.title || "Research Data Analysis",
                problem_description: "Data loading, preprocessing, model training and evaluation"
            });

            if (response.data.status === 'success') {
                setNotebookCode(response.data.code);
                setCurrentStep(5);
            }
        } catch (error) {
            console.error("Code Generation Failed", error);
        } finally {
            setLoading(false);
        }
    };

    const renderStepIndicator = () => (
        <div className="flex justify-between items-center mb-8 px-12">
            {[2, 3, 4, 5, 6, 7].map((step) => (
                <div key={step} className="flex flex-col items-center relative">
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center font-bold text-xs transition-colors duration-300 ${step < currentStep ? 'bg-green-500 text-white' :
                        step === currentStep ? 'bg-indigo-600 text-white' : 'bg-gray-200 text-gray-500'
                        }`}>
                        {step < currentStep ? <CheckCircle className="h-4 w-4" /> : step}
                    </div>
                    <span className="text-[10px] mt-1 text-gray-500 font-medium uppercase tracking-wider">
                        {step === 2 ? 'Context' :
                            step === 3 ? 'Fork' :
                                step === 4 ? 'Code' :
                                    step === 5 ? 'Exec' :
                                        step === 6 ? 'Synth' : 'Export'}
                    </span>
                    {step < 7 && (
                        <div className={`absolute top-4 left-8 h-[2px] -z-10 ${step < currentStep ? 'bg-green-500' : 'bg-gray-200'}`} style={{ width: 'calc(100% + 5rem)' }}></div>
                    )}
                </div>
            ))}
        </div>
    );

    return (
        <div className="min-h-screen bg-gray-50 flex flex-col font-sans">
            {/* Header */}
            <header className="bg-white border-b border-gray-200 h-16 flex items-center justify-between px-6 shadow-sm sticky top-0 z-10">
                <div className="flex items-center gap-2">
                    <div className="font-bold text-xl text-gray-800">Synthesis.ai</div>
                    <span className="px-2 py-0.5 bg-gray-100 text-gray-500 text-xs rounded-full">Research Mode</span>
                </div>
                <div className="text-sm font-medium text-gray-600">
                    {paper?.title || "Untitled Session"}
                </div>
            </header>

            {/* Main Content */}
            <main className="flex-1 max-w-6xl mx-auto w-full p-8 pb-32">
                {renderStepIndicator()}

                {/* Step 2: Topic Initialization & Context Setup */}
                {currentStep === 2 && (
                    <div className="animate-fade-in bg-white rounded-2xl shadow-sm border border-gray-100 p-12 min-h-[500px] flex flex-col items-center justify-center text-center">
                        <div className="w-16 h-16 bg-indigo-100 rounded-full flex items-center justify-center mb-6 animate-pulse">
                            <Search className="h-8 w-8 text-indigo-600" />
                        </div>
                        <h1 className="text-4xl font-bold text-gray-900 mb-4 tracking-tight">
                            {paper?.title || "Initializing..."}
                        </h1>
                        <p className="text-gray-500 text-lg mb-8 max-w-2xl">
                            Establishing context window from 2,000+ open-access repositories (arXiv, PubMed).
                        </p>
                        <div className="w-full max-w-md bg-gray-100 rounded-full h-2 mb-2 overflow-hidden">
                            <div className="bg-indigo-600 h-2 rounded-full animate-[width_2s_ease-in-out_forwards]" style={{ width: '100%' }}></div>
                        </div>
                        <div className="text-sm text-gray-400 font-mono">Scanning repositories...</div>

                        {/* Auto-advance for demo */}
                        <AutoAdvance onDone={() => setCurrentStep(3)} />
                    </div>
                )}

                {/* Step 3: Workflow Forking (AI Abstract + Path Selection) */}
                {currentStep === 3 && (
                    <div className="animate-fade-in bg-white rounded-2xl shadow-sm border border-gray-100 p-8 min-h-[600px]">
                        <div className="mb-8">
                            <h2 className="text-2xl font-bold text-gray-900 mb-2">Preliminary Research Draft</h2>
                            <p className="text-gray-500">Based on our initial scan, we've generated this foundation.</p>
                        </div>

                        {/* Generated Abstract Preview */}
                        <div className="bg-gray-50 border border-gray-200 rounded-xl p-6 mb-10 shadow-inner">
                            <h3 className="font-bold text-gray-800 text-lg mb-2">{outline.title}</h3>
                            <h4 className="text-xs font-bold text-gray-500 uppercase mb-1">Abstract</h4>
                            <p className="text-gray-600 text-sm leading-relaxed mb-4">{outline.abstract}</p>
                            <h4 className="text-xs font-bold text-gray-500 uppercase mb-1">Introduction</h4>
                            <p className="text-gray-600 text-sm leading-relaxed">{outline.introduction}</p>
                        </div>

                        <h2 className="text-xl font-bold text-gray-900 mb-6 text-center">Select Your Methodology</h2>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
                            {/* Option 1: Upload */}
                            <div className="bg-blue-50 border-2 border-blue-100 rounded-2xl p-8 flex flex-col items-center text-center hover:border-blue-400 hover:shadow-xl transition-all cursor-pointer group">
                                <div className="w-14 h-14 bg-blue-100 rounded-full flex items-center justify-center mb-4 text-blue-600">
                                    <Upload className="h-7 w-7" />
                                </div>
                                <h3 className="text-lg font-bold text-blue-900 mb-2">Option 1: Upload File</h3>
                                <p className="text-blue-700/70 text-sm mb-6">Existing datasets (.txt, .csv, .ipynb)</p>
                                <button className="w-full py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium shadow-sm transition-colors text-sm">
                                    Browse Files
                                </button>
                            </div>

                            {/* Option 2: Create Notebook */}
                            <div
                                onClick={generateNotebook}
                                className="bg-green-50 border-2 border-green-100 rounded-2xl p-8 flex flex-col items-center text-center hover:border-green-400 hover:shadow-xl transition-all cursor-pointer group"
                            >
                                <div className="w-14 h-14 bg-green-100 rounded-full flex items-center justify-center mb-4 text-green-600">
                                    <Code className="h-7 w-7" />
                                </div>
                                <h3 className="text-lg font-bold text-green-900 mb-2">Option 2: Create Notebook</h3>
                                <p className="text-green-700/70 text-sm mb-6">Generate code via AI Chat</p>
                                <button className="w-full py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg font-medium shadow-sm transition-colors text-sm" disabled={loading}>
                                    {loading ? "Generatng..." : "Start Chatting"}
                                </button>
                            </div>
                        </div>
                    </div>
                )}

                {/* Step 4 & 5: Interactive Code & Execution */}
                {currentStep === 5 && (
                    <div className="animate-fade-in flex flex-col h-full bg-white rounded-2xl shadow-sm border border-gray-100 overflow-hidden">
                        <div className="bg-gray-900 p-4 border-b border-gray-800 flex justify-between items-center">
                            <div className="flex items-center gap-3">
                                <div className="flex gap-1.5">
                                    <div className="w-3 h-3 rounded-full bg-red-500"></div>
                                    <div className="w-3 h-3 rounded-full bg-yellow-500"></div>
                                    <div className="w-3 h-3 rounded-full bg-green-500"></div>
                                </div>
                                <span className="text-gray-400 text-sm font-mono ml-2">model_training.ipynb</span>
                            </div>
                            <span className="text-xs text-green-400 font-mono flex items-center gap-1">
                                <Cpu className="h-3 w-3" /> Python 3.10
                            </span>
                        </div>

                        <div className="p-0 flex-1 bg-[#1e1e1e] overflow-y-auto font-mono text-sm">
                            <pre className="p-6 text-gray-300">
                                {notebookCode.split('\n').map((line, i) => (
                                    <div key={i} className="table-row">
                                        <span className="table-cell text-gray-600 select-none pr-4 text-right w-8">{i + 1}</span>
                                        <span className="table-cell">{line}</span>
                                    </div>
                                ))}
                            </pre>
                        </div>

                        {/* Step 5: External Execution Integration Buttons */}
                        <div className="p-6 bg-white border-t border-gray-200">
                            <div className="flex gap-4">
                                <button className="flex-1 flex items-center justify-center gap-2 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium shadow-sm transition-colors">
                                    <ExternalLink className="h-4 w-4" /> Go to Google Colab
                                </button>
                                <button
                                    onClick={() => setCurrentStep(6)}
                                    className="flex-1 flex items-center justify-center gap-2 py-3 bg-green-600 hover:bg-green-700 text-white rounded-lg font-medium shadow-sm transition-colors"
                                >
                                    <Upload className="h-4 w-4" /> Integrate Colab Result
                                </button>
                            </div>
                        </div>
                    </div>
                )}

                {/* Step 6: Synthesis & Assembly */}
                {currentStep === 6 && (
                    <div className="animate-fade-in relative min-h-[600px] mb-12">
                        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-12 max-w-4xl mx-auto">
                            <div className="mb-12 text-center">
                                <h1 className="text-3xl font-bold text-gray-900 mb-2">{outline.title}</h1>
                                <p className="text-gray-500 italic">Draft Version • {new Date().toLocaleDateString()}</p>
                            </div>

                            <div className="space-y-8 text-gray-800 leading-relaxed text-justify">
                                <section>
                                    <h3 className="font-bold text-lg mb-3">Abstract</h3>
                                    <p>{outline.abstract}</p>
                                </section>
                                <section>
                                    <h3 className="font-bold text-lg mb-3">1. Introduction</h3>
                                    <p>{outline.introduction}</p>
                                </section>
                                <section>
                                    <h3 className="font-bold text-lg mb-3">2. Methodology</h3>
                                    <div className="bg-gray-50 p-4 rounded-lg border border-gray-200 font-mono text-xs text-gray-600 mb-2">
                                        clf = RandomForestClassifier(n_estimators=100)<br />
                                        clf.fit(X_train, y_train)
                                    </div>
                                    <p>We implemented a Random Forest Classifier to analyze the dataset...</p>
                                </section>
                                <section>
                                    <h3 className="font-bold text-lg mb-3">3. Results</h3>
                                    <p>The model achieved an accuracy score consistent with state-of-the-art approaches. [Placeholder for integrated results].</p>
                                </section>
                            </div>
                        </div>

                        {/* Sticky Save Bar */}
                        <div className="fixed bottom-6 left-1/2 transform -translate-x-1/2 w-full max-w-lg">
                            <button
                                onClick={() => setCurrentStep(7)}
                                className="w-full flex items-center justify-center gap-2 py-4 bg-indigo-600 hover:bg-indigo-700 text-white rounded-full font-bold shadow-lg hover:shadow-xl hover:-translate-y-1 transition-all"
                            >
                                <Save className="h-5 w-5" /> Save Research Paper
                            </button>
                        </div>
                    </div>
                )}

                {/* Step 7: Final Review & Export (Dual View) */}
                {currentStep === 7 && (
                    <div className="animate-fade-in h-[700px] flex flex-col">
                        <div className="flex justify-between items-center mb-6">
                            <h2 className="text-2xl font-bold text-gray-900">Final Export</h2>
                            <button className="flex items-center gap-2 px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-medium shadow-sm transition-colors">
                                <Download className="h-4 w-4" /> Download PDF
                            </button>
                        </div>

                        <div className="flex-1 grid grid-cols-2 gap-0 border border-gray-300 rounded-xl overflow-hidden shadow-lg">
                            {/* Left Pane: LaTeX Editor */}
                            <div className="bg-[#1e1e1e] flex flex-col border-r border-gray-700">
                                <div className="bg-[#252526] px-4 py-2 text-xs text-gray-400 font-mono border-b border-gray-700">source.tex</div>
                                <div className="flex-1 p-4 font-mono text-xs text-blue-300 overflow-y-auto leading-6">
                                    <span className="text-purple-400">\documentclass</span><span className="text-yellow-300">{'{article}'}</span><br />
                                    <span className="text-purple-400">\usepackage</span><span className="text-yellow-300">{'{graphicx}'}</span><br />
                                    <span className="text-purple-400">\title</span><span className="text-yellow-300">{'{'}{outline.title}{'}'}</span><br />
                                    <br />
                                    <span className="text-purple-400">\begin</span><span className="text-yellow-300">{'{document}'}</span><br />
                                    <span className="text-purple-400">\maketitle</span><br />
                                    <br />
                                    <span className="text-purple-400">\section</span><span className="text-yellow-300">{'{Abstract}'}</span><br />
                                    <span className="text-white">{outline.abstract}</span><br />
                                    <br />
                                    <span className="text-purple-400">\section</span><span className="text-yellow-300">{'{Introduction}'}</span><br />
                                    <span className="text-white">{outline.introduction}</span><br />
                                    <br />
                                    <span className="text-purple-400">\end</span><span className="text-yellow-300">{'{document}'}</span>
                                </div>
                            </div>

                            {/* Right Pane: PDF Preview */}
                            <div className="bg-gray-100 flex flex-col">
                                <div className="bg-white px-4 py-2 border-b border-gray-200 text-xs text-gray-500 font-medium flex justify-between">
                                    <span>Preview</span>
                                    <span>Page 1 / 4</span>
                                </div>
                                <div className="flex-1 p-8 overflow-y-auto flex justify-center bg-gray-50/50">
                                    <div className="w-[400px] bg-white h-[560px] shadow-md border border-gray-200 p-8 text-[9px] leading-tight text-gray-900 select-none">
                                        <h1 className="text-lg font-bold text-center mb-2 font-serif">{outline.title}</h1>
                                        <p className="text-center text-gray-500 mb-6 italic font-serif">Synthesis AI • {new Date().toLocaleDateString()}</p>

                                        <h2 className="font-bold uppercase text-[10px] mb-1 font-serif">Abstract</h2>
                                        <p className="mb-4 text-justify font-serif leading-3">{outline.abstract}</p>

                                        <h2 className="font-bold uppercase text-[10px] mb-1 font-serif">1. Introduction</h2>
                                        <p className="text-justify font-serif leading-3">{outline.introduction}</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                )}

            </main>
        </div>
    );
};

export default ResearchWorkflow;

const AutoAdvance = ({ onDone }) => {
    useEffect(() => {
        const timer = setTimeout(() => onDone(), 2500);
        return () => clearTimeout(timer);
    }, [onDone]);
    return null;
};
