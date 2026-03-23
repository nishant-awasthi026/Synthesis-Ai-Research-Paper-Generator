import React, { useState, useEffect } from 'react';
import { exportAPI } from '../api/client';

const ExportPanel = ({ paperId, paperTitle }) => {
    const [templates, setTemplates] = useState([]);
    const [selectedTemplate, setSelectedTemplate] = useState('generic_article');
    const [exporting, setExporting] = useState(false);
    const [exportType, setExportType] = useState('latex');

    useEffect(() => {
        // Load available templates
        const loadTemplates = async () => {
            try {
                const response = await exportAPI.getTemplates();
                setTemplates(response.data.templates || []);
            } catch (error) {
                console.error('Failed to load templates:', error);
            }
        };
        loadTemplates();
    }, []);

    const handleExport = async () => {
        setExporting(true);

        try {
            let response;
            let filename;
            let mimeType;

            if (exportType === 'pdf') {
                response = await exportAPI.exportPDF(paperId, selectedTemplate);
                filename = `${paperTitle || 'paper'}.pdf`;
                mimeType = 'application/pdf';
            } else if (exportType === 'zip') {
                response = await exportAPI.exportZip(paperId, selectedTemplate, true);
                filename = `${paperTitle || 'paper'}_synthesis_export.zip`;
                mimeType = 'application/zip';
            } else {
                response = await exportAPI.exportLatex(paperId, selectedTemplate);
                filename = `${paperTitle || 'paper'}.tex`;
                mimeType = 'application/x-latex';
            }

            // Create blob and download
            const blob = new Blob([response.data], { type: mimeType });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } catch (error) {
            alert(error.response?.data?.detail || 'Export failed');
        } finally {
            setExporting(false);
        }
    };

    return (
        <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-semibold mb-4 text-gray-800">Export Paper</h3>

            {/* Export Type Selection */}
            <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                    Export Format
                </label>
                <div className="grid grid-cols-3 gap-3">
                    <button
                        onClick={() => setExportType('latex')}
                        className={`px-4 py-3 rounded-lg border-2 transition-all ${exportType === 'latex'
                                ? 'border-indigo-600 bg-indigo-50 text-indigo-700'
                                : 'border-gray-300 bg-white text-gray-700 hover:border-gray-400'
                            }`}
                    >
                        <div className="font-semibold">LaTeX</div>
                        <div className="text-xs mt-1">.tex file</div>
                    </button>
                    <button
                        onClick={() => setExportType('pdf')}
                        className={`px-4 py-3 rounded-lg border-2 transition-all ${exportType === 'pdf'
                                ? 'border-indigo-600 bg-indigo-50 text-indigo-700'
                                : 'border-gray-300 bg-white text-gray-700 hover:border-gray-400'
                            }`}
                    >
                        <div className="font-semibold">PDF</div>
                        <div className="text-xs mt-1">Requires pdflatex</div>
                    </button>
                    <button
                        onClick={() => setExportType('zip')}
                        className={`px-4 py-3 rounded-lg border-2 transition-all ${exportType === 'zip'
                                ? 'border-indigo-600 bg-indigo-50 text-indigo-700'
                                : 'border-gray-300 bg-white text-gray-700 hover:border-gray-400'
                            }`}
                    >
                        <div className="font-semibold">ZIP</div>
                        <div className="text-xs mt-1">Paper package</div>
                    </button>
                </div>
            </div>

            {/* Template Selection */}
            <div className="mb-6">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                    Template
                </label>
                <select
                    value={selectedTemplate}
                    onChange={(e) => setSelectedTemplate(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                >
                    {templates.map((template) => (
                        <option key={template.name} value={template.name}>
                            {template.title} - {template.description}
                        </option>
                    ))}
                </select>

                {templates.length === 0 && (
                    <div className="mt-2">
                        <option value="generic_article">Generic Article - Standard format</option>
                        <option value="ieee_conference">IEEE Conference - Two-column format</option>
                    </div>
                )}
            </div>

            {/* Template Preview */}
            <div className="mb-6 p-4 bg-gray-50 rounded-lg border">
                <h4 className="font-semibold text-sm text-gray-700 mb-2">
                    Template Preview
                </h4>
                <div className="text-sm text-gray-600">
                    {selectedTemplate === 'ieee_conference' ? (
                        <div>
                            <p className="mb-2">📄 <strong>IEEE Conference Format</strong></p>
                            <ul className="list-disc list-inside text-xs space-y-1 text-gray-500">
                                <li>Two-column layout</li>
                                <li>Standard IEEE formatting</li>
                                <li>Optimized for conferences</li>
                                <li>Includes author blocks</li>
                            </ul>
                        </div>
                    ) : (
                        <div>
                            <p className="mb-2">📄 <strong>Generic Article Format</strong></p>
                            <ul className="list-disc list-inside text-xs space-y-1 text-gray-500">
                                <li>Single-column layout</li>
                                <li>Standard academic article</li>
                                <li>Flexible sections</li>
                                <li>Suitable for most journals</li>
                            </ul>
                        </div>
                    )}
                </div>
            </div>

            {/* Export Info */}
            <div className="mb-4 p-3 bg-blue-50 border border-blue-200 rounded text-sm text-blue-800">
                <p className="font-semibold mb-1">ℹ️ Export Notes:</p>
                <ul className="list-disc list-inside text-xs space-y-1">
                    <li>LaTeX files can be compiled with any TeX distribution</li>
                    <li>PDF export requires pdflatex installed on backend server</li>
                    <li>ZIP includes LaTeX, optional PDF, docs, and base paper metadata</li>
                    <li>Citations will be formatted in BibTeX</li>
                    <li>All sections will be included automatically</li>
                </ul>
            </div>

            {/* Export Button */}
            <button
                onClick={handleExport}
                disabled={exporting}
                className="w-full bg-indigo-600 text-white py-3 px-4 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors font-semibold"
            >
                {exporting ? (
                    <span className="flex items-center justify-center">
                        <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                            <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                            <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                        </svg>
                        Exporting...
                    </span>
                ) : (
                    <span>Download {exportType.toUpperCase()}</span>
                )}
            </button>

            {exportType === 'pdf' && (
                <p className="mt-3 text-xs text-gray-500 text-center">
                    ⚠️ PDF generation requires pdflatex on backend server
                </p>
            )}
        </div>
    );
};

export default ExportPanel;
