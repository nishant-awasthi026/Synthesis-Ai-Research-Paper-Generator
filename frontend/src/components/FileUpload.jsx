import React, { useState, useCallback } from 'react';
import { uploadAPI } from '../api/client';
import { usePaperStore } from '../store';

const FileUpload = ({ paperId }) => {
    const [uploading, setUploading] = useState(false);
    const [dragActive, setDragActive] = useState(false);
    const [selectedFile, setSelectedFile] = useState(null);
    const [description, setDescription] = useState('');
    const [uploadType, setUploadType] = useState('results');
    const [colabUrl, setColabUrl] = useState('');
    const [message, setMessage] = useState({ type: '', text: '' });

    const updatePaper = usePaperStore((state) => state.updatePaper);

    const handleDrag = useCallback((e) => {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === 'dragenter' || e.type === 'dragover') {
            setDragActive(true);
        } else if (e.type === 'dragleave') {
            setDragActive(false);
        }
    }, []);

    const handleDrop = useCallback((e) => {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            setSelectedFile(e.dataTransfer.files[0]);
        }
    }, []);

    const handleFileChange = (e) => {
        if (e.target.files && e.target.files[0]) {
            setSelectedFile(e.target.files[0]);
        }
    };

    const handleUpload = async () => {
        if (!selectedFile && uploadType !== 'colab') {
            setMessage({ type: 'error', text: 'Please select a file' });
            return;
        }

        if (uploadType === 'colab' && !colabUrl) {
            setMessage({ type: 'error', text: 'Please enter Colab URL' });
            return;
        }

        setUploading(true);
        setMessage({ type: '', text: '' });

        try {
            let response;

            if (uploadType === 'colab') {
                response = await uploadAPI.linkColab(paperId, colabUrl);
            } else if (uploadType === 'notebook') {
                response = await uploadAPI.uploadNotebook(paperId, selectedFile);
            } else {
                response = await uploadAPI.uploadResults(paperId, selectedFile, description);
            }

            setMessage({ type: 'success', text: 'Upload successful!' });
            setSelectedFile(null);
            setDescription('');
            setColabUrl('');

            // Refresh paper data
            updatePaper(paperId, { has_results: true });
        } catch (error) {
            setMessage({
                type: 'error',
                text: error.response?.data?.detail || 'Upload failed'
            });
        } finally {
            setUploading(false);
        }
    };

    return (
        <div className="bg-white rounded-lg shadow-md p-6">
            <h3 className="text-xl font-semibold mb-4 text-gray-800">Upload Experimental Results</h3>

            {/* Upload Type Selection */}
            <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                    Upload Type
                </label>
                <select
                    value={uploadType}
                    onChange={(e) => setUploadType(e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                >
                    <option value="results">Results File (txt/csv/json)</option>
                    <option value="notebook">Jupyter Notebook</option>
                    <option value="colab">Google Colab Link</option>
                </select>
            </div>

            {/* Colab URL Input */}
            {uploadType === 'colab' ? (
                <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                        Google Colab URL
                    </label>
                    <input
                        type="url"
                        value={colabUrl}
                        onChange={(e) => setColabUrl(e.target.value)}
                        placeholder="https://colab.research.google.com/..."
                        className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    />
                </div>
            ) : (
                <>
                    {/* Drag and Drop Area */}
                    <div
                        onDragEnter={handleDrag}
                        onDragLeave={handleDrag}
                        onDragOver={handleDrag}
                        onDrop={handleDrop}
                        className={`mb-4 border-2 border-dashed rounded-lg p-8 text-center transition-colors ${dragActive
                                ? 'border-indigo-500 bg-indigo-50'
                                : 'border-gray-300 bg-gray-50'
                            }`}
                    >
                        <input
                            type="file"
                            id="fileInput"
                            onChange={handleFileChange}
                            accept={uploadType === 'notebook' ? '.ipynb' : '.txt,.csv,.json'}
                            className="hidden"
                        />

                        {selectedFile ? (
                            <div className="text-sm text-gray-700">
                                <p className="font-semibold mb-2">Selected file:</p>
                                <p className="text-indigo-600">{selectedFile.name}</p>
                                <p className="text-gray-500 text-xs mt-1">
                                    {(selectedFile.size / 1024).toFixed(2)} KB
                                </p>
                                <button
                                    onClick={() => setSelectedFile(null)}
                                    className="mt-2 text-red-600 hover:text-red-700 text-sm"
                                >
                                    Remove
                                </button>
                            </div>
                        ) : (
                            <div>
                                <svg
                                    className="mx-auto h-12 w-12 text-gray-400"
                                    stroke="currentColor"
                                    fill="none"
                                    viewBox="0 0 48 48"
                                >
                                    <path
                                        d="M28 8H12a4 4 0 00-4 4v20m32-12v8m0 0v8a4 4 0 01-4 4H12a4 4 0 01-4-4v-4m32-4l-3.172-3.172a4 4 0 00-5.656 0L28 28M8 32l9.172-9.172a4 4 0 015.656 0L28 28m0 0l4 4m4-24h8m-4-4v8m-12 4h.02"
                                        strokeWidth={2}
                                        strokeLinecap="round"
                                        strokeLinejoin="round"
                                    />
                                </svg>
                                <p className="mt-2 text-sm text-gray-600">
                                    Drag and drop file here, or{' '}
                                    <label
                                        htmlFor="fileInput"
                                        className="text-indigo-600 hover:text-indigo-700 cursor-pointer font-semibold"
                                    >
                                        browse
                                    </label>
                                </p>
                                <p className="text-xs text-gray-500 mt-1">
                                    {uploadType === 'notebook'
                                        ? 'Jupyter Notebook (.ipynb)'
                                        : 'TXT, CSV, or JSON files'}
                                </p>
                            </div>
                        )}
                    </div>

                    {/* Description Input */}
                    {uploadType === 'results' && (
                        <div className="mb-4">
                            <label className="block text-sm font-medium text-gray-700 mb-2">
                                Description (optional)
                            </label>
                            <textarea
                                value={description}
                                onChange={(e) => setDescription(e.target.value)}
                                placeholder="Describe your experimental results..."
                                rows={3}
                                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                            />
                        </div>
                    )}
                </>
            )}

            {/* Message Display */}
            {message.text && (
                <div
                    className={`mb-4 px-4 py-3 rounded ${message.type === 'success'
                            ? 'bg-green-50 text-green-800 border border-green-200'
                            : 'bg-red-50 text-red-800 border border-red-200'
                        }`}
                >
                    {message.text}
                </div>
            )}

            {/* Upload Button */}
            <button
                onClick={handleUpload}
                disabled={uploading || (!selectedFile && uploadType !== 'colab')}
                className="w-full bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
            >
                {uploading ? 'Uploading...' : 'Upload'}
            </button>

            <p className="mt-4 text-xs text-gray-500 text-center">
                ⚠️ Upload real experimental results to ensure ethical paper generation
            </p>
        </div>
    );
};

export default FileUpload;
