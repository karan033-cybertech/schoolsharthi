'use client'

import { useState } from 'react'
import { useQuery } from 'react-query'
import { notesAPI } from '@/lib/api'
import { BookOpen, Download, Eye, AlertCircle } from 'lucide-react'
import Link from 'next/link'
import SmartHeader from '../components/SmartHeader'
import ClassSubjectFilter from '../components/ClassSubjectFilter'

export default function NotesPage() {
  const [filters, setFilters] = useState({
    class_level: '',
    subject: '',
    chapter: '',
  })

  const { data: notes, isLoading } = useQuery(
    ['notes', filters],
    () => notesAPI.getNotes(filters).then((res) => res.data),
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
            📚 Handwritten Notes
          </h1>
          <div></div>
        </div>
      </div>

      <main className="container mx-auto px-4 py-8">
        {/* Filters */}
        <div className="bg-white rounded-2xl shadow-lg p-6 mb-8 border-2 border-gray-200 hover:shadow-xl transition-all">
          <h2 className="text-2xl font-bold mb-6 flex items-center gap-2 text-gray-900">
            <span>🔍</span> Filter Notes
          </h2>
          <div className="space-y-4">
            <ClassSubjectFilter
              selectedClass={filters.class_level}
              selectedSubject={filters.subject}
              onClassChange={(classLevel) => setFilters({ ...filters, class_level: classLevel, subject: '' })}
              onSubjectChange={(subject) => setFilters({ ...filters, subject })}
            />
            <div>
              <label className="block text-sm font-semibold text-gray-700 mb-2">Chapter</label>
              <input
                type="text"
                placeholder="Search chapter..."
                value={filters.chapter}
                onChange={(e) => setFilters({ ...filters, chapter: e.target.value })}
                className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-gray-900 focus:border-gray-900 transition-all bg-white hover:border-gray-300"
              />
            </div>
          </div>
        </div>

        {/* Notes Grid */}
        {isLoading ? (
          <div className="text-center py-20">
            <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
            <p className="mt-4 text-gray-600 font-semibold">Loading notes...</p>
          </div>
        ) : notes && notes.length > 0 ? (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {notes.map((note: any) => (
              <NoteCard key={note.id} note={note} />
            ))}
          </div>
        ) : (
          <div className="text-center py-20">
            <div className="text-6xl mb-4">📝</div>
            <p className="text-xl text-gray-600 font-semibold">No notes found</p>
            <p className="text-gray-500 mt-2">Try adjusting your filters</p>
          </div>
        )}
      </main>
    </div>
  )
}

function NoteCard({ note }: { note: any }) {
  const [downloadError, setDownloadError] = useState<string | null>(null)

  const handleDownload = async () => {
    setDownloadError(null)
    try {
      const response = await notesAPI.downloadNote(note.id)
      if (response.data.file_url) {
        window.open(response.data.file_url, '_blank')
      }
    } catch (error: any) {
      console.error('Download failed:', error)
      const errorMessage = error.response?.data?.detail || 'Failed to download note. Please try again later.'
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
        <div className="w-14 h-14 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-xl flex items-center justify-center group-hover:scale-110 transition-transform">
          <BookOpen className="w-7 h-7 text-white" />
        </div>
        <button
          onClick={handleDownload}
          className="p-3 text-gray-600 hover:text-primary-600 hover:bg-primary-50 rounded-xl transition-all"
          title="Download"
        >
          <Download className="w-5 h-5" />
        </button>
      </div>
      <h3 className="text-xl font-bold mb-3 text-gray-900 group-hover:text-primary-600 transition-colors">
        {note.title}
      </h3>
      <div className="flex flex-wrap gap-2 mb-3">
        <span className="px-3 py-1 bg-gradient-to-r from-primary-100 to-blue-100 text-primary-700 rounded-full text-sm font-semibold">
          Class {note.class_level}
        </span>
        <span className="px-3 py-1 bg-gradient-to-r from-purple-100 to-pink-100 text-purple-700 rounded-full text-sm font-semibold">
          {note.subject}
        </span>
      </div>
      <p className="text-sm text-gray-600 mb-4 font-medium">{note.chapter}</p>
      <div className="flex items-center gap-4 text-sm text-gray-500 pt-4 border-t border-gray-100">
        <span className="flex items-center gap-2">
          <Eye className="w-4 h-4" />
          <span className="font-semibold">{note.views_count}</span>
        </span>
        <span className="flex items-center gap-2">
          <Download className="w-4 h-4" />
          <span className="font-semibold">{note.download_count}</span>
        </span>
      </div>
    </div>
  )
}
