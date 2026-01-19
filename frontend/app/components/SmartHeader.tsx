'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import Image from 'next/image'

interface SmartHeaderProps {
  showAuth?: boolean
}

export default function SmartHeader({ showAuth = true }: SmartHeaderProps) {
  const [isScrolled, setIsScrolled] = useState(false)

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 20)
    }

    window.addEventListener('scroll', handleScroll, { passive: true })
    return () => window.removeEventListener('scroll', handleScroll)
  }, [])

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
                width={isScrolled ? 60 : 100}
                height={isScrolled ? 60 : 100}
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
            {showAuth && (
              <nav className="flex gap-4">
                <Link
                  href="/login"
                  className={`px-4 py-2 text-gray-700 hover:text-gray-900 font-semibold transition-all border-b-2 border-transparent hover:border-gray-900 ${
                    isScrolled ? 'text-sm' : ''
                  }`}
                >
                  Login
                </Link>
                <Link
                  href="/register"
                  className={`bg-gray-900 text-white rounded-lg hover:bg-gray-800 hover:shadow-xl hover:scale-105 transition-all font-bold border-2 border-gray-900 ${
                    isScrolled ? 'px-5 py-2 text-sm' : 'px-6 py-2'
                  }`}
                >
                  Sign Up Free
                </Link>
              </nav>
            )}
          </div>
        </div>
      </header>
      {/* Spacer to prevent content from hiding under fixed header */}
      <div
        className={`transition-all duration-300 ${
          isScrolled ? 'h-[72px]' : 'h-[116px]'
        }`}
      />
    </>
  )
}
