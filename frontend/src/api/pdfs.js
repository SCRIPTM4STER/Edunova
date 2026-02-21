import { apiClient } from './client'

const toFormData = (payload) => {
  const formData = new FormData()
  Object.entries(payload).forEach(([key, value]) => {
    if (value === undefined || value === null || value === '') return
    formData.append(key, value)
  })
  return formData
}

export const pdfApi = {
  listPdfs: (params) => apiClient.get('/pdf/', { params }),
  getPdf: (id) => apiClient.get(`/pdf/${id}/`),

  uploadPdf: (payload, onUploadProgress) =>
    apiClient.post('/pdf/upload/', toFormData(payload), {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress,
    }),

  updatePdf: (id, payload) => {
    const hasBinary = payload.file instanceof File || payload.cover_image instanceof File
    if (hasBinary) {
      return apiClient.patch(`/pdf/${id}/`, toFormData(payload), {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
    }
    return apiClient.patch(`/pdf/${id}/`, payload)
  },

  deletePdf: (id) => apiClient.delete(`/pdf/${id}/`),
  downloadPdf: (id) => apiClient.get(`/pdf/${id}/download/`, { responseType: 'blob' }),
}
