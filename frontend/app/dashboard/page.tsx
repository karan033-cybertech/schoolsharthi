'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/lib/store'
import { BookOpen, FileText, Brain, Briefcase, Lightbulb } from 'lucide-react'
import EnhancedCard from '@/app/components/EnhancedCard'
import FloatingActionButton from '@/app/components/FloatingActionButton'
import DashboardHeader from '@/app/components/DashboardHeader'

export default function DashboardPage() {
  const router = useRouter()
  const { user, logout, loadUser } = useAuthStore()

  useEffect(() => {
    loadUser()
  }, [loadUser])

  useEffect(() => {
    if (!user) {
      router.push('/login')
    }
  }, [user, router])

  if (!user) {
    return <div className="min-h-screen flex items-center justify-center">Loading...</div>
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-50">
      {/* Smart Header */}
      <DashboardHeader />

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <div className="mb-8">
          <h2 className="text-4xl md:text-5xl font-extrabold mb-3 text-gray-900">
            Your Learning Dashboard
          </h2>
          <p className="text-gray-600 text-lg">Choose what you want to explore today</p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          <EnhancedCard
            icon={<BookOpen className="w-8 h-8" />}
            title="📚 Notes"
            description="Browse premium handwritten notes organized by class, subject, and chapter"
            href="/notes"
            gradient="from-gray-800 to-gray-900"
            emoji="📚"
            badge="New"
            delay={0}
          />
          <EnhancedCard
            icon={<FileText className="w-8 h-8" />}
            title="📝 PYQs"
            description="Complete collection of Previous Year Questions for Boards, NEET, JEE"
            href="/pyqs"
            gradient="from-gray-700 to-gray-800"
            emoji="📝"
            delay={100}
          />
          <EnhancedCard
            icon={<Brain className="w-8 h-8" />}
            title="🤖 AI Doubt Solver"
            description="Get instant, step-by-step solutions in Hindi + English (Hinglish)"
            href="/ai-doubt"
            gradient="from-gray-900 to-black"
            emoji="🤖"
            badge="Popular"
            delay={200}
          />
          <EnhancedCard
            icon={<Lightbulb className="w-8 h-8" />}
            title="✨ AI Study Assistant"
            description="Important questions, PYQ patterns, and detailed step-by-step solutions"
            href="/ai-assistant"
            gradient="from-gray-600 to-gray-700"
            emoji="✨"
            delay={300}
          />
          <EnhancedCard
            icon={<Briefcase className="w-8 h-8" />}
            title="💼 Career Guidance"
            description="Expert counseling for stream selection, NEET/JEE strategy, and government exams"
            href="/career"
            gradient="from-gray-800 to-gray-900"
            emoji="💼"
            delay={400}
          />
        </div>
      </main>
      <FloatingActionButton />
    </div>
  )
}

