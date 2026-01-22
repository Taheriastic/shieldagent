import { useState, useEffect, useCallback } from 'react'
import { api } from '../lib/axios'
import type { User, Token, RegisterRequest } from '../types'

interface AuthState {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
}

export function useAuth() {
  const [state, setState] = useState<AuthState>({
    user: null,
    isAuthenticated: false,
    isLoading: true,
  })

  // Load user from localStorage on mount
  useEffect(() => {
    const token = localStorage.getItem('token')
    const userStr = localStorage.getItem('user')
    
    if (token && userStr) {
      try {
        const user = JSON.parse(userStr) as User
        setState({
          user,
          isAuthenticated: true,
          isLoading: false,
        })
      } catch {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        setState({ user: null, isAuthenticated: false, isLoading: false })
      }
    } else {
      setState({ user: null, isAuthenticated: false, isLoading: false })
    }
  }, [])

  const login = useCallback(async (email: string, password: string) => {
    const formData = new FormData()
    formData.append('username', email)
    formData.append('password', password)

    const response = await api.post<Token>('/auth/login', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })

    localStorage.setItem('token', response.data.access_token)

    // Fetch user info
    const userResponse = await api.get<User>('/auth/me')
    localStorage.setItem('user', JSON.stringify(userResponse.data))

    setState({
      user: userResponse.data,
      isAuthenticated: true,
      isLoading: false,
    })

    return userResponse.data
  }, [])

  const register = useCallback(async (data: RegisterRequest) => {
    const response = await api.post<User>('/auth/register', data)
    return response.data
  }, [])

  const logout = useCallback(() => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    setState({
      user: null,
      isAuthenticated: false,
      isLoading: false,
    })
  }, [])

  return {
    user: state.user,
    isAuthenticated: state.isAuthenticated,
    isLoading: state.isLoading,
    login,
    register,
    logout,
  }
}
