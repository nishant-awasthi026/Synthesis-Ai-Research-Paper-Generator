import React, { useState, useEffect } from 'react';
import { validationAPI } from '../api/client';
import { useValidationStore } from '../store';

const ValidationDashboard = ({ paperId }) => {
    const [loading, setLoading] = useState(false);
    const [validating, setValidating] = useState(null);
    const validation = useValidationStore((state) => state.validations[paperId]);
    const setValidation = useValidationStore((state) => state.setValidation);

    const normalized = validation?.validations || validation || {};
    const preExportStatus = validation?.status;
    const canExport = validation?.can_export;
    const blockers = validation?.blockers || [];

    const runValidation = async (type) => {
        setValidating(type);
        setLoading(true);

        try {
            let response;

            switch (type) {
                case 'results':
                    response = await validationAPI.validateResults(paperId);
                    break;
                case 'plagiarism':
                    response = await validationAPI.checkPlagiarism(paperId);
                    break;
                case 'ai':
                    response = await validationAPI.detectAI(paperId);
                    break;
                case 'ethics':
                    response = await validationAPI.checkEthics(paperId);
                    break;
                case 'all':
                    response = await validationAPI.validateAll(paperId);
                    break;
                default:
                    return;
            }

            setValidation(paperId, response.data);
        } catch (error) {
            console.error('Validation failed:', error);
        } finally {
            setLoading(false);
            setValidating(null);
        }
    };

    const runPreExportCheck = async () => {
        setValidating('pre-export');
        setLoading(true);

        try {
            const response = await validationAPI.preExportCheck(paperId);
            setValidation(paperId, response.data);
        } catch (error) {
            console.error('Pre-export check failed:', error);
        } finally {
            setLoading(false);
            setValidating(null);
        }
    };

    const getStatusColor = (status) => {
        switch (status) {
            case 'passed':
                return 'text-green-600 bg-green-50 border-green-200';
            case 'warnings':
                return 'text-yellow-600 bg-yellow-50 border-yellow-200';
            case 'failed':
                return 'text-red-600 bg-red-50 border-red-200';
            default:
                return 'text-gray-600 bg-gray-50 border-gray-200';
        }
    };

    const getStatusIcon = (status) => {
        switch (status) {
            case 'passed':
                return '✓';
            case 'warnings':
                return '⚠';
            case 'failed':
                return '✗';
            default:
                return '•';
        }
    };

    const ValidationCard = ({ title, status, score, warnings, details }) => (
        <div className={`border rounded-lg p-4 ${getStatusColor(status)}`}>
            <div className="flex items-start justify-between mb-2">
                <h4 className="font-semibold text-sm">{title}</h4>
                <span className="text-2xl">{getStatusIcon(status)}</span>
            </div>

            {score !== undefined && (
                <div className="mb-2">
                    <div className="flex items-center justify-between text-xs mb-1">
                        <span>Score</span>
                        <span className="font-semibold">{(score * 100).toFixed(0)}%</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2">
                        <div
                            className={`h-2 rounded-full ${score > 0.7 ? 'bg-green-500' : score > 0.4 ? 'bg-yellow-500' : 'bg-red-500'
                                }`}
                            style={{ width: `${score * 100}%` }}
                        />
                    </div>
                </div>
            )}

            {warnings && warnings.length > 0 && (
                <div className="mt-2 text-xs">
                    <p className="font-semibold mb-1">Warnings:</p>
                    <ul className="list-disc list-inside space-y-1">
                        {warnings.slice(0, 3).map((warning, idx) => (
                            <li key={idx}>{warning}</li>
                        ))}
                        {warnings.length > 3 && (
                            <li className="text-gray-500">+{warnings.length - 3} more</li>
                        )}
                    </ul>
                </div>
            )}

            {details && Object.keys(details).length > 0 && (
                <div className="mt-2 text-xs">
                    <p className="font-semibold mb-1">Details:</p>
                    <div className="space-y-1">
                        {Object.entries(details).slice(0, 3).map(([key, value]) => (
                            <div key={key} className="flex justify-between">
                                <span className="capitalize">{key.replace(/_/g, ' ')}:</span>
                                <span className="font-semibold">{String(value)}</span>
                            </div>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );

    return (
        <div className="bg-white rounded-lg shadow-md p-6">
            <div className="flex items-center justify-between mb-6">
                <h3 className="text-xl font-semibold text-gray-800">Validation Dashboard</h3>
                <button
                    onClick={() => runValidation('all')}
                    disabled={loading}
                    className="px-4 py-2 bg-indigo-600 text-white text-sm rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 disabled:opacity-50"
                >
                    {loading && validating === 'all' ? 'Running...' : 'Run All Checks'}
                </button>
            </div>

            {/* Quick Actions */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6">
                <button
                    onClick={() => runValidation('results')}
                    disabled={loading}
                    className="px-3 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 text-sm rounded-md transition-colors disabled:opacity-50"
                >
                    {validating === 'results' ? '...' : 'Results'}
                </button>
                <button
                    onClick={() => runValidation('plagiarism')}
                    disabled={loading}
                    className="px-3 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 text-sm rounded-md transition-colors disabled:opacity-50"
                >
                    {validating === 'plagiarism' ? '...' : 'Plagiarism'}
                </button>
                <button
                    onClick={() => runValidation('ai')}
                    disabled={loading}
                    className="px-3 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 text-sm rounded-md transition-colors disabled:opacity-50"
                >
                    {validating === 'ai' ? '...' : 'AI Content'}
                </button>
                <button
                    onClick={() => runValidation('ethics')}
                    disabled={loading}
                    className="px-3 py-2 bg-gray-100 hover:bg-gray-200 text-gray-700 text-sm rounded-md transition-colors disabled:opacity-50"
                >
                    {validating === 'ethics' ? '...' : 'Ethics'}
                </button>
            </div>

            {/* Validation Results */}
            {validation ? (
                <div className="space-y-4">
                    {normalized.results && (
                        <ValidationCard
                            title="Results Validation"
                            status={normalized.results.status}
                            score={normalized.results.score}
                            warnings={normalized.results.warnings}
                            details={normalized.results.details}
                        />
                    )}

                    {normalized.plagiarism && (
                        <ValidationCard
                            title="Plagiarism Check"
                            status={normalized.plagiarism.status}
                            score={normalized.plagiarism.score}
                            warnings={normalized.plagiarism.similar_sections?.map(s =>
                                `${s.similarity}% similar to external source`
                            )}
                            details={{
                                'Max Similarity': `${normalized.plagiarism.max_similarity || 0}%`,
                                'Avg Similarity': `${normalized.plagiarism.avg_similarity || 0}%`
                            }}
                        />
                    )}

                    {normalized.ai_content && (
                        <ValidationCard
                            title="AI Content Detection"
                            status={normalized.ai_content.status}
                            score={1 - (normalized.ai_content.ai_probability || 0)}
                            warnings={normalized.ai_content.flagged_sections?.map(s =>
                                `AI-like content in ${s.section}`
                            )}
                            details={{
                                'AI Probability': `${((normalized.ai_content.ai_probability || 0) * 100).toFixed(0)}%`,
                                'Flagged Sections': normalized.ai_content.flagged_sections?.length || 0
                            }}
                        />
                    )}

                    {normalized.ethics && (
                        <ValidationCard
                            title="Ethics Checklist"
                            status={normalized.ethics.status}
                            score={normalized.ethics.score}
                            warnings={normalized.ethics.issues?.map(i =>
                                i.replace(/_/g, ' ')
                            )}
                            details={normalized.ethics.checks}
                        />
                    )}

                    {/* Pre-Export Check */}
                    {preExportStatus !== undefined && (
                        <div className={`p-4 rounded-lg border-2 ${canExport
                                ? 'bg-green-50 border-green-500'
                                : 'bg-red-50 border-red-500'
                            }`}>
                            <div className="flex items-center justify-between mb-2">
                                <h4 className="font-bold text-lg">
                                    {canExport ? '✓ Ready for Export' : '✗ Export Blocked'}
                                </h4>
                            </div>
                            <p className="text-sm mb-2">{validation.message}</p>
                            {blockers.length > 0 && (
                                <div className="text-sm">
                                    <p className="font-semibold mb-1">Blocking Issues:</p>
                                    <ul className="list-disc list-inside">
                                        {blockers.map((issue, idx) => (
                                            <li key={idx}>{issue}</li>
                                        ))}
                                    </ul>
                                </div>
                            )}
                        </div>
                    )}
                </div>
            ) : (
                <div className="text-center py-12 text-gray-500">
                    <p className="mb-4">No validation data yet</p>
                    <p className="text-sm">Click "Run All Checks" to validate your paper</p>
                </div>
            )}

            {/* Pre-Export Check Button */}
            <div className="mt-6 pt-6 border-t">
                <button
                    onClick={runPreExportCheck}
                    disabled={loading}
                    className="w-full px-4 py-3 bg-green-600 text-white font-semibold rounded-md hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 disabled:opacity-50"
                >
                    {loading && validating === 'pre-export'
                        ? 'Checking...'
                        : 'Run Pre-Export Validation'}
                </button>
            </div>
        </div>
    );
};

export default ValidationDashboard;
