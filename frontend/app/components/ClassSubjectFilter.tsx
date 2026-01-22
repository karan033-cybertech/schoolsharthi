'use client'

import { useState, useEffect } from 'react'

// Subject mapping based on class
const SUBJECTS_BY_CLASS: { [key: string]: string[] } = {
  '9': ['English', 'Hindi', 'Maths', 'Science', 'Social Science'],
  '10': ['English', 'Hindi', 'Maths', 'Science', 'Social Science'],
  '11': ['Physics', 'Chemistry', 'Biology', 'Maths', 'English', 'Hindi'],
  '12': ['Physics', 'Chemistry', 'Biology', 'Maths', 'English', 'Hindi'],
}

interface ClassSubjectFilterProps {
  selectedClass: string
  selectedSubject: string
  onClassChange: (classLevel: string) => void
  onSubjectChange: (subject: string) => void
  className?: string
  showLabels?: boolean
}

export default function ClassSubjectFilter({
  selectedClass,
  selectedSubject,
  onClassChange,
  onSubjectChange,
  className = '',
  showLabels = true,
}: ClassSubjectFilterProps) {
  const [availableSubjects, setAvailableSubjects] = useState<string[]>([])

  useEffect(() => {
    if (selectedClass && SUBJECTS_BY_CLASS[selectedClass]) {
      setAvailableSubjects(SUBJECTS_BY_CLASS[selectedClass])
      if (selectedSubject && !SUBJECTS_BY_CLASS[selectedClass].includes(selectedSubject)) {
        onSubjectChange('')
      }
    } else {
      setAvailableSubjects([])
      onSubjectChange('')
    }
  }, [selectedClass, selectedSubject, onSubjectChange])

  // 🔧 Only classes 9 to 12
  const CLASS_LEVELS = ['9', '10', '11', '12']

  return (
    <div className={`grid md:grid-cols-2 gap-4 ${className}`}>
      <div>
        {showLabels && (
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Class {selectedClass && <span className="text-gray-500">(Required)</span>}
          </label>
        )}
        <select
          value={selectedClass}
          onChange={(e) => onClassChange(e.target.value)}
          className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:ring-2 focus:ring-gray-900 focus:border-gray-900 transition-all bg-white hover:border-gray-300"
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
        {showLabels && (
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Subject
            {!selectedClass && (
              <span className="text-gray-400 text-xs ml-1">(Select class first)</span>
            )}
          </label>
        )}
        <select
          value={selectedSubject}
          onChange={(e) => onSubjectChange(e.target.value)}
          disabled={!selectedClass}
          className={`w-full px-4 py-3 border-2 rounded-xl focus:ring-2 focus:ring-gray-900 focus:border-gray-900 transition-all ${
            !selectedClass
              ? 'border-gray-200 bg-gray-50 text-gray-400 cursor-not-allowed'
              : 'border-gray-200 bg-white hover:border-gray-300'
          }`}
        >
          <option value="">
            {selectedClass ? 'Select Subject' : 'Select Class First'}
          </option>
          {availableSubjects.map((subject) => (
            <option key={subject} value={subject}>
              {subject}
            </option>
          ))}
        </select>
      </div>
    </div>
  )
}
