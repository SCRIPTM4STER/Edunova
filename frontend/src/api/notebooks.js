import { apiClient } from './client'

export const notebookApi = {
  getNotebooks: () => apiClient.get('/notebook/notebooks/'),
  createNotebook: (payload) => apiClient.post('/notebook/notebooks/', payload),
  getNotes: (params) => apiClient.get('/notebook/notes/', { params }),
  createNote: (payload) => apiClient.post('/notebook/notes/', payload),
  updateNote: (id, payload) => apiClient.patch(`/notebook/notes/${id}/`, payload),
  deleteNote: (id) => apiClient.delete(`/notebook/notes/${id}/`),
  generatePdfFromNote: (id) => apiClient.post(`/notebook/notes/${id}/generate-pdf/`),
}
