'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import Image from 'next/image'
import { LogOut, Upload } from 'lucide-react'
import { useAuthStore } from '@/lib/store'

export default function DashboardHeader() {
  const [isScrolled, setIsScrolled] = useState(false)
  const { user, logout } = useAuthStore()

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20)
    }

    window.addEventListener('scroll', handleScroll, { passive: true })
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

  const handleLogout = () => {
    logout()
    window.location.href = '/'
  }

  return (
    <>
      {/* Fixed Header - Always visible at top */}
      <header
        className={`bg-white/95 backdrop-blur-md fixed top-0 left-0 right-0 z-50 border-b-2 transition-all duration-300 ${
          isScrolled
            ? 'shadow-lg border-gray-300 py-2'
            : 'shadow-md border-gray-200 py-4'
        }`}
      >
        <div className="container mx-auto px-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-3">
              <Image
                src="/logo.png"
                alt="SchoolSharthi Logo"
                width={isScrolled ? 60 : 80}
                height={isScrolled ? 60 : 80}
                className="object-contain transition-all duration-300"
                priority
              />
              <div>
                <h1
                  className={`font-extrabold text-gray-900 transition-all duration-300 ${
                    isScrolled ? 'text-xl' : 'text-2xl'
                  }`}
                >
                  SchoolSharthi
                </h1>
                <p
                  className={`text-gray-600 font-medium transition-all duration-300 ${
                    isScrolled ? 'text-[10px]' : 'text-xs'
                  }`}
                >
                  Har Student Ka Sacha Sarthi
                </p>
              </div>
            </div>
            <div className="flex items-center gap-4">
              <div className={`hidden md:block px-4 py-2 bg-gray-100 border-2 border-gray-200 rounded-lg transition-all duration-300 ${
                isScrolled ? 'text-sm px-3 py-1.5' : ''
              }`}>
                <span className="text-gray-700 font-medium">
                  👋 Welcome, <span className="text-gray-900 font-bold">{user?.full_name || user?.username}</span>
                </span>
              </div>
              {user?.role === 'admin' && (
                <Link
                  href="/admin"
                  className={`bg-gray-900 text-white rounded-lg hover:bg-gray-800 hover:shadow-lg hover:scale-105 transition-all flex items-center gap-2 font-bold border-2 border-gray-900 ${
                    isScrolled ? 'px-3 py-1.5 text-sm' : 'px-4 py-2'
                  }`}
                >
                  <Upload className="w-4 h-4" />
                  Admin Panel
                </Link>
              )}
              <button
                onClick={handleLogout}
                className={`text-gray-700 hover:text-red-600 flex items-center gap-2 font-medium transition-colors ${
                  isScrolled ? 'text-sm' : ''
                }`}
              >
                <LogOut className="w-4 h-4" />
                <span className="hidden sm:inline">Logout</span>
              </button>
            </div>
          </div>
        </div>
      </header>
      {/* Spacer to prevent content from hiding under fixed header */}
      <div
        className={`transition-all duration-300 ${
          isScrolled ? 'h-[72px]' : 'h-[96px]'
        }`}
      />
    </>
  )
}
