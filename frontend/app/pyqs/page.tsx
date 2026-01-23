'use client'

import { useState } from 'react'
import { useQuery } from 'react-query'
import { pyqsAPI } from '@/lib/api'
import { FileText, Download, Eye, AlertCircle } from 'lucide-react'
import Link from 'next/link'
import SmartHeader from '../components/SmartHeader'
import ClassSubjectFilter from '../components/ClassSubjectFilter'

const EXAM_TYPES = ['boards', 'neet', 'jee_main', 'jee_advanced']

interface PYQFilters {
  exam_type: string
  class_level: string
  subject: string
  year: number | undefined
}

export default function PYQsPage() {
  const [filters, setFilters] = useState<PYQFilters>({
    exam_type: '',
    class_level: '',
    subject: '',
    year: undefined,
  })

  const { data: pyqs, isLoading } = useQuery(
    ['pyqs', filters],
    () => {
      const apiParams = {
        exam_type: filters.exam_type || undefined,
        class_level: filters.class_level || undefined,
        subject: filters.subject || undefined,
        year: filters.year,
      }
      return pyqsAPI.getPYQs(apiParams).then((res) => res.data)
    },
    { enabled: true }
  )

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-white to-gray-50">
      <SmartHeader showAuth={false} />
      <div className="container mx-auto px-4 py-4 border-b border-gray-200">
        <div className="flex justify-between items-center">
          <Link href="/dashboard" className="text-gray-700 hover:text-gray-900 font-semibold flex items-center gap-2 hover:underline transition-colors">
            ← Back to Dashboard
          </Link>
          <h1 className="text-3xl font-extrabold text-gray-900">
            📝 Previous Year Questions
          </h1>
          <div></div>
        </div>
      </div>

      <main className="container mx-auto px-4 py-8">
        {/* Filters */}
        <div className="bg-white rounded-2xl shadow-lg p-6 mb-8 border-2 border-gray-200 hover:shadow-xl transition-all">
          <h2 className="text-2xl font-bold mb-6 flex items-center gap-2 text-gray-900">
            <span>🔍</span> Filter PYQs
          </h2>
          {/* Class and Subject - Required First */}
          <ClassSubjectFilter
            selectedClass={filters.class_level}
            selectedSubject={filters.subject}
            onClassChange={(classLevel) => setFilters({ ...filters, class_level: classLevel, subject: '' })}
            onSubjectChange={(subject) => setFilters({ ...filters, subject })}
            className="mb-4"
          />
          {/* Exam Type and Year */}
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Exam Type</label>
              <select
                value={filters.exam_type}
                onChange={(e) => setFilters({ ...filters, exam_type: e.target.value })}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-gray-900 focus:border-gray-900 transition-all bg-white hover:border-gray-300"
              >
                <option value="">All Exams</option>
                {EXAM_TYPES.map((type) => (
                  <option key={type} value={type}>
                    {type.replace('_', ' ').toUpperCase()}
                  </option>
                ))}
              </select>
            </div>
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Year</label>
              <input
                type="number"
                placeholder="e.g., 2023"
                value={filters.year ?? ''}
                onChange={(e) => {
                  const value = e.target.value
                  setFilters({ 
                    ...filters, 
                    year: value === '' ? undefined : Number(value) 
                  })
                }}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-gray-900 focus:border-gray-900 transition-all bg-white hover:border-gray-300"
              />
            </div>
          </div>
        </div>

        {/* PYQs Grid */}
        {isLoading ? (
          <div className="text-center py-12">Loading PYQs...</div>
        ) : pyqs && pyqs.length > 0 ? (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {pyqs.map((pyq: any) => (
              <PYQCard key={pyq.id} pyq={pyq} />
            ))}
          </div>
        ) : (
          <div className="text-center py-12 text-gray-500">No PYQs found</div>
        )}
      </main>
    </div>
  )
}

function PYQCard({ pyq }: { pyq: any }) {
  const [downloadError, setDownloadError] = useState<string | null>(null)

  const handleDownload = async () => {
    setDownloadError(null)
    try {
      const response = await pyqsAPI.downloadPYQ(pyq.id)
      if (response.data.question_paper_url) {
        window.open(response.data.question_paper_url, '_blank')
      }
    } catch (error: any) {
      console.error('Download failed:', error)
      const errorMessage = error.response?.data?.detail || 'Failed to download PYQ. Please try again later.'
      setDownloadError(errorMessage)
      // Auto-hide error after 5 seconds
      setTimeout(() => setDownloadError(null), 5000)
    }
  }

  return (
    <div className="group bg-white/80 backdrop-blur-md rounded-2xl shadow-lg p-6 hover:shadow-2xl transition-all duration-300 hover:-translate-y-2 border border-gray-100">
      {downloadError && (
        <div className="mb-4 p-3 bg-red-50 border-2 border-red-200 rounded-xl flex items-start gap-2">
          <AlertCircle className="w-5 h-5 text-red-600 flex-shrink-0 mt-0.5" />
          <div className="flex-1">
            <p className="text-sm font-semibold text-red-900">Download Error</p>
            <p className="text-xs text-red-700 mt-1">{downloadError}</p>
          </div>
        </div>
      )}
      <div className="flex items-start justify-between mb-4">
        <div className="w-14 h-14 bg-gradient-to-br from-green-500 to-emerald-500 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform">
          <FileText className="w-7 h-7 text-white" />
        </div>
        <button
          onClick={handleDownload}
          className="p-3 text-gray-600 hover:text-green-600 hover:bg-green-50 rounded-xl transition-all"
          title="Download"
        >
          <Download className="w-5 h-5" />
        </button>
      </div>
      <h3 className="text-xl font-bold mb-3 text-gray-900 group-hover:text-green-600 transition-colors">
        {pyq.title}
      </h3>
      <div className="flex flex-wrap gap-2 mb-3">
        <span className="px-3 py-1 bg-gradient-to-r from-green-100 to-emerald-100 text-green-700 rounded-full text-sm font-semibold">
          {pyq.exam_type.replace('_', ' ').toUpperCase()}
        </span>
        {pyq.year && (
          <span className="px-3 py-1 bg-gradient-to-r from-blue-100 to-cyan-100 text-blue-700 rounded-full text-sm font-semibold">
            {pyq.year}
          </span>
        )}
      </div>
      <div className="flex items-center gap-4 text-sm text-gray-500 pt-4 border-t border-gray-100">
        <span className="flex items-center gap-2">
          <Eye className="w-4 h-4" />
          <span className="font-semibold">{pyq.views_count}</span>
        </span>
        <span className="flex items-center gap-2">
          <Download className="w-4 h-4" />
          <span className="font-semibold">{pyq.download_count}</span>
        </span>
      </div>
    </div>
  )
}
