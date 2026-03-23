import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Auth API
export const authAPI = {
    register: (data) => api.post('/auth/register', data),
    login: (data) => api.post('/auth/login', data),
    getMe: () => api.get('/auth/me'),
    updateProfile: (data) => api.put('/auth/profile', data),
    logout: () => api.post('/auth/logout'),
};

// Papers API
export const papersAPI = {
    create: (data) => api.post('/papers/create', data),
    getAll: (params = {}) => api.get('/papers/list', { params }),
    getOne: (id) => api.get(`/papers/${id}`),
    update: (id, data) => api.put(`/papers/${id}`, data),
    delete: (id) => api.delete(`/papers/${id}`),
};

// Upload API
export const uploadAPI = {
    uploadResults: (paperId, file, description) => {
        const formData = new FormData();
        formData.append('file', file);
        if (description) formData.append('description', description);
        return api.post(`/papers/${paperId}/upload/results`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
        });
    },
    uploadNotebook: (paperId, file) => {
        const formData = new FormData();
        formData.append('file', file);
        return api.post(`/papers/${paperId}/upload/notebook`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' },
        });
    },
    linkColab: (paperId, colabUrl) =>
        api.post(`/papers/${paperId}/upload/colab`, { colab_url: colabUrl }),
    getResults: (paperId) => api.get(`/papers/${paperId}/results`),
    deleteResult: (paperId, experimentId) =>
        api.delete(`/papers/${paperId}/results/${experimentId}`),
};

// Validation API
export const validationAPI = {
    validateResults: (paperId) => api.post(`/papers/${paperId}/validate/results`),
    checkPlagiarism: (paperId) => api.post(`/papers/${paperId}/validate/plagiarism`),
    detectAI: (paperId) => api.post(`/papers/${paperId}/validate/ai-content`),
    checkEthics: (paperId) => api.post(`/papers/${paperId}/validate/ethics`),
    validateAll: (paperId) => api.post(`/papers/${paperId}/validate/all`),
    preExportCheck: (paperId) => api.post(`/papers/${paperId}/pre-export-check`),
    getHistory: (paperId) => api.get(`/papers/${paperId}/validations`),
};

// Chat API
export const chatAPI = {
    sendMessage: (paperId, message) =>
        api.post(`/papers/${paperId}/chat`, { message }),
    applyEdit: (paperId, section, content) =>
        api.post(`/papers/${paperId}/apply-edit`, { section, content }),
    getHistory: (paperId) => api.get(`/papers/${paperId}/chat/history`),
    clearHistory: (paperId) => api.delete(`/papers/${paperId}/chat/history`),
};

// Export API
export const exportAPI = {
    exportLatex: (paperId, template = 'generic_article') =>
        api.post(`/export/${paperId}/latex`, null, {
            params: { template },
            responseType: 'blob',
        }),
    exportPDF: (paperId, template = 'generic_article') =>
        api.post(`/export/${paperId}/pdf`, null, {
            params: { template },
            responseType: 'blob',
        }),
    exportZip: (paperId, template = 'generic_article', includePdf = true) =>
        api.post(`/export/${paperId}/zip`, null, {
            params: { template, include_pdf: includePdf },
            responseType: 'blob',
        }),
    getTemplates: () => api.get('/export/templates'),
    getFormats: () => api.get('/export/formats'),
};

// Discovery API (existing)
export const discoveryAPI = {
    checkNovelty: (data) => api.post('/discovery/novelty', data),
    findSimilar: (data) => api.post('/discovery/similar', data),
};

// Generation API (existing)
export const generateAPI = {
    generateSection: (data) => api.post('/generate/section', data),
    generateTopics: (data) => api.post('/generate/topics', data),
};

// Citations API (existing)
export const citationsAPI = {
    create: (data) => api.post('/citations/create', data),
    format: (data) => api.post('/citations/format', data),
    getAll: (paperId) => api.get(`/citations/${paperId}`),
};

export default api;
