import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useApp } from '../App'
import { getQuestions } from '../api'

const CATEGORIES = [
  { icon: '🔊', label: 'Phonemic Awareness',  desc: 'Identifying and manipulating sounds in words' },
  { icon: '🔤', label: 'Letter Recognition',   desc: 'Correctly identifying letters (b/d, p/q)' },
  { icon: '📖', label: 'Reading & Spelling',   desc: 'Phonetic decoding and spelling patterns' },
  { icon: '🧠', label: 'Comprehension',        desc: 'Understanding meaning from text' },
  { icon: '👁️', label: 'Visual Processing',    desc: 'How the child perceives letter/word arrangements' },
]

export default function ScreeningIntroScreen() {
  const navigate = useNavigate()
  const { childData, update } = useApp()
  const [loading, setLoading] = useState(false)
  const [error, setError]     = useState('')

  const age = childData?.child_age || 7

  const startScreening = async () => {
    setLoading(true)
    setError('')
    try {
      const data = await getQuestions(age)
      update({ questions: data.questions, responses: [], currentQuestion: 0 })
      navigate('/assessment')
    } catch (err) {
      setError('Could not load assessment questions. Is the backend running?')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div
      className="min-h-screen flex flex-col items-center justify-center p-6"
      style={{ background: 'linear-gradient(140deg,#e0f7f4 0%,#ede9fe 55%,#fce8f3 100%)' }}
    >
      <div className="card p-10 w-full max-w-xl">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="text-5xl mb-4">🤖</div>
          <h1 className="text-3xl font-bold text-gray-800 mb-2">
            Let's understand {childData?.child_name || 'your child'} better
          </h1>
          <p className="text-gray-400 text-sm leading-relaxed">
            Our AI will ask a series of questions to understand their learning style
            and identify any areas where they might need extra support.
          </p>
        </div>

        {/* Categories */}
        <div className="space-y-3 mb-8">
          {CATEGORIES.map((c) => (
            <div
              key={c.label}
              className="flex items-center gap-4 p-4 rounded-2xl bg-gray-50 border border-gray-100"
            >
              <div
                className="w-10 h-10 rounded-xl flex items-center justify-center text-xl flex-shrink-0"
                style={{ background: 'linear-gradient(135deg,#e0f7f4,#ede9fe)' }}
              >
                {c.icon}
              </div>
              <div>
                <div className="font-semibold text-gray-800 text-sm">{c.label}</div>
                <div className="text-xs text-gray-400 mt-0.5">{c.desc}</div>
              </div>
              <div className="ml-auto text-teal-500 text-lg">✓</div>
            </div>
          ))}
        </div>

        {/* Time info */}
        <div className="flex items-center justify-center gap-2 text-sm text-gray-400 mb-6">
          <span>⏱️</span>
          <span>Approx. 5–10 minutes &nbsp;|&nbsp; Suitable for ages 5–16</span>
        </div>

        {error && (
          <div className="mb-4 p-3 rounded-xl bg-red-50 border border-red-200 text-sm text-red-600 text-center">
            {error}
          </div>
        )}

        {/* CTA */}
        <button
          onClick={startScreening}
          disabled={loading}
          className="btn-gradient w-full py-4 rounded-xl text-base"
        >
          {loading ? 'Loading questions...' : 'Start AI Screening →'}
        </button>

        <p className="text-center text-sm text-gray-400 mt-4">
          <button
            type="button"
            onClick={() => navigate('/dashboard')}
            className="hover:underline"
            style={{ color: '#0d9488' }}
          >
            I'll do this later
          </button>
        </p>
      </div>
    </div>
  )
}
