import Link from 'next/link'
import Image from 'next/image'
import { BookOpen, FileText, Brain, Briefcase, ArrowRight, Sparkles, Star, TrendingUp, Users, Award } from 'lucide-react'
import TestimonialSection from './components/TestimonialSection'
import FloatingActionButton from './components/FloatingActionButton'
import SmartHeader from './components/SmartHeader'
import AnimatedCounter from './components/AnimatedCounter'

export default function Home() {
  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-50 via-white to-gray-50">
      {/* Smart Header */}
      <SmartHeader />

      {/* Hero Section */}
      <section className="relative py-20 md:py-32 overflow-hidden bg-gradient-to-br from-gray-900 via-gray-800 to-black">
        <div className="absolute inset-0 opacity-5">
          <div className="absolute top-0 left-0 w-96 h-96 bg-white rounded-full blur-3xl"></div>
          <div className="absolute bottom-0 right-0 w-96 h-96 bg-white rounded-full blur-3xl"></div>
        </div>
        <div className="container mx-auto px-4 text-center relative z-10">
          <div className="inline-block mb-4 px-4 py-2 bg-white/10 backdrop-blur-sm text-white border border-white/20 rounded-full text-sm font-semibold">
            🎓 Trusted by 10,000+ Students
          </div>
          <h2 className="text-5xl md:text-7xl font-extrabold mb-6 text-white leading-tight">
            Excel in Your Studies
            <br />
            <span className="text-4xl md:text-6xl bg-gradient-to-r from-white via-gray-200 to-gray-400 bg-clip-text text-transparent">With AI-Powered Learning</span>
          </h2>
          <p className="text-xl md:text-2xl text-gray-300 mb-10 max-w-3xl mx-auto leading-relaxed">
            Get handwritten notes, PYQs, instant doubt solving, and career guidance
            <br />
            <span className="text-lg text-gray-400">All in one place, designed for Indian students</span>
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center items-center">
            <Link
              href="/register"
              className="group px-8 py-4 bg-white text-gray-900 rounded-lg font-bold text-lg hover:bg-gray-100 hover:shadow-2xl hover:scale-105 transition-all flex items-center gap-2 border-2 border-white"
            >
              Start Learning Free
              <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
            </Link>
            <Link
              href="/login"
              className="px-8 py-4 bg-transparent text-white rounded-lg font-bold text-lg border-2 border-white/30 hover:border-white hover:bg-white/10 transition-all backdrop-blur-sm"
            >
              Already a Student?
            </Link>
          </div>
          <div className="mt-12 flex flex-wrap justify-center gap-8 text-gray-300">
            <div className="flex items-center gap-2 bg-white/10 backdrop-blur-sm px-4 py-2 rounded-lg border border-white/20">
              <Star className="w-5 h-5 text-yellow-400 fill-yellow-400" />
              <span className="font-semibold">4.8/5 Rating</span>
            </div>
            <div className="flex items-center gap-2 bg-white/10 backdrop-blur-sm px-4 py-2 rounded-lg border border-white/20">
              <Users className="w-5 h-5 text-white" />
              <span className="font-semibold">10K+ Students</span>
            </div>
            <div className="flex items-center gap-2 bg-white/10 backdrop-blur-sm px-4 py-2 rounded-lg border border-white/20">
              <Award className="w-5 h-5 text-white" />
              <span className="font-semibold">100% Free</span>
            </div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-20 bg-white">
        <div className="container mx-auto px-4">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-extrabold mb-4 text-gray-900">
              Everything You Need to Succeed
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Powerful tools designed specifically for Indian students
            </p>
          </div>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <FeatureCard
              icon={<BookOpen className="w-8 h-8" />}
              title="📚 Handwritten Notes"
              description="Premium topper notes for Class 6-12, organized by chapter"
              color="from-gray-800 to-gray-900"
              delay="0"
            />
            <FeatureCard
              icon={<FileText className="w-8 h-8" />}
              title="📝 PYQs Collection"
              description="Complete PYQs for Boards, NEET, JEE Main & Advanced"
              color="from-gray-700 to-gray-800"
              delay="100"
            />
            <FeatureCard
              icon={<Brain className="w-8 h-8" />}
              title="🤖 AI Doubt Solver"
              description="Get instant, step-by-step solutions in Hindi + English"
              color="from-gray-900 to-black"
              delay="200"
            />
            <FeatureCard
              icon={<Briefcase className="w-8 h-8" />}
              title="💼 Career Guidance"
              description="AI-powered counseling for stream selection & career paths"
              color="from-gray-600 to-gray-700"
              delay="300"
            />
          </div>
        </div>
      </section>

      {/* Stats Section */}
      <section className="py-16 bg-gradient-to-r from-gray-100 to-gray-50 border-y-2 border-gray-200">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-3 gap-8 text-center">
            <div className="p-6 group hover:scale-105 transition-transform duration-300 bg-white rounded-xl border-2 border-gray-200 hover:border-gray-900 hover:shadow-xl">
              <AnimatedCounter
                end={10000}
                suffix="+"
                className="text-5xl font-extrabold text-gray-900 mb-2 group-hover:scale-110 transition-transform"
              />
              <div className="text-gray-600 font-semibold">Active Students</div>
            </div>
            <div className="p-6 group hover:scale-105 transition-transform duration-300 bg-white rounded-xl border-2 border-gray-200 hover:border-gray-900 hover:shadow-xl">
              <AnimatedCounter
                end={5000}
                suffix="+"
                className="text-5xl font-extrabold text-gray-900 mb-2 group-hover:scale-110 transition-transform"
              />
              <div className="text-gray-600 font-semibold">Study Materials</div>
            </div>
            <div className="p-6 group hover:scale-105 transition-transform duration-300 bg-white rounded-xl border-2 border-gray-200 hover:border-gray-900 hover:shadow-xl">
              <AnimatedCounter
                end={98}
                suffix="%"
                className="text-5xl font-extrabold text-gray-900 mb-2 group-hover:scale-110 transition-transform"
              />
              <div className="text-gray-600 font-semibold">Success Rate</div>
            </div>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <TestimonialSection />

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white relative overflow-hidden border-t-2 border-gray-700">
        <div className="absolute inset-0 opacity-5">
          <div className="absolute top-0 left-0 w-72 h-72 bg-white rounded-full blur-3xl"></div>
          <div className="absolute bottom-0 right-0 w-96 h-96 bg-white rounded-full blur-3xl"></div>
        </div>
        <div className="container mx-auto px-4 text-center relative z-10">
          <Sparkles className="w-16 h-16 mx-auto mb-6 text-white animate-pulse" />
          <h2 className="text-4xl md:text-6xl font-extrabold mb-6 text-white">
            Ready to Excel in Your Exams?
          </h2>
          <p className="text-xl md:text-2xl mb-10 max-w-2xl mx-auto text-gray-300">
            Join thousands of students who are already achieving their dreams with SchoolSharthi
          </p>
          <Link
            href="/register"
            className="inline-flex items-center gap-3 px-10 py-5 bg-white text-gray-900 rounded-lg font-bold text-lg hover:bg-gray-100 hover:shadow-2xl hover:scale-105 transition-all border-2 border-white"
          >
            Start Your Journey Now
            <ArrowRight className="w-6 h-6" />
          </Link>
          <p className="mt-6 text-gray-400">✨ 100% Free • No Credit Card Required</p>
        </div>
      </section>

      {/* Footer */}
      <footer className="bg-gray-900 text-white py-12">
        <div className="container mx-auto px-4">
          <div className="grid md:grid-cols-3 gap-8 mb-8">
            <div>
              <div className="flex items-center gap-2 mb-4">
                <Image 
                  src="/logo.png" 
                  alt="SchoolSharthi Logo" 
                  width={40} 
                  height={40} 
                  className="object-contain"
                />
                <div>
                  <h3 className="text-xl font-bold">SchoolSharthi</h3>
                  <p className="text-sm text-gray-400 font-medium">Har Student Ka Sacha Sarthi</p>
                </div>
              </div>
              <p className="text-gray-400">
                Empowering Indian students with quality education resources and AI-powered learning tools.
              </p>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Quick Links</h4>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="/notes" className="hover:text-white transition">Notes</Link></li>
                <li><Link href="/pyqs" className="hover:text-white transition">PYQs</Link></li>
                <li><Link href="/ai-doubt" className="hover:text-white transition">AI Doubt Solver</Link></li>
                <li><Link href="/career" className="hover:text-white transition">Career Guidance</Link></li>
              </ul>
            </div>
            <div>
              <h4 className="font-semibold mb-4">Support</h4>
              <ul className="space-y-2 text-gray-400">
                <li><Link href="/login" className="hover:text-white transition">Login</Link></li>
                <li><Link href="/register" className="hover:text-white transition">Sign Up</Link></li>
              </ul>
            </div>
          </div>
          <div className="border-t border-gray-800 pt-8 text-center text-gray-400">
            <p>&copy; 2024 SchoolSharthi. All rights reserved. Made with ❤️ for Indian Students</p>
          </div>
        </div>
      </footer>

      {/* Floating Action Button */}
      <FloatingActionButton />
    </main>
  )
}

function FeatureCard({ 
  icon, 
  title, 
  description, 
  color, 
  delay 
}: { 
  icon: React.ReactNode
  title: string
  description: string
  color: string
  delay: string
}) {
  return (
    <div 
      className="group bg-white p-8 rounded-2xl shadow-lg hover:shadow-2xl transition-all duration-300 hover:-translate-y-2 border-2 border-gray-200 hover:border-gray-900"
      style={{ animationDelay: `${delay}ms` }}
    >
      <div className={`w-16 h-16 rounded-xl bg-gradient-to-br ${color} flex items-center justify-center mb-6 group-hover:scale-110 group-hover:rotate-3 transition-all text-white shadow-xl`}>
        {icon}
      </div>
      <h3 className="text-xl font-bold mb-3 text-gray-900 group-hover:text-gray-700 transition-colors">{title}</h3>
      <p className="text-gray-600 leading-relaxed">{description}</p>
      <div className="mt-4 h-1 w-0 bg-gray-900 group-hover:w-full transition-all duration-300 rounded-full"></div>
    </div>
  )
}
