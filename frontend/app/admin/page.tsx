'use client'

import { useState, useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/lib/store'
import { adminAPI } from '@/lib/api'
import { useQuery, useMutation, useQueryClient } from 'react-query'
import { Upload, FileText, BookOpen, Users, Settings, Trash2, Check, X, Eye, Key, Shield, UserCheck, UserX } from 'lucide-react'
import Link from 'next/link'
import Image from 'next/image'

type TabType = 'upload-note' | 'upload-pyq' | 'manage-notes' | 'manage-pyqs' | 'manage-users' | 'ai-settings'

// Helper function to get subjects based on class level
function getSubjectsForClass(classLevel: string): string[] {
  const classNum = parseInt(classLevel)
  if (classNum >= 6 && classNum <= 10) {
    // Classes 6-10: hindi, english, maths, science, socialscience
    return ['hindi', 'english', 'mathematics', 'science', 'socialscience']
  } else if (classNum === 11 || classNum === 12) {
    // Classes 11-12: physics, chemistry, maths, biology
    return ['physics', 'chemistry', 'mathematics', 'biology']
  }
  return []
}

export default function AdminPage() {
  const router = useRouter()
  const { user } = useAuthStore()
  const [activeTab, setActiveTab] = useState<TabType>('upload-note')

  useEffect(() => {
    if (!user || user.role !== 'admin') {
      router.push('/dashboard')
    }
  }, [user, router])

  if (!user || user.role !== 'admin') {
    return null
  }

  const tabs = [
    { id: 'upload-note' as TabType, label: 'Upload Note', icon: BookOpen },
    { id: 'upload-pyq' as TabType, label: 'Upload PYQ', icon: FileText },
    { id: 'manage-notes' as TabType, label: 'Manage Notes', icon: BookOpen },
    { id: 'manage-pyqs' as TabType, label: 'Manage PYQs', icon: FileText },
    { id: 'manage-users' as TabType, label: 'Manage Users', icon: Users },
    { id: 'ai-settings' as TabType, label: 'AI Settings', icon: Settings },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-purple-50 to-pink-50">
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
                <Link href="/dashboard" className="text-primary-600 hover:text-purple-600 font-semibold flex items-center gap-2 hover:underline">
                  ← Back to Dashboard
                </Link>
                <p className="text-xs text-gray-600 font-medium">Har Student Ka Sacha Sarthi</p>
              </div>
            </div>
            <h1 className="text-2xl font-bold bg-gradient-to-r from-primary-600 to-purple-600 bg-clip-text text-transparent">
              Admin Panel
            </h1>
            <div></div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-8">
        {/* Tabs */}
        <div className="flex flex-wrap gap-2 mb-6 border-b border-gray-200 pb-2">
          {tabs.map((tab) => {
            const Icon = tab.icon
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-4 py-2 font-semibold rounded-t-lg transition-all flex items-center gap-2 ${
                  activeTab === tab.id
                    ? 'bg-primary-600 text-white shadow-lg'
                    : 'bg-white text-gray-600 hover:bg-gray-100'
                }`}
              >
                <Icon className="w-4 h-4" />
                {tab.label}
              </button>
            )
          })}
        </div>

        {/* Content */}
        {activeTab === 'upload-note' && <UploadNoteForm />}
        {activeTab === 'upload-pyq' && <UploadPYQForm />}
        {activeTab === 'manage-notes' && <ManageNotes />}
        {activeTab === 'manage-pyqs' && <ManagePYQs />}
        {activeTab === 'manage-users' && <ManageUsers />}
        {activeTab === 'ai-settings' && <AISettings />}
      </main>
    </div>
  )
}

function UploadNoteForm() {
  const [formData, setFormData] = useState({
    title: '',
    class_level: '',
    subject: '',
    chapter: '',
    description: '',
  })
  const [file, setFile] = useState<File | null>(null)
  const [thumbnail, setThumbnail] = useState<File | null>(null)
  const [isUploading, setIsUploading] = useState(false)
  const [message, setMessage] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!file) {
      setMessage('Please select a file')
      return
    }

    setIsUploading(true)
    setMessage('')

    try {
      const formDataToSend = new FormData()
      formDataToSend.append('title', formData.title)
      formDataToSend.append('class_level', formData.class_level)
      formDataToSend.append('subject', formData.subject)
      formDataToSend.append('chapter', formData.chapter)
      formDataToSend.append('description', formData.description)
      formDataToSend.append('file', file)
      if (thumbnail) {
        formDataToSend.append('thumbnail', thumbnail)
      }

      await adminAPI.uploadNote(formDataToSend)
      setMessage('✅ Note uploaded successfully!')
      setFormData({ title: '', class_level: '', subject: '', chapter: '', description: '' })
      setFile(null)
      setThumbnail(null)
    } catch (error: any) {
      // Show detailed error message from backend
      let errorMessage = 'Upload failed'
      
      if (error.response) {
        // Backend returned an error response
        errorMessage = error.response.data?.detail || error.response.data?.message || error.response.statusText || 'Upload failed'
        console.error('Upload error (backend):', error.response.data || error.response)
      } else if (error.request) {
        // Request was made but no response received (network error)
        errorMessage = 'Network error: Could not connect to server. Please check your connection and try again.'
        console.error('Upload error (network):', error.request)
      } else {
        // Something else happened
        errorMessage = error.message || 'Upload failed'
        console.error('Upload error (other):', error)
      }
      
      setMessage('❌ ' + errorMessage)
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <div className="bg-white/80 backdrop-blur-md rounded-2xl shadow-xl p-8 border border-gray-100">
      <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
        <BookOpen className="w-6 h-6" />
        Upload Handwritten Note
      </h2>
      {message && (
        <div
          className={`mb-4 p-4 rounded-xl ${
            message.includes('✅') ? 'bg-green-100 text-green-700 border-2 border-green-300' : 'bg-red-100 text-red-700 border-2 border-red-300'
          }`}
        >
          {message}
        </div>
      )}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">Title *</label>
          <input
            type="text"
            required
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all"
          />
        </div>

        <div className="grid md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Class *</label>
            <select
              required
              value={formData.class_level}
              onChange={(e) => {
                const newClass = e.target.value
                // Reset subject when class changes
                setFormData({ ...formData, class_level: newClass, subject: '' })
              }}
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all"
            >
              <option value="">Select Class</option>
              {['6', '7', '8', '9', '10', '11', '12'].map((level) => (
                <option key={level} value={level}>
                  Class {level}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Subject *</label>
            <select
              required
              value={formData.subject}
              onChange={(e) => setFormData({ ...formData, subject: e.target.value })}
              disabled={!formData.class_level}
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all disabled:bg-gray-100 disabled:cursor-not-allowed"
            >
              <option value="">{formData.class_level ? 'Select Subject' : 'Select Class first'}</option>
              {getSubjectsForClass(formData.class_level).map((subject) => (
                <option key={subject} value={subject}>
                  {subject === 'socialscience' ? 'Social Science' : subject.charAt(0).toUpperCase() + subject.slice(1)}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Chapter *</label>
            <input
              type="text"
              required
              value={formData.chapter}
              onChange={(e) => setFormData({ ...formData, chapter: e.target.value })}
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all"
            />
          </div>
        </div>

        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">Description</label>
          <textarea
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            rows={3}
            className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all resize-none"
          />
        </div>

        <div className="grid md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Note File (PDF/Image) *</label>
            <input
              type="file"
              required
              accept=".pdf,.jpg,.jpeg,.png"
              onChange={(e) => setFile(e.target.files?.[0] || null)}
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Thumbnail (Optional)</label>
            <input
              type="file"
              accept=".jpg,.jpeg,.png"
              onChange={(e) => setThumbnail(e.target.files?.[0] || null)}
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all"
            />
          </div>
        </div>

        <button
          type="submit"
          disabled={isUploading}
          className="w-full py-4 bg-gradient-to-r from-primary-600 to-purple-600 text-white rounded-xl font-bold text-lg hover:shadow-xl hover:scale-105 disabled:opacity-50 flex items-center justify-center gap-2 transition-all"
        >
          <Upload className="w-5 h-5" />
          {isUploading ? 'Uploading...' : 'Upload Note'}
        </button>
      </form>
    </div>
  )
}

function UploadPYQForm() {
  const [formData, setFormData] = useState({
    title: '',
    exam_type: '',
    year: '',
    class_level: '',
    subject: '',
  })
  const [questionPaper, setQuestionPaper] = useState<File | null>(null)
  const [answerKey, setAnswerKey] = useState<File | null>(null)
  const [solution, setSolution] = useState<File | null>(null)
  const [isUploading, setIsUploading] = useState(false)
  const [message, setMessage] = useState('')

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!questionPaper && !answerKey && !solution) {
      setMessage('Please upload at least one file')
      return
    }

    setIsUploading(true)
    setMessage('')

    try {
      const formDataToSend = new FormData()
      formDataToSend.append('title', formData.title)
      formDataToSend.append('exam_type', formData.exam_type)
      formDataToSend.append('year', formData.year)
      if (formData.class_level) {
        formDataToSend.append('class_level', formData.class_level)
      }
      if (formData.subject) {
        formDataToSend.append('subject', formData.subject)
      }
      if (questionPaper) {
        formDataToSend.append('question_paper', questionPaper)
      }
      if (answerKey) {
        formDataToSend.append('answer_key', answerKey)
      }
      if (solution) {
        formDataToSend.append('solution', solution)
      }

      await adminAPI.uploadPYQ(formDataToSend)
      setMessage('✅ PYQ uploaded successfully!')
      setFormData({ title: '', exam_type: '', year: '', class_level: '', subject: '' })
      setQuestionPaper(null)
      setAnswerKey(null)
      setSolution(null)
    } catch (error: any) {
      // Show detailed error message from backend
      let errorMessage = 'Upload failed'
      
      if (error.response) {
        // Backend returned an error response
        errorMessage = error.response.data?.detail || error.response.data?.message || error.response.statusText || 'Upload failed'
        console.error('PYQ upload error (backend):', error.response.data || error.response)
      } else if (error.request) {
        // Request was made but no response received (network error)
        errorMessage = 'Network error: Could not connect to server. Please check your connection and try again.'
        console.error('PYQ upload error (network):', error.request)
      } else {
        // Something else happened
        errorMessage = error.message || 'Upload failed'
        console.error('PYQ upload error (other):', error)
      }
      
      setMessage('❌ ' + errorMessage)
    } finally {
      setIsUploading(false)
    }
  }

  return (
    <div className="bg-white/80 backdrop-blur-md rounded-2xl shadow-xl p-8 border border-gray-100">
      <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
        <FileText className="w-6 h-6" />
        Upload Previous Year Question
      </h2>
      {message && (
        <div
          className={`mb-4 p-4 rounded-xl ${
            message.includes('✅') ? 'bg-green-100 text-green-700 border-2 border-green-300' : 'bg-red-100 text-red-700 border-2 border-red-300'
          }`}
        >
          {message}
        </div>
      )}
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">Title *</label>
          <input
            type="text"
            required
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all"
          />
        </div>

        <div className="grid md:grid-cols-4 gap-4">
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Exam Type *</label>
            <select
              required
              value={formData.exam_type}
              onChange={(e) => setFormData({ ...formData, exam_type: e.target.value })}
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all"
            >
              <option value="">Select Exam</option>
              {['boards', 'neet', 'jee_main', 'jee_advanced'].map((type) => (
                <option key={type} value={type}>
                  {type.replace('_', ' ').toUpperCase()}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Year *</label>
            <input
              type="number"
              required
              value={formData.year}
              onChange={(e) => setFormData({ ...formData, year: e.target.value })}
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Class</label>
            <select
              value={formData.class_level}
              onChange={(e) => {
                const newClass = e.target.value
                // Reset subject when class changes
                setFormData({ ...formData, class_level: newClass, subject: '' })
              }}
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all"
            >
              <option value="">Select Class</option>
              {['6', '7', '8', '9', '10', '11', '12'].map((level) => (
                <option key={level} value={level}>
                  Class {level}
                </option>
              ))}
            </select>
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Subject</label>
            <select
              value={formData.subject}
              onChange={(e) => setFormData({ ...formData, subject: e.target.value })}
              disabled={!formData.class_level}
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all disabled:bg-gray-100 disabled:cursor-not-allowed"
            >
              <option value="">{formData.class_level ? 'Select Subject' : 'Select Class first'}</option>
              {getSubjectsForClass(formData.class_level).map((subject) => (
                <option key={subject} value={subject}>
                  {subject === 'socialscience' ? 'Social Science' : subject.charAt(0).toUpperCase() + subject.slice(1)}
                </option>
              ))}
            </select>
          </div>
        </div>

        <div className="grid md:grid-cols-3 gap-4">
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Question Paper</label>
            <input
              type="file"
              accept=".pdf"
              onChange={(e) => setQuestionPaper(e.target.files?.[0] || null)}
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Answer Key</label>
            <input
              type="file"
              accept=".pdf"
              onChange={(e) => setAnswerKey(e.target.files?.[0] || null)}
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">Solution</label>
            <input
              type="file"
              accept=".pdf"
              onChange={(e) => setSolution(e.target.files?.[0] || null)}
              className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all"
            />
          </div>
        </div>

        <button
          type="submit"
          disabled={isUploading}
          className="w-full py-4 bg-gradient-to-r from-primary-600 to-purple-600 text-white rounded-xl font-bold text-lg hover:shadow-xl hover:scale-105 disabled:opacity-50 flex items-center justify-center gap-2 transition-all"
        >
          <Upload className="w-5 h-5" />
          {isUploading ? 'Uploading...' : 'Upload PYQ'}
        </button>
      </form>
    </div>
  )
}

function ManageNotes() {
  const queryClient = useQueryClient()
  const { data: notes, isLoading } = useQuery('admin-notes', () =>
    adminAPI.getAllNotes({ limit: 100 }).then((res) => res.data)
  )

  const deleteMutation = useMutation(
    (id: number) => adminAPI.deleteNote(id),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('admin-notes')
      },
    }
  )

  if (isLoading) {
    return <div className="text-center py-12">Loading notes...</div>
  }

  return (
    <div className="bg-white/80 backdrop-blur-md rounded-2xl shadow-xl p-8 border border-gray-100">
      <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
        <BookOpen className="w-6 h-6" />
        Manage Notes ({notes?.length || 0})
      </h2>
      <div className="space-y-4">
        {notes && notes.length > 0 ? (
          notes.map((note: any) => (
            <div key={note.id} className="border-2 border-gray-200 rounded-xl p-6 hover:border-primary-300 hover:shadow-lg transition-all bg-white">
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <h3 className="text-xl font-bold mb-2">{note.title}</h3>
                  <div className="flex flex-wrap gap-2 mb-2">
                    <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm font-semibold">
                      Class {note.class_level}
                    </span>
                    <span className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm font-semibold">
                      {note.subject}
                    </span>
                    <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-semibold">
                      {note.chapter}
                    </span>
                    <span className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm font-semibold">
                      👁️ {note.views_count} | ⬇️ {note.download_count}
                    </span>
                  </div>
                  {note.description && <p className="text-gray-600 mt-2">{note.description}</p>}
                </div>
                <button
                  onClick={() => {
                    if (confirm('Are you sure you want to delete this note?')) {
                      deleteMutation.mutate(note.id)
                    }
                  }}
                  className="ml-4 p-3 text-red-600 hover:bg-red-50 rounded-xl transition-all"
                  title="Delete"
                >
                  <Trash2 className="w-5 h-5" />
                </button>
              </div>
            </div>
          ))
        ) : (
          <div className="text-center py-12 text-gray-500">No notes found</div>
        )}
      </div>
    </div>
  )
}

function ManagePYQs() {
  const queryClient = useQueryClient()
  const { data: pyqs, isLoading } = useQuery('admin-pyqs', () =>
    adminAPI.getAllPYQs({ limit: 100 }).then((res) => res.data)
  )

  const deleteMutation = useMutation(
    (id: number) => adminAPI.deletePYQ(id),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('admin-pyqs')
      },
    }
  )

  if (isLoading) {
    return <div className="text-center py-12">Loading PYQs...</div>
  }

  return (
    <div className="bg-white/80 backdrop-blur-md rounded-2xl shadow-xl p-8 border border-gray-100">
      <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
        <FileText className="w-6 h-6" />
        Manage PYQs ({pyqs?.length || 0})
      </h2>
      <div className="space-y-4">
        {pyqs && pyqs.length > 0 ? (
          pyqs.map((pyq: any) => (
            <div key={pyq.id} className="border-2 border-gray-200 rounded-xl p-6 hover:border-primary-300 hover:shadow-lg transition-all bg-white">
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <h3 className="text-xl font-bold mb-2">{pyq.title}</h3>
                  <div className="flex flex-wrap gap-2 mb-2">
                    <span className="px-3 py-1 bg-orange-100 text-orange-700 rounded-full text-sm font-semibold">
                      {pyq.exam_type.replace('_', ' ').toUpperCase()}
                    </span>
                    <span className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm font-semibold">
                      Year {pyq.year}
                    </span>
                    {pyq.class_level && (
                      <span className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm font-semibold">
                        Class {pyq.class_level}
                      </span>
                    )}
                    {pyq.subject && (
                      <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-semibold">
                        {pyq.subject}
                      </span>
                    )}
                    <span className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm font-semibold">
                      👁️ {pyq.views_count} | ⬇️ {pyq.download_count}
                    </span>
                  </div>
                </div>
                <button
                  onClick={() => {
                    if (confirm('Are you sure you want to delete this PYQ?')) {
                      deleteMutation.mutate(pyq.id)
                    }
                  }}
                  className="ml-4 p-3 text-red-600 hover:bg-red-50 rounded-xl transition-all"
                  title="Delete"
                >
                  <Trash2 className="w-5 h-5" />
                </button>
              </div>
            </div>
          ))
        ) : (
          <div className="text-center py-12 text-gray-500">No PYQs found</div>
        )}
      </div>
    </div>
  )
}

function ManageUsers() {
  const queryClient = useQueryClient()
  const { data: users, isLoading } = useQuery('admin-users', () =>
    adminAPI.getAllUsers({ limit: 100 }).then((res) => res.data)
  )

  const toggleActiveMutation = useMutation(
    (id: number) => adminAPI.toggleUserActive(id),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('admin-users')
      },
    }
  )

  const deleteMutation = useMutation(
    (id: number) => adminAPI.deleteUser(id),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('admin-users')
      },
    }
  )

  const makeAdminMutation = useMutation(
    (id: number) => adminAPI.makeUserAdmin(id),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('admin-users')
      },
    }
  )

  if (isLoading) {
    return <div className="text-center py-12">Loading users...</div>
  }

  return (
    <div className="bg-white/80 backdrop-blur-md rounded-2xl shadow-xl p-8 border border-gray-100">
      <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
        <Users className="w-6 h-6" />
        Manage Users ({users?.length || 0})
      </h2>
      <div className="space-y-4">
        {users && users.length > 0 ? (
          users.map((user: any) => (
            <div key={user.id} className="border-2 border-gray-200 rounded-xl p-6 hover:border-primary-300 hover:shadow-lg transition-all bg-white">
              <div className="flex justify-between items-start">
                <div className="flex-1">
                  <div className="flex items-center gap-3 mb-2">
                    <h3 className="text-xl font-bold">{user.full_name || user.username}</h3>
                    {user.role === 'admin' && (
                      <span className="px-3 py-1 bg-purple-100 text-purple-700 rounded-full text-sm font-semibold flex items-center gap-1">
                        <Shield className="w-4 h-4" />
                        Admin
                      </span>
                    )}
                    {!user.is_active && (
                      <span className="px-3 py-1 bg-red-100 text-red-700 rounded-full text-sm font-semibold">
                        Inactive
                      </span>
                    )}
                  </div>
                  <p className="text-gray-600 mb-1">@{user.username}</p>
                  <p className="text-gray-600 mb-2">{user.email}</p>
                  <p className="text-sm text-gray-500">Joined: {new Date(user.created_at).toLocaleDateString()}</p>
                </div>
                <div className="flex gap-2">
                  {user.role !== 'admin' && (
                    <button
                      onClick={() => {
                        if (confirm(`Make ${user.username} an admin?`)) {
                          makeAdminMutation.mutate(user.id)
                        }
                      }}
                      className="p-3 text-purple-600 hover:bg-purple-50 rounded-xl transition-all"
                      title="Make Admin"
                    >
                      <Shield className="w-5 h-5" />
                    </button>
                  )}
                  <button
                    onClick={() => {
                      toggleActiveMutation.mutate(user.id)
                    }}
                    className="p-3 text-blue-600 hover:bg-blue-50 rounded-xl transition-all"
                    title={user.is_active ? 'Deactivate' : 'Activate'}
                  >
                    {user.is_active ? <UserX className="w-5 h-5" /> : <UserCheck className="w-5 h-5" />}
                  </button>
                  <button
                    onClick={() => {
                      if (confirm(`Are you sure you want to delete user ${user.username}?`)) {
                        deleteMutation.mutate(user.id)
                      }
                    }}
                    className="p-3 text-red-600 hover:bg-red-50 rounded-xl transition-all"
                    title="Delete"
                  >
                    <Trash2 className="w-5 h-5" />
                  </button>
                </div>
              </div>
            </div>
          ))
        ) : (
          <div className="text-center py-12 text-gray-500">No users found</div>
        )}
      </div>
    </div>
  )
}

function AISettings() {
  const { data: keyStatus } = useQuery('ai-key-status', () =>
    adminAPI.getAIKeyStatus().then((res) => res.data)
  )
  const [apiKey, setApiKey] = useState('')
  const [provider, setProvider] = useState<'groq' | 'openai'>('groq')
  const [message, setMessage] = useState('')
  const [isSaving, setIsSaving] = useState(false)

  const handleSave = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!apiKey.trim()) {
      setMessage('Please enter an API key')
      return
    }

    setIsSaving(true)
    setMessage('')

    try {
      await adminAPI.updateAIKey(apiKey, provider)
      setMessage(`✅ ${provider.toUpperCase()} API key updated successfully! Please restart the backend server for changes to take effect.`)
      setApiKey('')
    } catch (error: any) {
      setMessage('❌ ' + (error.response?.data?.detail || 'Failed to update API key'))
    } finally {
      setIsSaving(false)
    }
  }

  return (
    <div className="bg-white/80 backdrop-blur-md rounded-2xl shadow-xl p-8 border border-gray-100">
      <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
        <Settings className="w-6 h-6" />
        AI Settings
      </h2>

      <div className="mb-6 p-4 bg-blue-50 border-2 border-blue-200 rounded-xl">
        <div className="flex items-center gap-2 mb-2">
          <Key className="w-5 h-5 text-blue-600" />
          <span className="font-semibold text-blue-900">AI API Key Status</span>
        </div>
        {keyStatus?.configured ? (
          <div className="space-y-1">
            {keyStatus.has_groq && (
              <p className="text-blue-700">
                ✅ Groq API Key is configured ({keyStatus.groq_preview}) - <strong>Active</strong>
              </p>
            )}
            {keyStatus.has_openai && (
              <p className="text-blue-700">
                ✅ OpenAI API Key is configured ({keyStatus.openai_preview})
              </p>
            )}
            <p className="text-sm text-blue-600 mt-2">
              Current provider: <strong>{keyStatus.provider?.toUpperCase() || 'None'}</strong>
            </p>
          </div>
        ) : (
          <p className="text-orange-700">
            ⚠️ No API key configured. AI features will use placeholder responses.
            <br />
            <span className="text-sm">💡 We recommend using Groq (free and fast!)</span>
          </p>
        )}
      </div>

      {message && (
        <div
          className={`mb-4 p-4 rounded-xl ${
            message.includes('✅') ? 'bg-green-100 text-green-700 border-2 border-green-300' : 'bg-red-100 text-red-700 border-2 border-red-300'
          }`}
        >
          {message}
        </div>
      )}

      <form onSubmit={handleSave} className="space-y-4">
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">AI Provider</label>
          <select
            value={provider}
            onChange={(e) => setProvider(e.target.value as 'groq' | 'openai')}
            className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all bg-white"
          >
            <option value="groq">Groq (Recommended - Free & Fast)</option>
            <option value="openai">OpenAI</option>
          </select>
          {provider === 'groq' && (
            <p className="text-sm text-green-600 mt-2 font-medium">
              ✨ Groq is free, fast, and perfect for this application!
            </p>
          )}
        </div>

        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            {provider === 'groq' ? 'Groq' : 'OpenAI'} API Key
          </label>
          <input
            type="password"
            value={apiKey}
            onChange={(e) => setApiKey(e.target.value)}
            placeholder={provider === 'groq' ? 'gsk_...' : 'sk-proj-...'}
            className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-all font-mono"
          />
          <p className="text-sm text-gray-500 mt-2">
            Enter your {provider === 'groq' ? 'Groq' : 'OpenAI'} API key. This will be saved to the backend .env file.
          </p>
        </div>

        <button
          type="submit"
          disabled={isSaving}
          className="w-full py-4 bg-gradient-to-r from-primary-600 to-purple-600 text-white rounded-xl font-bold text-lg hover:shadow-xl hover:scale-105 disabled:opacity-50 flex items-center justify-center gap-2 transition-all"
        >
          <Key className="w-5 h-5" />
          {isSaving ? 'Saving...' : `Save ${provider === 'groq' ? 'Groq' : 'OpenAI'} API Key`}
        </button>
      </form>

      <div className="mt-6 p-4 bg-yellow-50 border-2 border-yellow-200 rounded-xl">
        <p className="text-sm text-yellow-800">
          <strong>Note:</strong> After updating the API key, you need to restart the backend server for the changes to take effect.
        </p>
      </div>
    </div>
  )
}
