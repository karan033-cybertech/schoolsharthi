'use client'

import { useState } from 'react'
import { useMutation } from 'react-query'
import { aiAPI } from '@/lib/api'
import { Brain, BookOpen, FileText, Calculator, ArrowLeft, Sparkles } from 'lucide-react'
import Link from 'next/link'

const SUBJECTS = ['physics', 'chemistry', 'biology', 'mathematics']
const CLASS_LEVELS = ['6', '7', '8', '9', '10', '11', '12']
const EXAM_TYPES = ['boards', 'neet', 'jee_main', 'jee_advanced']

export default function AIAssistantPage() {
  const [activeTab, setActiveTab] = useState<'questions' | 'patterns' | 'solution'>('questions')
  const [questionsForm, setQuestionsForm] = useState({
    subject: '',
    class_level: '',
    chapter: '',
    count: 10,
  })
  const [patternsForm, setPatternsForm] = useState({
    exam_type: '',
    subject: '',
    year_range: '',
  })
  const [solutionForm, setSolutionForm] = useState({
    problem: '',
    subject: '',
  })
  const [results, setResults] = useState<{ [key: string]: string }>({})

  const questionsMutation = useMutation(
    (data: any) => aiAPI.generateImportantQuestions(data),
    {
      onSuccess: (res) => {
        setResults({ ...results, questions: res.data.questions })
      },
    }
  )

  const patternsMutation = useMutation(
    (data: any) => aiAPI.getPYQPatterns(data),
    {
      onSuccess: (res) => {
        setResults({ ...results, patterns: res.data.patterns })
      },
    }
  )

  const solutionMutation = useMutation(
    (data: any) => aiAPI.getStepByStepSolution(data),
    {
      onSuccess: (res) => {
        setResults({ ...results, solution: res.data.solution })
      },
    }
  )

  const handleQuestionsSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    questionsMutation.mutate(questionsForm)
  }

  const handlePatternsSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    patternsMutation.mutate(patternsForm)
  }

  const handleSolutionSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    solutionMutation.mutate(solutionForm)
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-50 via-purple-50 to-pink-50">
      <header className="bg-white/80 backdrop-blur-md shadow-sm border-b border-gray-100 sticky top-0 z-50">
        <div className="container mx-auto px-4 py-4">
          <div className="flex justify-between items-center">
            <Link href="/dashboard" className="text-primary-600 hover:text-indigo-600 font-semibold flex items-center gap-2 hover:underline">
              <ArrowLeft className="w-4 h-4" />
              Back to Dashboard
            </Link>
            <h1 className="text-3xl font-extrabold flex items-center gap-3 bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent">
              <div className="w-10 h-10 bg-gradient-to-br from-indigo-500 to-purple-600 rounded-xl flex items-center justify-center">
                <Sparkles className="w-6 h-6 text-white" />
              </div>
              AI Study Assistant
            </h1>
            <div></div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8 max-w-6xl">
        {/* Tabs */}
        <div className="flex gap-2 mb-8 bg-white/80 backdrop-blur-md rounded-2xl p-2 shadow-lg border border-gray-100">
          <button
            onClick={() => setActiveTab('questions')}
            className={`flex-1 px-6 py-4 font-bold rounded-xl flex items-center justify-center gap-2 transition-all ${
              activeTab === 'questions'
                ? 'bg-gradient-to-r from-blue-500 to-cyan-500 text-white shadow-lg scale-105'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <BookOpen className="w-5 h-5" />
            Important Questions
          </button>
          <button
            onClick={() => setActiveTab('patterns')}
            className={`flex-1 px-6 py-4 font-bold rounded-xl flex items-center justify-center gap-2 transition-all ${
              activeTab === 'patterns'
                ? 'bg-gradient-to-r from-green-500 to-emerald-500 text-white shadow-lg scale-105'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <FileText className="w-5 h-5" />
            PYQ Patterns
          </button>
          <button
            onClick={() => setActiveTab('solution')}
            className={`flex-1 px-6 py-4 font-bold rounded-xl flex items-center justify-center gap-2 transition-all ${
              activeTab === 'solution'
                ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white shadow-lg scale-105'
                : 'text-gray-600 hover:bg-gray-100'
            }`}
          >
            <Calculator className="w-5 h-5" />
            Step-by-Step
          </button>
        </div>

        {/* Important Questions Tab */}
        {activeTab === 'questions' && (
          <div className="bg-white/80 backdrop-blur-md rounded-2xl shadow-xl p-8 border border-gray-100">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-12 h-12 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-xl flex items-center justify-center">
                <span className="text-2xl">📚</span>
              </div>
              <h2 className="text-2xl font-bold">Generate Important Questions</h2>
            </div>
            <form onSubmit={handleQuestionsSubmit} className="space-y-4 mb-6">
              <div className="grid md:grid-cols-4 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Subject *</label>
                  <select
                    required
                    value={questionsForm.subject}
                    onChange={(e) => setQuestionsForm({ ...questionsForm, subject: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                  >
                    <option value="">Select Subject</option>
                    {SUBJECTS.map((s) => (
                      <option key={s} value={s}>
                        {s.charAt(0).toUpperCase() + s.slice(1)}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Class *</label>
                  <select
                    required
                    value={questionsForm.class_level}
                    onChange={(e) => setQuestionsForm({ ...questionsForm, class_level: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                  >
                    <option value="">Select Class</option>
                    {CLASS_LEVELS.map((level) => (
                      <option key={level} value={level}>
                        Class {level}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Chapter *</label>
                  <input
                    type="text"
                    required
                    value={questionsForm.chapter}
                    onChange={(e) => setQuestionsForm({ ...questionsForm, chapter: e.target.value })}
                    placeholder="Chapter name"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Count</label>
                  <input
                    type="number"
                    min="5"
                    max="20"
                    value={questionsForm.count}
                    onChange={(e) => setQuestionsForm({ ...questionsForm, count: parseInt(e.target.value) })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={questionsMutation.isLoading}
                className="w-full py-3 bg-primary-600 text-white rounded-lg font-semibold hover:bg-primary-700 disabled:opacity-50"
              >
                {questionsMutation.isLoading ? 'Generating...' : 'Generate Questions'}
              </button>
            </form>

            {results.questions && (
              <div className="mt-8 p-6 bg-gradient-to-br from-blue-50 to-cyan-50 rounded-2xl border-2 border-blue-200">
                <div className="flex items-center gap-2 mb-4">
                  <span className="text-2xl">✨</span>
                  <h3 className="text-xl font-bold text-blue-900">Generated Questions:</h3>
                </div>
                <div className="text-gray-700 whitespace-pre-wrap leading-relaxed bg-white p-4 rounded-xl">{results.questions}</div>
              </div>
            )}
          </div>
        )}

        {/* PYQ Patterns Tab */}
        {activeTab === 'patterns' && (
          <div className="bg-white/80 backdrop-blur-md rounded-2xl shadow-xl p-8 border border-gray-100">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-12 h-12 bg-gradient-to-br from-green-500 to-emerald-500 rounded-xl flex items-center justify-center">
                <span className="text-2xl">📊</span>
              </div>
              <h2 className="text-2xl font-bold">Find PYQ Patterns</h2>
            </div>
            <form onSubmit={handlePatternsSubmit} className="space-y-4 mb-6">
              <div className="grid md:grid-cols-3 gap-4">
                <div>
                  <label className="block text-sm font-medium mb-2">Exam Type *</label>
                  <select
                    required
                    value={patternsForm.exam_type}
                    onChange={(e) => setPatternsForm({ ...patternsForm, exam_type: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                  >
                    <option value="">Select Exam</option>
                    {EXAM_TYPES.map((type) => (
                      <option key={type} value={type}>
                        {type.replace('_', ' ').toUpperCase()}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Subject (Optional)</label>
                  <select
                    value={patternsForm.subject}
                    onChange={(e) => setPatternsForm({ ...patternsForm, subject: e.target.value })}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                  >
                    <option value="">All Subjects</option>
                    {SUBJECTS.map((s) => (
                      <option key={s} value={s}>
                        {s.charAt(0).toUpperCase() + s.slice(1)}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium mb-2">Year Range (Optional)</label>
                  <input
                    type="text"
                    value={patternsForm.year_range}
                    onChange={(e) => setPatternsForm({ ...patternsForm, year_range: e.target.value })}
                    placeholder="e.g., 2019-2023"
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={patternsMutation.isLoading}
                className="w-full py-3 bg-primary-600 text-white rounded-lg font-semibold hover:bg-primary-700 disabled:opacity-50"
              >
                {patternsMutation.isLoading ? 'Analyzing...' : 'Find Patterns'}
              </button>
            </form>

            {results.patterns && (
              <div className="mt-8 p-6 bg-gradient-to-br from-green-50 to-emerald-50 rounded-2xl border-2 border-green-200">
                <div className="flex items-center gap-2 mb-4">
                  <span className="text-2xl">📈</span>
                  <h3 className="text-xl font-bold text-green-900">Pattern Analysis:</h3>
                </div>
                <div className="text-gray-700 whitespace-pre-wrap leading-relaxed bg-white p-4 rounded-xl">{results.patterns}</div>
              </div>
            )}
          </div>
        )}

        {/* Step-by-Step Solution Tab */}
        {activeTab === 'solution' && (
          <div className="bg-white/80 backdrop-blur-md rounded-2xl shadow-xl p-8 border border-gray-100">
            <div className="flex items-center gap-3 mb-6">
              <div className="w-12 h-12 bg-gradient-to-br from-purple-500 to-pink-500 rounded-xl flex items-center justify-center">
                <span className="text-2xl">🧮</span>
              </div>
              <h2 className="text-2xl font-bold">Get Step-by-Step Solution</h2>
            </div>
            <form onSubmit={handleSolutionSubmit} className="space-y-4 mb-6">
              <div>
                <label className="block text-sm font-medium mb-2">Problem *</label>
                <textarea
                  required
                  value={solutionForm.problem}
                  onChange={(e) => setSolutionForm({ ...solutionForm, problem: e.target.value })}
                  placeholder="Enter the problem/question here..."
                  rows={5}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                />
              </div>

              <div>
                <label className="block text-sm font-medium mb-2">Subject (Optional)</label>
                <select
                  value={solutionForm.subject}
                  onChange={(e) => setSolutionForm({ ...solutionForm, subject: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                >
                  <option value="">Select Subject</option>
                  {SUBJECTS.map((s) => (
                    <option key={s} value={s}>
                      {s.charAt(0).toUpperCase() + s.slice(1)}
                    </option>
                  ))}
                </select>
              </div>

              <button
                type="submit"
                disabled={solutionMutation.isLoading}
                className="w-full py-3 bg-primary-600 text-white rounded-lg font-semibold hover:bg-primary-700 disabled:opacity-50"
              >
                {solutionMutation.isLoading ? 'Solving...' : 'Get Solution'}
              </button>
            </form>

            {results.solution && (
              <div className="mt-8 p-6 bg-gradient-to-br from-purple-50 to-pink-50 rounded-2xl border-2 border-purple-200">
                <div className="flex items-center gap-2 mb-4">
                  <span className="text-2xl">✅</span>
                  <h3 className="text-xl font-bold text-purple-900">Step-by-Step Solution:</h3>
                </div>
                <div className="text-gray-700 whitespace-pre-wrap leading-relaxed bg-white p-4 rounded-xl">{results.solution}</div>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  )
}
