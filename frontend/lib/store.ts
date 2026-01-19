import { create } from 'zustand'
import Cookies from 'js-cookie'
import { authAPI } from './api'

interface User {
  id: number
  email: string
  username: string
  full_name?: string
  role: string
  is_active: boolean
}

interface AuthState {
  user: User | null
  token: string | null
  isLoading: boolean
  login: (username: string, password: string) => Promise<void>
  register: (email: string, username: string, password: string, full_name?: string, role?: string) => Promise<void>
  logout: () => void
  loadUser: () => Promise<void>
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: Cookies.get('access_token') || null,
  isLoading: false,

  login: async (username: string, password: string) => {
    set({ isLoading: true })
    try {
      const response = await authAPI.login({ username, password })
      const { access_token } = response.data
      Cookies.set('access_token', access_token, { expires: 7 })
      set({ token: access_token })
      await useAuthStore.getState().loadUser()
    } catch (error) {
      throw error
    } finally {
      set({ isLoading: false })
    }
  },

  register: async (email: string, username: string, password: string, full_name?: string, role?: string) => {
    set({ isLoading: true })
    try {
      await authAPI.register({ email, username, password, full_name, role })
      await useAuthStore.getState().login(username, password)
    } catch (error) {
      throw error
    } finally {
      set({ isLoading: false })
    }
  },

  logout: () => {
    Cookies.remove('access_token')
    set({ user: null, token: null })
  },

  loadUser: async () => {
    const token = Cookies.get('access_token')
    if (!token) {
      set({ user: null })
      return
    }

    try {
      const response = await authAPI.getMe()
      set({ user: response.data })
    } catch (error) {
      Cookies.remove('access_token')
      set({ user: null, token: null })
    }
  },
}))
