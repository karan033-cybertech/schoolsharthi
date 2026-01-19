'use client'

import { useState, useEffect } from 'react'
import { useMutation, useQuery } from 'react-query'
import { careerAPI } from '@/lib/api'
import { Briefcase, Send, MessageSquare, GraduationCap, Target, Building2, BookOpen, Wrench } from 'lucide-react'
import Link from 'next/link'
import Image from 'next/image'

export default function CareerPage() {
  const [query, setQuery] = useState('')
  const [guidanceType, setGuidanceType] = useState('')

  const { data: guidanceTypes } = useQuery('guidance-types', () =>
    careerAPI.getGuidanceTypes().then((res) => res.data)
  )

  const { data: queries, refetch } = useQuery('career-queries', () =>
    careerAPI.getQueries().then((res) => res.data)
  )

  const askMutation = useMutation(
    (data: { query: string; guidance_type?: string }) => careerAPI.askQuery(data),
    {
      onSuccess: () => {
        setQuery('')
        setGuidanceType('')
        refetch()
      },
    }
  )

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!query.trim()) return

    askMutation.mutate({ query, guidance_type: guidanceType || undefined })
  }

  const getIcon = (type: string) => {
    switch (type) {
      case 'stream_selection':
        return <GraduationCap className="w-5 h-5" />
      case 'career_roadmap_12th':
        return <Target className="w-5 h-5" />
      case 'neet_jee_strategy':
        return <BookOpen className="w-5 h-5" />
      case 'govt_exams':
        return <Building2 className="w-5 h-5" />
      case 'skill_based':
        return <Wrench className="w-5 h-5" />
      default:
        return <Briefcase className="w-5 h-5" />
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-orange-50 via-red-50 to-pink-50">
      <header className="bg-white/80 backdrop-blur-md shadow-sm border-b border-gray-100 sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            <div className="flex items-center gap-3">
              <Image 
                src="/logo.png" 
                alt="SchoolSharthi Logo" 
                width={60} 
                height={60} 
                className="object-contain"
              />
              <div>
                <Link href="/dashboard" className="text-primary-600 hover:text-orange-600 font-semibold flex items-center gap-2 hover:underline">
                  ← Back to Dashboard
                </Link>
                <p className="text-xs text-gray-600 font-medium">Har Student Ka Sacha Sarthi</p>
              </div>
            </div>
            <h1 className="text-3xl font-extrabold flex items-center gap-3 bg-gradient-to-r from-orange-600 to-red-600 bg-clip-text text-transparent">
              <div className="w-10 h-10 bg-gradient-to-br from-orange-500 to-red-500 rounded-xl flex items-center justify-center">
                <Briefcase className="w-6 h-6 text-white" />
              </div>
              Career Guidance
            </h1>
            <div></div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Guidance Types */}
        {guidanceTypes && guidanceTypes.guidance_types && (
          <div className="bg-white/80 backdrop-blur-md rounded-2xl shadow-xl p-8 mb-8 border border-gray-100">
            <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
              <span>🎯</span> Choose Your Guidance Type
            </h2>
            <div className="grid md:grid-cols-2 gap-4">
              {guidanceTypes.guidance_types.map((type: any) => (
                <button
                  key={type.type}
                  onClick={() => setGuidanceType(type.type)}
                  className={`p-5 border-2 rounded-xl text-left transition-all hover:scale-105 ${
                    guidanceType === type.type
                      ? 'border-orange-500 bg-gradient-to-br from-orange-50 to-red-50 shadow-lg'
                      : 'border-gray-200 hover:border-orange-300 bg-white'
                  }`}
                >
                  <div className="flex items-start gap-3">
                    <div className={`${guidanceType === type.type ? 'text-orange-600' : 'text-gray-400'} mt-1`}>
                      {getIcon(type.type)}
                    </div>
                    <div>
                      <h3 className="font-bold text-gray-900 mb-1">{type.title}</h3>
                      <p className="text-sm text-gray-600">{type.description}</p>
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Ask Query Form */}
        <div className="bg-white/80 backdrop-blur-md rounded-2xl shadow-xl p-8 mb-8 border border-gray-100">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-12 h-12 bg-gradient-to-br from-orange-500 to-red-500 rounded-xl flex items-center justify-center">
              <span className="text-2xl">💼</span>
            </div>
            <h2 className="text-2xl font-bold">Ask Career Question</h2>
          </div>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Your Career Question</label>
              <textarea
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder={
                  guidanceType === 'stream_selection'
                    ? 'E.g., मुझे 10th के बाद कौन सा stream choose करना चाहिए? Science, Commerce, या Arts?'
                    : guidanceType === 'career_roadmap_12th'
                    ? 'E.g., 12th Science के बाद मेरे career options क्या हैं?'
                    : guidanceType === 'neet_jee_strategy'
                    ? 'E.g., NEET की तैयारी कैसे करें? Important topics कौन से हैं?'
                    : guidanceType === 'govt_exams'
                    ? 'E.g., Government jobs के लिए कौन से exams देने चाहिए?'
                    : guidanceType === 'skill_based'
                    ? 'E.g., Skill-based courses कौन से हैं जिनसे जल्दी job मिल सकती है?'
                    : 'E.g., What career options are available after Class 12 Science? What should I study for NEET? etc.'
                }
                rows={6}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-orange-500 focus:border-orange-500 transition-all resize-none"
                required
              />
            </div>

            {guidanceType && (
              <div className="p-4 bg-gradient-to-r from-orange-50 to-red-50 rounded-xl border-2 border-orange-200">
                <div className="flex items-center gap-2">
                  <span className="text-lg">✅</span>
                  <span className="text-sm font-semibold text-orange-700">
                    Selected: {guidanceTypes?.guidance_types?.find((t: any) => t.type === guidanceType)?.title}
                  </span>
                </div>
              </div>
            )}

            <button
              type="submit"
              disabled={askMutation.isLoading}
              className="w-full py-4 bg-gradient-to-r from-orange-600 to-red-600 text-white rounded-xl font-bold text-lg hover:shadow-xl hover:scale-105 disabled:opacity-50 flex items-center justify-center gap-2 transition-all"
            >
              <Send className="w-5 h-5" />
              {askMutation.isLoading ? '🤔 Getting guidance...' : '🚀 Get Career Guidance'}
            </button>
          </form>
        </div>

        {/* Previous Queries */}
        <div className="bg-white/80 backdrop-blur-md rounded-2xl shadow-xl p-8 border border-gray-100">
          <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-orange-500 to-red-500 rounded-xl flex items-center justify-center">
              <MessageSquare className="w-5 h-5 text-white" />
            </div>
            Previous Queries
          </h2>
          {queries && queries.length > 0 ? (
            <div className="space-y-4">
              {queries.map((q: any) => (
                <div key={q.id} className="border-2 border-gray-100 rounded-xl p-6 hover:border-orange-300 hover:shadow-lg transition-all bg-white">
                  <div className="mb-3">
                    <p className="font-semibold text-gray-900 text-lg">{q.query}</p>
                  </div>
                  {q.ai_response && (
                    <div className="mt-4 p-4 bg-gradient-to-br from-orange-50 to-red-50 rounded-xl border border-orange-100">
                      <div className="flex items-start gap-2 mb-2">
                        <span className="text-xl">💡</span>
                        <span className="font-semibold text-orange-700">Career Guidance:</span>
                      </div>
                      <p className="text-gray-700 whitespace-pre-wrap leading-relaxed">{q.ai_response}</p>
                    </div>
                  )}
                  {!q.ai_response && (
                    <div className="mt-4 p-4 bg-yellow-50 rounded-xl border border-yellow-200">
                      <p className="text-yellow-700 font-medium flex items-center gap-2">
                        <span className="animate-spin">⏳</span>
                        Processing your question...
                      </p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-12">
              <div className="text-6xl mb-4">💼</div>
              <p className="text-gray-600 text-lg font-semibold">No queries asked yet</p>
              <p className="text-gray-500 mt-2">Ask your first career question above!</p>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}
