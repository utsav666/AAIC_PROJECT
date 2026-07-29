import React, { useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useApp } from '../App'
import { assess } from '../api'

const STEPS = [
  'Reading your child\'s responses...',
  'Analysing phonemic patterns...',
  'Scoring each dimension...',
  'Classifying dyslexia indicators...',
  'Building personalised profile...',
]

export default function AnalyzingScreen() {
  const navigate = useNavigate()
  const { childData, responses, update } = useApp()

  useEffect(() => {
    let cancelled = false

    const run = async () => {
      try {
        const result = await assess({
          child_name: childData.child_name,
          child_age:  childData.child_age,
          responses,
        })
        if (!cancelled) {
          update({
            assessmentResult: result,
            learningLevel: result.overall_level || 1,
          })
          navigate('/results')
        }
      } catch {
        if (!cancelled) navigate('/results') // still navigate, show partial
      }
    }

    run()
    return () => { cancelled = true }
  }, [])

  return (
    <div
      className="min-h-screen flex flex-col items-center justify-center p-6"
      style={{ background: 'linear-gradient(140deg,#e0f7f4 0%,#ede9fe 55%,#fce8f3 100%)' }}
    >
      <div className="card p-12 w-full max-w-md text-center">
        {/* Animated brain */}
        <div className="text-7xl mb-6 animate-bounce">🧠</div>
        <h2 className="text-2xl font-bold text-gray-800 mb-2">AI is analysing responses…</h2>
        <p className="text-gray-400 text-sm mb-8">
          Our specialist AI is reviewing {childData?.child_name || 'the'}'s answers
        </p>

        {/* Spinning loader */}
        <div
          className="w-12 h-12 rounded-full border-4 border-gray-200 mx-auto mb-8"
          style={{
            borderTopColor: '#0d9488',
            animation: 'spin 1s linear infinite',
          }}
        />

        {/* Steps */}
        <div className="space-y-2 text-left">
          {STEPS.map((step, i) => (
            <AnalyzingStep key={step} step={step} delay={i * 0.8} />
          ))}
        </div>
      </div>

      <style>{`
        @keyframes spin { to { transform: rotate(360deg); } }
        @keyframes fadeInLeft { from { opacity:0; transform:translateX(-10px); } to { opacity:1; transform:none; } }
      `}</style>
    </div>
  )
}

function AnalyzingStep({ step, delay }) {
  const [done, setDone] = React.useState(false)
  useEffect(() => {
    const t = setTimeout(() => setDone(true), delay * 1000 + 600)
    return () => clearTimeout(t)
  }, [delay])

  return (
    <div
      className="flex items-center gap-3 text-sm"
      style={{ animation: `fadeInLeft 0.4s ease ${delay}s both` }}
    >
      <div
        className="w-5 h-5 rounded-full flex items-center justify-center text-xs flex-shrink-0 transition-all"
        style={{ background: done ? '#0d9488' : '#e5e7eb', color: done ? 'white' : '#94a3b8' }}
      >
        {done ? '✓' : '…'}
      </div>
      <span className={done ? 'text-gray-700' : 'text-gray-400'}>{step}</span>
    </div>
  )
}
