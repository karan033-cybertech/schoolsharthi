'use client'

import { useState } from 'react'
import { useMutation, useQuery } from 'react-query'
import { aiAPI } from '@/lib/api'
import { Brain, Send, MessageSquare, Globe } from 'lucide-react'
import Link from 'next/link'
import SmartHeader from '../components/SmartHeader'
import ClassSubjectFilter from '../components/ClassSubjectFilter'

export default function AIDoubtPage() {
  const [question, setQuestion] = useState('')
  const [subject, setSubject] = useState('')
  const [classLevel, setClassLevel] = useState('')
  const [chapter, setChapter] = useState('')

  const { data: doubts, refetch } = useQuery('doubts', () =>
    aiAPI.getDoubts().then((res) => res.data)
  )

  const askMutation = useMutation(
    (data: { question: string; subject?: string; class_level?: string; chapter?: string }) =>
      aiAPI.askDoubt(data),
    {
      onSuccess: () => {
        setQuestion('')
        refetch()
      },
    }
  )

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!question.trim()) return

    askMutation.mutate({
      question,
      subject: subject || undefined,
      class_level: classLevel || undefined,
      chapter: chapter || undefined,
    })
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-50">
      <SmartHeader showAuth={false} />
      <div className="container mx-auto px-4 py-4 border-b border-gray-200">
        <div className="flex justify-between items-center">
          <Link href="/dashboard" className="text-gray-700 hover:text-gray-900 font-semibold flex items-center gap-2 hover:underline transition-colors">
            ← Back to Dashboard
          </Link>
          <h1 className="text-3xl font-extrabold flex items-center gap-3 text-gray-900">
            <div className="w-10 h-10 bg-gradient-to-br from-gray-800 to-gray-900 rounded-xl flex items-center justify-center">
              <Brain className="w-6 h-6 text-white" />
            </div>
            AI Doubt Solver
          </h1>
          <div></div>
        </div>
      </div>

      <main className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Ask Question Form */}
        <div className="bg-white rounded-2xl shadow-lg p-8 mb-8 border-2 border-gray-200 hover:shadow-xl transition-all">
          <div className="flex items-center gap-3 mb-6">
            <div className="w-12 h-12 bg-gradient-to-br from-gray-800 to-gray-900 rounded-xl flex items-center justify-center">
              <span className="text-2xl">💡</span>
            </div>
            <div>
              <h2 className="text-2xl font-bold text-gray-900">Ask Your Question</h2>
              <p className="text-sm text-gray-600 flex items-center gap-1 mt-1">
                <Globe className="w-4 h-4" />
                Write in any language - we&apos;ll respond in the same language
              </p>
            </div>
          </div>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Your Question</label>
              <textarea
                value={question}
                onChange={(e) => setQuestion(e.target.value)}
                placeholder="Type your doubt here in any language (Hindi, English, Hinglish)... We'll respond in the same language!"
                rows={5}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-gray-900 focus:border-gray-900 transition-all resize-none bg-white hover:border-gray-300"
                required
              />
            </div>

            <ClassSubjectFilter
              selectedClass={classLevel}
              selectedSubject={subject}
              onClassChange={(classLevel) => {
                setClassLevel(classLevel)
                setSubject('')
              }}
              onSubjectChange={setSubject}
              className="mb-4"
            />

            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Chapter (Optional)</label>
              <input
                type="text"
                value={chapter}
                onChange={(e) => setChapter(e.target.value)}
                placeholder="Chapter name"
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-gray-900 focus:border-gray-900 transition-all bg-white hover:border-gray-300"
              />
            </div>

            <button
              type="submit"
              disabled={askMutation.isLoading}
              className="w-full py-4 bg-gray-900 text-white rounded-xl font-bold text-lg hover:bg-gray-800 hover:shadow-xl hover:scale-105 disabled:opacity-50 flex items-center justify-center gap-2 transition-all border-2 border-gray-900"
            >
              <Send className="w-5 h-5" />
              {askMutation.isLoading ? '🤔 Thinking...' : '🚀 Ask Question'}
            </button>
          </form>
        </div>

        {/* Previous Doubts */}
        <div className="bg-white rounded-2xl shadow-lg p-8 border-2 border-gray-200 hover:shadow-xl transition-all">
          <h2 className="text-2xl font-bold mb-6 flex items-center gap-3">
            <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-xl flex items-center justify-center">
              <MessageSquare className="w-5 h-5 text-white" />
            </div>
            Previous Questions
          </h2>
          {doubts && doubts.length > 0 ? (
            <div className="space-y-4">
              {doubts.map((doubt: any) => (
                <div key={doubt.id} className="border-2 border-gray-100 rounded-xl p-6 hover:border-primary-300 hover:shadow-lg transition-all bg-white">
                  <div className="mb-3">
                    <p className="font-semibold text-gray-900 text-lg">{doubt.question}</p>
                  </div>
                  {doubt.ai_response && (
                    <div className="mt-4 p-4 bg-gray-50 rounded-xl border-2 border-gray-200">
                      <div className="flex items-start gap-2 mb-2">
                        <span className="text-xl">🤖</span>
                        <span className="font-semibold text-gray-900">AI Response:</span>
                      </div>
                      <p className="text-gray-700 whitespace-pre-wrap leading-relaxed">{doubt.ai_response}</p>
                    </div>
                  )}
                  {!doubt.ai_response && (
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
              <div className="text-6xl mb-4">💭</div>
              <p className="text-gray-600 text-lg font-semibold">No questions asked yet</p>
              <p className="text-gray-500 mt-2">Ask your first question above!</p>
            </div>
          )}
        </div>
      </main>
    </div>
  )
}
