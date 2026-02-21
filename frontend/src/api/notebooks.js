import { apiClient } from './client'

const toFormData = (payload) => {
  const formData = new FormData()
  Object.entries(payload).forEach(([key, value]) => {
    if (value === undefined || value === null || value === '') return
    formData.append(key, value)
  })
  return formData
}

export const notebookApi = {
  getNotebooks: () => apiClient.get('/notebook/notebooks/'),
  createNotebook: (payload) => apiClient.post('/notebook/notebooks/', payload),

  getNotes: (params) => apiClient.get('/notebook/notes/', { params }),
  getNote: (id) => apiClient.get(`/notebook/notes/${id}/`),

  createNote: (payload) => {
    if (payload.image instanceof File) {
      return apiClient.post('/notebook/notes/', toFormData(payload), {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
    }
    return apiClient.post('/notebook/notes/', payload)
  },

  updateNote: (id, payload) => {
    if (payload.image instanceof File) {
      return apiClient.patch(`/notebook/notes/${id}/`, toFormData(payload), {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
    }
    return apiClient.patch(`/notebook/notes/${id}/`, payload)
  },

  deleteNote: (id) => apiClient.delete(`/notebook/notes/${id}/`),
  generatePdfFromNote: (id) => apiClient.post(`/notebook/notes/${id}/generate-pdf/`),
}
