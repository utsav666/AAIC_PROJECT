import React, { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom'
import { useApp } from '../App'

export default function AssessmentScreen() {
  const navigate = useNavigate()
  const { childData, questions, responses, currentQuestion, update } = useApp()
  const [answer, setAnswer]   = useState('')
  const [hint, setHint]       = useState(false)
  const startTime             = useRef(Date.now())

  const total = questions.length
  const idx   = currentQuestion
  const q     = questions[idx]

  // Reset answer when question changes
  useEffect(() => {
    setAnswer('')
    setHint(false)
    startTime.current = Date.now()
  }, [idx])

  // Guard: no questions loaded
  if (!q) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="card p-10 text-center">
          <p className="text-gray-400 mb-4">No questions loaded.</p>
          <button className="btn-gradient px-6 py-3 rounded-xl text-sm" onClick={() => navigate('/screening-intro')}>
            ← Back
          </button>
        </div>
      </div>
    )
  }

  const dimColors = {
    phonemic_awareness: '#0d9488',
    letter_recognition: '#7c3aed',
    reading_spelling:   '#d97706',
    comprehension:      '#2563eb',
    visual_processing:  '#db2777',
  }
  const dimColor = dimColors[q.dimension] || '#0d9488'
  const pct = Math.round(((idx) / total) * 100)

  const handleNext = () => {
    if (!answer) return
    const elapsed = Math.round((Date.now() - startTime.current) / 1000)
    const newResponses = [
      ...responses,
      {
        question: q.question,
        expected: q.expected,
        answer,
        dimension: q.dimension,
        time_seconds: elapsed,
      },
    ]
    if (idx + 1 >= total) {
      update({ responses: newResponses, currentQuestion: 0 })
      navigate('/analyzing')
    } else {
      update({ responses: newResponses, currentQuestion: idx + 1 })
    }
  }

  return (
    <div
      className="min-h-screen flex flex-col items-center justify-center p-6"
      style={{ background: 'linear-gradient(140deg,#e0f7f4 0%,#ede9fe 55%,#fce8f3 100%)' }}
    >
      <div className="card p-8 w-full max-w-xl">
        {/* Header */}
        <div className="flex items-center justify-between mb-5">
          <div>
            <h2 className="text-lg font-bold text-gray-800">
              AI Screening — {childData?.child_name || 'Assessment'}
            </h2>
            <p className="text-xs text-gray-400 mt-0.5">Question {idx + 1} of {total}</p>
          </div>
          <div
            className="w-10 h-10 rounded-full flex items-center justify-center text-white text-sm font-bold"
            style={{ background: dimColor }}
          >
            {idx + 1}
          </div>
        </div>

        {/* Progress bar */}
        <div className="h-2 rounded-full bg-gray-100 mb-6 overflow-hidden">
          <div
            className="h-full rounded-full transition-all duration-500"
            style={{ width: `${pct}%`, background: `linear-gradient(90deg, ${dimColor}, #7c3aed)` }}
          />
        </div>

        {/* Dimension badge */}
        <div className="mb-4">
          <span
            className="inline-block text-xs font-bold px-3 py-1 rounded-full"
            style={{ background: dimColor + '18', color: dimColor }}
          >
            {q.dimension.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())}
          </span>
        </div>

        {/* Question */}
        <div className="p-5 rounded-2xl bg-gray-50 border border-gray-100 mb-6">
          <p className="text-gray-800 font-semibold text-base leading-relaxed">{q.question}</p>
        </div>

        {/* Answer input */}
        {q.type === 'multiple_choice' ? (
          <div className="space-y-3 mb-6">
            {q.options?.map((opt) => (
              <label
                key={opt}
                className="flex items-center gap-3 p-4 rounded-xl border-2 cursor-pointer transition-all"
                style={{
                  borderColor: answer === opt ? dimColor : '#e5e7eb',
                  background: answer === opt ? dimColor + '10' : 'white',
                }}
              >
                <div
                  className="w-5 h-5 rounded-full border-2 flex-shrink-0"
                  style={{
                    borderColor: answer === opt ? dimColor : '#d1d5db',
                    background: answer === opt ? dimColor : 'white',
                  }}
                />
                <input
                  type="radio"
                  name="answer"
                  value={opt}
                  checked={answer === opt}
                  onChange={() => setAnswer(opt)}
                  className="hidden"
                />
                <span className="text-sm font-medium text-gray-700">{opt}</span>
              </label>
            ))}
          </div>
        ) : (
          <div className="mb-6">
            <input
              type="text"
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleNext()}
              placeholder="Type your answer here..."
              className="w-full px-4 py-4 border-2 rounded-xl text-sm focus:outline-none transition-all"
              style={{ borderColor: answer ? dimColor : '#e5e7eb' }}
              autoFocus
            />
          </div>
        )}

        {/* Hint */}
        <div className="mb-6">
          <button
            type="button"
            onClick={() => setHint(!hint)}
            className="flex items-center gap-2 text-xs font-medium text-gray-400 hover:text-gray-600"
          >
            <span>💡</span>
            <span>{hint ? 'Hide hint' : 'Need a hint?'}</span>
          </button>
          {hint && (
            <div className="mt-2 p-3 rounded-xl bg-amber-50 border border-amber-100 text-sm text-amber-700">
              {q.hint}
            </div>
          )}
        </div>

        {/* Next button */}
        <button
          onClick={handleNext}
          disabled={!answer}
          className="btn-gradient w-full py-4 rounded-xl text-sm disabled:opacity-40 disabled:cursor-not-allowed"
        >
          {idx + 1 >= total ? 'Submit Answers' : 'Next Question →'}
        </button>
      </div>

      {/* Progress dots */}
      <div className="flex gap-1.5 mt-4">
        {questions.map((_, i) => (
          <div
            key={i}
            className="rounded-full transition-all"
            style={{
              width: i === idx ? 20 : 8,
              height: 8,
              background: i < idx ? '#0d9488' : i === idx ? '#7c3aed' : '#e2e8f0',
            }}
          />
        ))}
      </div>
    </div>
  )
}
