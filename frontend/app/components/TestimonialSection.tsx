'use client'

import { Star, Quote } from 'lucide-react'
import { useState, useEffect } from 'react'

interface Testimonial {
  name: string
  class: string
  location: string
  rating: number
  text: string
  avatar: string
}

const testimonials: Testimonial[] = [
  {
    name: 'Priya Sharma',
    class: 'Class 12',
    location: 'Delhi',
    rating: 5,
    text: 'SchoolSharthi helped me score 95% in Boards! The handwritten notes are exactly like topper notes, and AI doubt solver cleared all my concepts.',
    avatar: '👩‍🎓'
  },
  {
    name: 'Rahul Kumar',
    class: 'Class 11',
    location: 'Mumbai',
    rating: 5,
    text: 'Best platform for JEE preparation! PYQ analysis feature helped me identify important topics. Career guidance section is amazing!',
    avatar: '👨‍🎓'
  },
  {
    name: 'Anjali Patel',
    class: 'Class 10',
    location: 'Ahmedabad',
    rating: 5,
    text: 'As a rural student, I found the career guidance very helpful. It explained all options in simple Hindi-English mix. Highly recommended!',
    avatar: '👩‍🎓'
  },
  {
    name: 'Vikram Singh',
    class: 'Class 12',
    location: 'Pune',
    rating: 5,
    text: 'AI doubt solver is a game changer! Got instant solutions in Hinglish. The step-by-step explanations are crystal clear.',
    avatar: '👨‍🎓'
  }
]

export default function TestimonialSection() {
  const [currentIndex, setCurrentIndex] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentIndex((prev) => (prev + 1) % testimonials.length)
    }, 5000)
    return () => clearInterval(interval)
  }, [])

  return (
    <section className="py-20 bg-gradient-to-b from-white to-primary-50/30">
      <div className="container mx-auto px-4">
        <div className="text-center mb-16">
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-primary-100 text-primary-700 rounded-full text-sm font-semibold mb-4">
            <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
            Loved by Students
          </div>
          <h2 className="text-4xl md:text-5xl font-extrabold mb-4 bg-gradient-to-r from-primary-600 to-purple-600 bg-clip-text text-transparent">
            What Students Say
          </h2>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Real stories from students who are achieving their dreams
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-6">
          {testimonials.map((testimonial, index) => (
            <div
              key={index}
              className={`bg-white rounded-2xl p-6 shadow-lg hover:shadow-2xl transition-all duration-500 ${
                index === currentIndex ? 'scale-105 border-2 border-primary-200' : 'border border-gray-100'
              }`}
            >
              <div className="flex items-center gap-1 mb-4">
                {[...Array(testimonial.rating)].map((_, i) => (
                  <Star
                    key={i}
                    className="w-4 h-4 fill-yellow-400 text-yellow-400"
                  />
                ))}
              </div>
              <Quote className="w-8 h-8 text-primary-300 mb-3" />
              <p className="text-gray-700 mb-6 leading-relaxed italic">
                &ldquo;{testimonial.text}&rdquo;
              </p>
              <div className="flex items-center gap-3 pt-4 border-t border-gray-100">
                <div className="text-4xl">{testimonial.avatar}</div>
                <div>
                  <div className="font-bold text-gray-900">{testimonial.name}</div>
                  <div className="text-sm text-gray-500">
                    {testimonial.class} • {testimonial.location}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Indicator dots */}
        <div className="flex justify-center gap-2 mt-8">
          {testimonials.map((_, index) => (
            <button
              key={index}
              onClick={() => setCurrentIndex(index)}
              className={`w-2 h-2 rounded-full transition-all duration-300 ${
                index === currentIndex
                  ? 'bg-primary-600 w-8'
                  : 'bg-gray-300 hover:bg-gray-400'
              }`}
              aria-label={`Go to testimonial ${index + 1}`}
            />
          ))}
        </div>
      </div>
    </section>
  )
}
