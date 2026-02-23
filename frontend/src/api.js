import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export const api = {
    uploadDocument: async (file) => {
        const formData = new FormData();
        formData.append('file', file);
        return axios.post(`${API_BASE_URL}/documents/upload`, formData, {
            headers: { 'Content-Type': 'multipart/form-data' }
        });
    },

    getHistory: async () => {
        return axios.get(`${API_BASE_URL}/history?limit=10`);
    },

    loadSession: async (sessionId) => {
        return axios.get(`${API_BASE_URL}/history/${sessionId}`);
    },

    summarizeDoc: async (documentId) => {
        return axios.post(`${API_BASE_URL}/summary/`, { document_id: documentId });
    },

    chatWithDocs: async (query, sessionId, documentId) => {
        return axios.post(`${API_BASE_URL}/chat/`, {
            query,
            session_id: sessionId,
            document_id: documentId
        });
    }
};
