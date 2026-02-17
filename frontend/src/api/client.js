import axios from 'axios'
import { tokenStorage } from '../utils/storage'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api/v1'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
})

const authClient = axios.create({
  baseURL: API_BASE_URL,
})

apiClient.interceptors.request.use((config) => {
  const token = tokenStorage.getAccessToken()
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

let isRefreshing = false
let pendingRequests = []

const resolveQueue = (error, token = null) => {
  pendingRequests.forEach((promise) => {
    if (error) {
      promise.reject(error)
    } else {
      promise.resolve(token)
    }
  })
  pendingRequests = []
}

apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config
    if (
      error.response?.status !== 401 ||
      originalRequest?._retry ||
      originalRequest?.url?.includes('/auth/token/')
    ) {
      return Promise.reject(error)
    }

    if (isRefreshing) {
      return new Promise((resolve, reject) => {
        pendingRequests.push({ resolve, reject })
      }).then((token) => {
        originalRequest.headers.Authorization = `Bearer ${token}`
        return apiClient(originalRequest)
      })
    }

    isRefreshing = true
    originalRequest._retry = true

    try {
      const refresh = tokenStorage.getRefreshToken()
      if (!refresh) throw new Error('Missing refresh token')

      const { data } = await authClient.post('/auth/token/refresh/', { refresh })
      tokenStorage.setTokens({ access: data.access, refresh: data.refresh || refresh })
      resolveQueue(null, data.access)
      originalRequest.headers.Authorization = `Bearer ${data.access}`

      return apiClient(originalRequest)
    } catch (refreshError) {
      resolveQueue(refreshError, null)
      tokenStorage.clear()
      return Promise.reject(refreshError)
    } finally {
      isRefreshing = false
    }
  },
)

export { apiClient, authClient }
