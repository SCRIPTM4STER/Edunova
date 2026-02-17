import { authClient, apiClient } from './client'

export const authApi = {
  login: (payload) => authClient.post('/auth/token/', payload),
  register: (payload) => authClient.post('/auth/register/', payload),
  refresh: (refresh) => authClient.post('/auth/token/refresh/', { refresh }),
  getProfile: () => apiClient.get('/auth/profile/me/'),
  changePassword: (payload) => apiClient.post('/auth/change-password/', payload),
}
