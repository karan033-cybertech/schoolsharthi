'use client'

import { useState } from 'react'
import { MessageCircle, X, HelpCircle, Star } from 'lucide-react'
import FeedbackModal from './FeedbackModal'

export default function FloatingActionButton() {
  const [isOpen, setIsOpen] = useState(false)
  const [showFeedback, setShowFeedback] = useState(false)

  return (
    <>
      <div className="fixed bottom-6 right-6 z-40">
        {/* Main FAB */}
        <button
          onClick={() => setIsOpen(!isOpen)}
          className="w-14 h-14 bg-gray-900 text-white rounded-full shadow-2xl hover:bg-gray-800 hover:shadow-gray-900/50 flex items-center justify-center transition-all duration-300 hover:scale-110 group border-2 border-gray-800"
          aria-label="Help and feedback"
        >
          {isOpen ? (
            <X className="w-6 h-6 transition-transform rotate-90" />
          ) : (
            <MessageCircle className="w-6 h-6 group-hover:scale-110 transition-transform" />
          )}
        </button>

        {/* Action buttons */}
        <div
          className={`absolute bottom-16 right-0 space-y-3 transition-all duration-300 ${
            isOpen
              ? 'opacity-100 translate-y-0 pointer-events-auto'
              : 'opacity-0 translate-y-4 pointer-events-none'
          }`}
        >
          <button
            onClick={() => {
              setShowFeedback(true)
              setIsOpen(false)
            }}
            className="flex items-center gap-3 bg-white text-gray-700 px-4 py-3 rounded-full shadow-lg hover:shadow-xl transition-all hover:scale-105 group"
          >
            <div className="w-10 h-10 bg-gradient-to-br from-yellow-400 to-orange-500 rounded-full flex items-center justify-center group-hover:rotate-12 transition-transform">
              <Star className="w-5 h-5 text-white" />
            </div>
            <span className="font-semibold">Give Feedback</span>
          </button>

          <a
            href="mailto:support@schoolsharthi.com"
            className="flex items-center gap-3 bg-white text-gray-700 px-4 py-3 rounded-full shadow-lg hover:shadow-xl transition-all hover:scale-105 group"
          >
            <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-cyan-500 rounded-full flex items-center justify-center group-hover:rotate-12 transition-transform">
              <HelpCircle className="w-5 h-5 text-white" />
            </div>
            <span className="font-semibold">Get Help</span>
          </a>
        </div>
      </div>

      <FeedbackModal
        isOpen={showFeedback}
        onClose={() => setShowFeedback(false)}
      />
    </>
  )
}
