'use client'

import { ReactNode } from 'react'
import Link from 'next/link'
import { ArrowRight, Sparkles } from 'lucide-react'

interface EnhancedCardProps {
  icon: ReactNode
  title: string
  description: string
  href: string
  gradient: string
  emoji?: string
  badge?: string
  delay?: number
}

export default function EnhancedCard({
  icon,
  title,
  description,
  href,
  gradient,
  emoji,
  badge,
  delay = 0
}: EnhancedCardProps) {
  // Ensure gradient is valid, default to grey if not
  const validGradient = gradient || 'from-gray-800 to-gray-900'
  
  return (
    <Link href={href} className="block h-full">
      <div
        className="group relative bg-white rounded-3xl shadow-lg hover:shadow-2xl transition-all duration-500 overflow-hidden border-2 border-gray-200 hover:border-gray-900 h-full flex flex-col"
        style={{
          animationDelay: `${delay}ms`,
          animation: 'fadeInUp 0.6s ease-out forwards',
          opacity: 0
        }}
      >
        {/* Animated gradient background on hover */}
        <div className={`absolute inset-0 bg-gradient-to-br ${validGradient} opacity-0 group-hover:opacity-5 transition-opacity duration-500`} />
        
        {/* Shine effect on hover */}
        <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-700">
          <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent -translate-x-full group-hover:translate-x-full transition-transform duration-1000" />
        </div>

        <div className="relative p-8 flex flex-col flex-1">
          {/* Icon with enhanced animation */}
          <div className="relative mb-6">
            <div className={`absolute inset-0 bg-gradient-to-br ${validGradient} rounded-2xl blur-xl opacity-20 group-hover:opacity-30 transition-opacity duration-500`} />
            <div className={`relative bg-gradient-to-br ${validGradient} text-white w-20 h-20 rounded-2xl flex items-center justify-center shadow-xl group-hover:scale-110 group-hover:rotate-6 transition-all duration-500 border-2 border-gray-800`}>
              {icon}
              {emoji && (
                <span className="absolute -top-2 -right-2 text-3xl animate-bounce">
                  {emoji}
                </span>
              )}
            </div>
            {badge && (
              <div className="absolute -top-2 -right-2 bg-gray-900 text-white text-xs font-bold px-3 py-1 rounded-full shadow-lg animate-pulse border border-gray-700">
                {badge}
              </div>
            )}
          </div>

          {/* Content */}
          <h3 className="text-2xl font-bold mb-3 text-gray-900 group-hover:text-gray-700 transition-colors duration-300">
            {title}
          </h3>
          <p className="text-gray-600 leading-relaxed flex-1 mb-4 group-hover:text-gray-700 transition-colors">
            {description}
          </p>

          {/* CTA with enhanced animation */}
          <div className="flex items-center justify-between mt-auto pt-4 border-t border-gray-200 group-hover:border-gray-900 transition-colors">
            <span className="text-gray-900 font-semibold opacity-0 group-hover:opacity-100 transition-all duration-300 flex items-center gap-2">
              Explore Now
              <ArrowRight className="w-4 h-4 group-hover:translate-x-2 transition-transform duration-300" />
            </span>
            <Sparkles className="w-5 h-5 text-gray-600 opacity-0 group-hover:opacity-100 group-hover:animate-pulse transition-all duration-300" />
          </div>
        </div>

        {/* Decorative corner accent */}
        <div className={`absolute top-0 right-0 w-24 h-24 bg-gradient-to-br ${validGradient} opacity-0 group-hover:opacity-10 rounded-bl-full transition-opacity duration-500`} />
      </div>

      <style jsx>{`
        @keyframes fadeInUp {
          from {
            opacity: 0;
            transform: translateY(30px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }
      `}</style>
    </Link>
  )
}
