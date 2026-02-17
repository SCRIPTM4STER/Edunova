import { apiClient } from './client'

export const pdfApi = {
  listPdfs: (params) => apiClient.get('/pdf/', { params }),
  uploadPdf: (formData) =>
    apiClient.post('/pdf/upload/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  updatePdf: (id, payload) => apiClient.patch(`/pdf/${id}/`, payload),
  deletePdf: (id) => apiClient.delete(`/pdf/${id}/`),
  downloadPdf: (id) =>
    apiClient.get(`/pdf/${id}/download/`, {
      responseType: 'blob',
    }),
}
