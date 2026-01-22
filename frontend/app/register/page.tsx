'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { useAuthStore } from '@/lib/store'

export default function RegisterPage() {
  const router = useRouter()
  const { register, isLoading } = useAuthStore()

  const [formData, setFormData] = useState({
    email: '',
    username: '',
    password: '',
    full_name: '',
  })

  const [error, setError] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    try {
      await register(
        formData.email,
        formData.username,
        formData.password,
        formData.full_name
      )
      router.push('/dashboard')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Registration failed. Please try again.')
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50 px-4 py-8">
      <div className="max-w-md w-full">
        <div className="bg-white/80 backdrop-blur-md rounded-2xl shadow-2xl p-8 border border-gray-100">
          <div className="text-center mb-8">
            <div className="w-16 h-16 bg-gradient-to-br from-primary-500 to-purple-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
              <span className="text-3xl">✨</span>
            </div>
            <h1 className="text-4xl font-extrabold mb-2 bg-gradient-to-r from-primary-600 to-purple-600 bg-clip-text text-transparent">
              Join SchoolSharthi
            </h1>
            <p className="text-gray-600">Start your learning journey today - 100% Free!</p>
          </div>

          {error && (
            <div className="bg-red-50 border-2 border-red-200 text-red-700 px-4 py-3 rounded-xl mb-6 flex items-center gap-2">
              <span>⚠️</span>
              <span>{error}</span>
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-5">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Full Name
              </label>
              <input
                type="text"
                value={formData.full_name}
                onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all"
                placeholder="Enter your full name"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Email
              </label>
              <input
                type="email"
                required
                value={formData.email}
                onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all"
                placeholder="your.email@example.com"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Username
              </label>
              <input
                type="text"
                required
                value={formData.username}
                onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all"
                placeholder="Choose a username"
              />
            </div>

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Password
              </label>
              <input
                type="password"
                required
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all"
                placeholder="Create a strong password"
              />
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="w-full py-4 bg-gradient-to-r from-primary-600 to-purple-600 text-white rounded-xl font-bold text-lg hover:shadow-xl hover:scale-105 disabled:opacity-50 disabled:cursor-not-allowed transition-all"
            >
              {isLoading ? '⏳ Creating account...' : '🚀 Create Free Account'}
            </button>
          </form>

          <p className="mt-6 text-center text-sm text-gray-600">
            Already have an account?{' '}
            <Link href="/login" className="text-primary-600 hover:text-purple-600 font-semibold hover:underline">
              Login here
            </Link>
          </p>
        </div>
      </div>
    </div>
  )
}
