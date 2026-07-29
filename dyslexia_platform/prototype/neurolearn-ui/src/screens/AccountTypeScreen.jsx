import React from 'react'
import { useNavigate } from 'react-router-dom'
import { useApp } from '../App'
import { StepIndicator, FeatureBar, Footer } from '../components/Shared'

const ROLES = [
  { key: 'parent',     icon: '🏠', label: 'Parent / Guardian',      desc: "Support my child's learning journey",      color: '#0d9488', bg: '#f0fdf9', border: '#99f6e4' },
  { key: 'teacher',    icon: '📚', label: 'Teacher',                 desc: 'Manage my classroom and support students', color: '#7c3aed', bg: '#faf5ff', border: '#ddd6fe' },
  { key: 'student',    icon: '🎒', label: 'Student',                 desc: 'I want to learn, practise and improve',    color: '#d97706', bg: '#fffbeb', border: '#fde68a' },
  { key: 'specialist', icon: '🩺', label: 'Specialist / Therapist',  desc: 'Assess and support learners',              color: '#db2777', bg: '#fdf2f8', border: '#fbcfe8' },
]

export default function AccountTypeScreen() {
  const navigate = useNavigate()
  const { update } = useApp()

  const select = (roleKey) => { update({ userRole: roleKey }); navigate('/register') }

  return (
    <div className="min-h-screen flex flex-col" style={{ background: 'linear-gradient(160deg, #e8faf8 0%, #ede9fe 50%, #fce8f3 100%)' }}>
      <div className="flex flex-1">
        {/* ── Left Brand Panel ─────────────────────────────────── */}
        <div className="hidden lg:flex w-[380px] flex-shrink-0 flex-col items-center px-10 pt-14 pb-8">
          <div className="text-6xl mb-2">🧠</div>
          <div className="text-3xl font-extrabold" style={{ color: '#0d9488' }}>NeuroLearn</div>
          <div className="text-xs font-bold tracking-[0.3em] mt-1" style={{ color: '#0d9488' }}>KIDS</div>

          <div className="mt-8 text-left w-full">
            <h2 className="text-2xl font-bold text-gray-800 leading-snug mb-3">
              Personalized<br/>Learning for<br/>Every Unique Mind
            </h2>
            <div className="w-10 h-1 rounded bg-pink-300 mb-4" />
            <p className="text-sm text-gray-500 leading-relaxed">
              Help your child build confidence and develop strong reading skills with AI-powered personalized learning.
            </p>
          </div>

          <div className="mt-auto flex items-end justify-center w-full">
            <div className="text-7xl">👦🏻👧🏻</div>
          </div>

          {/* Security badge */}
          <div className="flex items-center gap-2 mt-6 w-full">
            <div className="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center text-sm">🔒</div>
            <div>
              <div className="text-xs font-bold text-gray-700">Your data is safe with us</div>
              <div className="text-[11px] text-gray-400">We use enterprise-grade security to protect your family's information.</div>
            </div>
          </div>
        </div>

        {/* ── Right Card ──────────────────────────────────────── */}
        <div className="flex-1 flex flex-col items-center justify-center p-8">
          <div className="bg-white rounded-3xl shadow-xl p-10 w-full max-w-lg">
            {/* Step indicator */}
            <StepIndicator steps={['Sign In', 'Choose Account Type', 'Create Account']} current={1} />

            <h1 className="text-3xl font-bold text-gray-800 text-center mb-2">Who are you? 👋</h1>
            <p className="text-gray-400 text-sm text-center mb-8">Select the option that best describes you</p>

            {/* Role cards 2x2 */}
            <div className="grid grid-cols-2 gap-4 mb-6">
              {ROLES.map(r => (
                <button
                  key={r.key}
                  onClick={() => select(r.key)}
                  className="p-5 rounded-2xl border-2 text-left transition-all hover:shadow-lg hover:-translate-y-0.5"
                  style={{ background: r.bg, borderColor: r.border }}
                >
                  <div className="text-3xl mb-3">{r.icon}</div>
                  <div className="font-bold text-gray-800 text-sm mb-1">{r.label}</div>
                  <div className="text-xs text-gray-400 leading-relaxed">{r.desc}</div>
                  <div className="mt-3 text-xs font-bold" style={{ color: r.color }}>Select →</div>
                </button>
              ))}
            </div>

            {/* Security note */}
            <div className="flex items-center justify-center gap-2 text-xs text-gray-400 mb-3">
              <span>🔒</span> Your data is safe with us — PDPA compliant
            </div>
            <p className="text-center text-xs text-gray-400">
              Not sure which to choose?{' '}
              <a href="#" className="hover:underline" style={{ color: '#0d9488' }}>Learn more</a>
            </p>
          </div>
        </div>
      </div>

      {/* Feature bar + Footer */}
      <div className="bg-white border-t border-gray-100 px-10 py-6">
        <div className="max-w-5xl mx-auto grid grid-cols-4 gap-6">
          {[
            { icon: '🧠', bg: '#ede9fe', title: 'AI-Powered Assessment', desc: 'Identify strengths and learning needs.' },
            { icon: '📚', bg: '#e6f7f5', title: 'Adaptive Learning', desc: 'Personalized lessons that grow with your child.' },
            { icon: '📈', bg: '#fce8f3', title: 'Track Progress', desc: 'Real-time insights for parents and educators.' },
            { icon: '🛡️', bg: '#e6f7f5', title: 'Trusted by Families', desc: 'Designed with experts. Loved by families.' },
          ].map(f => (
            <div key={f.title} className="flex items-center gap-3">
              <div className="w-10 h-10 rounded-full flex items-center justify-center text-lg flex-shrink-0" style={{ background: f.bg }}>{f.icon}</div>
              <div>
                <div className="text-xs font-bold text-gray-800">{f.title}</div>
                <div className="text-[11px] text-gray-400">{f.desc}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
      <div className="flex items-center justify-between px-10 py-4 text-xs text-gray-400" style={{ background: 'linear-gradient(90deg, #e8faf8, #ede9fe)' }}>
        <span>© 2026 NeuroLearn Kids. All rights reserved.</span>
        <div className="flex gap-4">
          <a href="#" className="hover:text-teal-600">Privacy Policy</a><span>|</span>
          <a href="#" className="hover:text-teal-600">Terms of Use</a><span>|</span>
          <a href="#" className="hover:text-teal-600">Help Center</a>
        </div>
      </div>
    </div>
  )
}
