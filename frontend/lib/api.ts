import axios from 'axios'
import Cookies from 'js-cookie'

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Add token to requests
api.interceptors.request.use((config) => {
  const token = Cookies.get('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Handle token refresh on 401
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      Cookies.remove('access_token')
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

// Auth APIs
export const authAPI = {
  register: (data: { email: string; username: string; password: string; full_name?: string; role?: string }) =>
    api.post('/api/auth/register', data),
  login: (data: { username: string; password: string }) =>
    api.post('/api/auth/login', data),
  getMe: () => api.get('/api/auth/me'),
}

// Notes APIs
export const notesAPI = {
  getNotes: (params?: { class_level?: string; subject?: string; chapter?: string; skip?: number; limit?: number }) =>
    api.get('/api/notes/', { params }),
  getNote: (id: number) => api.get(`/api/notes/${id}`),
  downloadNote: (id: number) => api.post(`/api/notes/${id}/download`),
}

// PYQs APIs
export const pyqsAPI = {
  getPYQs: (params?: { exam_type?: string; class_level?: string; subject?: string; year?: number; skip?: number; limit?: number }) =>
    api.get('/api/pyqs/', { params }),
  getPYQ: (id: number) => api.get(`/api/pyqs/${id}`),
  downloadPYQ: (id: number) => api.post(`/api/pyqs/${id}/download`),
}

// Admin APIs
export const adminAPI = {
  uploadNote: (formData: FormData) =>
    api.post('/api/admin/notes/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  uploadPYQ: (formData: FormData) =>
    api.post('/api/admin/pyqs/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  getPendingNotes: () => api.get('/api/admin/notes/pending'),
  approveNote: (id: number) => api.post(`/api/admin/notes/${id}/approve`),
  deleteNote: (id: number) => api.delete(`/api/admin/notes/${id}`),
  getAllNotes: (params?: { skip?: number; limit?: number }) =>
    api.get('/api/admin/notes/all', { params }),
  getAllPYQs: (params?: { skip?: number; limit?: number }) =>
    api.get('/api/admin/pyqs/all', { params }),
  deletePYQ: (id: number) => api.delete(`/api/admin/pyqs/${id}`),
  approvePYQ: (id: number) => api.post(`/api/admin/pyqs/${id}/approve`),
  getAllUsers: (params?: { skip?: number; limit?: number }) =>
    api.get('/api/admin/users/all', { params }),
  toggleUserActive: (id: number) => api.post(`/api/admin/users/${id}/toggle-active`),
  deleteUser: (id: number) => api.delete(`/api/admin/users/${id}`),
  makeUserAdmin: (id: number) => api.post(`/api/admin/users/${id}/make-admin`),
  updateAIKey: (apiKey: string, provider: 'groq' | 'openai' = 'groq') => {
    const formData = new FormData()
    formData.append('api_key', apiKey)
    formData.append('provider', provider)
    return api.post('/api/admin/settings/ai-key', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
  getAIKeyStatus: () => api.get('/api/admin/settings/ai-key'),
}

// AI APIs
export const aiAPI = {
  askDoubt: (data: { question: string; subject?: string; class_level?: string; chapter?: string }) =>
    api.post('/api/ai/doubt', data),
  getDoubts: () => api.get('/api/ai/doubts'),
  getDoubt: (id: number) => api.get(`/api/ai/doubts/${id}`),
  generateImportantQuestions: (data: { subject: string; class_level: string; chapter: string; count?: number }) =>
    api.post('/api/ai/important-questions', data),
  getPYQPatterns: (data: { exam_type: string; subject?: string; year_range?: string }) =>
    api.post('/api/ai/pyq-patterns', data),
  getStepByStepSolution: (data: { problem: string; subject?: string }) =>
    api.post('/api/ai/step-by-step', data),
}

// Career APIs
export const careerAPI = {
  askQuery: (data: { query: string; guidance_type?: string }) => api.post('/api/career/query', data),
  getQueries: () => api.get('/api/career/queries'),
  getQuery: (id: number) => api.get(`/api/career/queries/${id}`),
  getGuidanceTypes: () => api.get('/api/career/guidance-types'),
}

// Adaptive Learning APIs
export const learningAPI = {
  getPerformance: () => api.get('/api/learning/performance'),
  getWeakTopicsSummary: (language?: string) => api.get('/api/learning/weak-topics-summary', { params: { language } }),
  getRecommendations: () => api.get('/api/learning/recommendations'),
}

// Smart Revision Mode APIs
export const revisionAPI = {
  generateRevision: (data: { query: string; subject?: string; class_level?: string; language?: string }) =>
    api.post('/api/revision/generate', data),
  quickRevision: (subject: string, class_level?: string, language?: string) =>
    api.get('/api/revision/quick', { params: { subject, class_level, language } }),
}

// Smart Search APIs
export const searchAPI = {
  search: (data: { query: string; search_type?: string; limit?: number }) =>
    api.post('/api/search/search', data),
  quickSearch: (q: string, type?: string, limit?: number) =>
    api.get('/api/search/quick', { params: { q, type, limit } }),
}

// Exam Mode APIs
export const examAPI = {
  createExam: (data: { subject?: string; class_level?: string; exam_type?: string; duration_minutes?: number; total_questions?: number; difficulty?: string }) =>
    api.post('/api/exam/create', data),
  startExam: (examId: number) => api.post(`/api/exam/${examId}/start`),
  getExam: (examId: number) => api.get(`/api/exam/${examId}`),
  getQuestions: (examId: number) => api.get(`/api/exam/${examId}/questions`),
  submitAnswer: (examId: number, data: { question_id: number; selected_answer: string; time_spent_seconds?: number }) =>
    api.post(`/api/exam/${examId}/answer`, data),
  submitExam: (examId: number) => api.post(`/api/exam/${examId}/submit`),
  getResult: (examId: number) => api.get(`/api/exam/${examId}/result`),
  getAnalysis: (examId: number, language?: string) => api.get(`/api/exam/${examId}/analysis`, { params: { language } }),
  listExams: () => api.get('/api/exam/list'),
}

export default api
