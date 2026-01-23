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
        class_level: filters.class_level
          ? filters.class_level.toUpperCase()
          : undefined,
        subject: filters.subject
          ? filters.subject.toUpperCase() // ✅ MAIN FIX
          : undefined,
        year: filters.year,
      }

      return pyqsAPI.getPYQs(apiParams).then((res) => res.data)
    },
    { keepPreviousData: true }
  )

  return (
    <div className="min-h-screen bg-gray-50">
      <SmartHeader showAuth={false} />

      <main className="container mx-auto px-4 py-8">
        <ClassSubjectFilter
          selectedClass={filters.class_level}
          selectedSubject={filters.subject}
          onClassChange={(classLevel) =>
            setFilters({
              ...filters,
              class_level: classLevel,
              subject: '',
            })
          }
          onSubjectChange={(subject) =>
            setFilters({ ...filters, subject })
          }
        />

        {isLoading ? (
          <div className="text-center py-10">Loading PYQs...</div>
        ) : pyqs && pyqs.length > 0 ? (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 mt-6">
            {pyqs.map((pyq: any) => (
              <PYQCard key={pyq.id} pyq={pyq} />
            ))}
          </div>
        ) : (
          <div className="text-center py-12 text-gray-500">
            No PYQs found
          </div>
        )}
      </main>
    </div>
  )
}

function PYQCard({ pyq }: { pyq: any }) {
  const [error, setError] = useState<string | null>(null)

  const handleDownload = async () => {
    try {
      const res = await pyqsAPI.downloadPYQ(pyq.id)
      if (res.data.question_paper_url) {
        window.open(res.data.question_paper_url, '_blank')
      }
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Download failed')
      setTimeout(() => setError(null), 4000)
    }
  }

  return (
    <div className="bg-white rounded-xl shadow p-5">
      {error && (
        <div className="mb-3 text-sm text-red-600 flex gap-2">
          <AlertCircle size={16} /> {error}
        </div>
      )}

      <h3 className="font-bold text-lg mb-2">{pyq.title}</h3>

      <div className="flex gap-2 text-sm mb-3">
        <span className="px-2 py-1 bg-gray-100 rounded">
          {pyq.exam_type.toUpperCase()}
        </span>
        {pyq.year && (
          <span className="px-2 py-1 bg-gray-100 rounded">
            {pyq.year}
          </span>
        )}
      </div>

      <div className="flex justify-between items-center text-sm text-gray-500">
        <span className="flex gap-1 items-center">
          <Eye size={14} /> {pyq.views_count}
        </span>

        <button
          onClick={handleDownload}
          className="flex items-center gap-1 text-green-600"
        >
          <Download size={14} /> Download
        </button>
      </div>
    </div>
  )
}
