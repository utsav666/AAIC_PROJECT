import React from 'react'
import { useNavigate } from 'react-router-dom'
import { useApp } from '../App'
import { Sidebar, StepperBar } from '../components/Layout'

// ── Semicircle Gauge (matching mockup: 4 color segments) ─────────────────────
function RiskGauge({ level = 2 }) {
  const cx = 120, cy = 110, r = 80, sw = 20
  const labels = ['Low', 'Mild', 'Moderate', 'High']
  const colors = ['#10b981', '#eab308', '#f97316', '#ec4899']
  const sublabels = ['Minimal support', 'Some support', 'Targeted support', 'Intensive support']

  // Draw 4 equal arc segments (left to right)
  const arcs = colors.map((color, i) => {
    const startAngle = Math.PI - (i * (Math.PI / 4))
    const endAngle   = Math.PI - ((i + 1) * (Math.PI / 4))
    const x1 = cx + r * Math.cos(startAngle)
    const y1 = cy - r * Math.sin(startAngle)
    const x2 = cx + r * Math.cos(endAngle)
    const y2 = cy - r * Math.sin(endAngle)
    return { d: `M ${x1.toFixed(1)} ${y1.toFixed(1)} A ${r} ${r} 0 0 0 ${x2.toFixed(1)} ${y2.toFixed(1)}`, color }
  })

  // Pointer position
  const pct = Math.min((level - 0.5) / 4, 0.99)
  const pointerAngle = Math.PI * (1 - pct)
  const px = cx + (r + 8) * Math.cos(pointerAngle)
  const py = cy - (r + 8) * Math.sin(pointerAngle)

  const severityText = level <= 1 ? 'Low' : level <= 2 ? 'Mild' : level <= 3 ? 'Moderate' : 'High'

  return (
    <div className="flex flex-col items-center">
      <svg viewBox="0 0 240 135" style={{ width: '100%', maxWidth: 260 }}>
        {arcs.map((a, i) => (
          <path key={i} d={a.d} fill="none" stroke={a.color} strokeWidth={sw} strokeLinecap="round" />
        ))}
        <circle cx={px} cy={py} r={5} fill="#1e293b" stroke="white" strokeWidth={2} />
        <text x={cx} y={cy - 2} textAnchor="middle" fill="#1e293b" fontSize="26" fontWeight="700" fontFamily="Lexend, sans-serif">
          {severityText}
        </text>
        <text x={cx} y={cy + 16} textAnchor="middle" fill="#94a3b8" fontSize="11" fontFamily="Lexend, sans-serif">
          Risk Level
        </text>
      </svg>
      <div className="flex items-center gap-3 mt-1 flex-wrap justify-center">
        {labels.map((l, i) => (
          <div key={l} className="flex items-center gap-1">
            <div className="w-2 h-2 rounded-full" style={{ background: colors[i] }} />
            <span className="text-[10px] text-gray-500 font-medium">{l}</span>
          </div>
        ))}
      </div>
    </div>
  )
}

// ── Domain Bar ───────────────────────────────────────────────────────────────
function DomainBar({ icon, label, score, max = 100 }) {
  const pct = (score / max) * 100
  const isStrong = score >= 75
  const color = isStrong ? '#0d9488' : '#f59e0b'
  const statusLabel = isStrong ? 'Strong' : 'Developing'

  return (
    <div className="flex items-center gap-3 py-2.5 border-b border-gray-50 last:border-0">
      <div className="w-7 h-7 rounded-lg flex items-center justify-center text-sm flex-shrink-0" style={{ background: color + '15' }}>
        {icon}
      </div>
      <div className="w-36 text-xs font-medium text-gray-700 flex-shrink-0">{label}</div>
      <div className="flex-1 h-2.5 rounded-full bg-gray-100 overflow-hidden">
        <div className="h-full rounded-full" style={{ width: `${pct}%`, background: color }} />
      </div>
      <div className="text-xs font-semibold text-gray-600 w-12 text-right">{score}/100</div>
      <div className="text-xs font-bold w-20 text-right" style={{ color }}>{statusLabel}</div>
    </div>
  )
}

// ── Main ─────────────────────────────────────────────────────────────────────
const MOCK = {
  overall_level: 2,
  severity: 'mild',
  summary: 'shows some indicators of dyslexia. Early support can make a big difference!',
  dimensions: {
    letter_knowledge: { score: 85 }, phonological_awareness: { score: 62 },
    word_reading: { score: 58 }, reading_comprehension: { score: 60 },
    visual_processing: { score: 78 }, speech_listening: { score: 82 },
  },
}

const DOMAINS = [
  { key: 'letter_knowledge',       icon: '🔤', label: 'Letter Knowledge' },
  { key: 'phonological_awareness', icon: '🔊', label: 'Phonological Awareness' },
  { key: 'word_reading',           icon: '📖', label: 'Word Reading' },
  { key: 'reading_comprehension',  icon: '💬', label: 'Reading Comprehension' },
  { key: 'visual_processing',      icon: '👁️', label: 'Visual Processing' },
  { key: 'speech_listening',       icon: '🎙️', label: 'Speech & Listening' },
]

export default function ResultsScreen() {
  const navigate = useNavigate()
  const { childData, assessmentResult, update } = useApp()
  const result = assessmentResult || MOCK
  const level  = result.overall_level || 2
  const name   = childData?.child_name || 'Nathaniel'
  const dims   = result.dimensions || MOCK.dimensions

  const getScore = (key) => {
    const d = dims[key]
    if (!d) return 60
    return d.score > 5 ? d.score : d.score * 20
  }

  const startLearning = () => {
    update({ learningLevel: level, currentModuleIndex: 0, moduleProgress: {} })
    navigate('/dashboard')
  }

  return (
    <div className="flex min-h-screen" style={{ background: '#f8fafc' }}>
      <Sidebar active="Screening" />

      <main className="flex-1 overflow-y-auto p-6 pb-10">
        <StepperBar current={5} />

        {/* Header */}
        <div className="flex items-start justify-between mb-5">
          <div>
            <h1 className="text-2xl font-bold text-gray-800">AI Screening Results</h1>
            <p className="text-xs text-gray-400 mt-1">
              Completed on {new Date().toLocaleDateString('en-SG', { day: 'numeric', month: 'short', year: 'numeric' })} · Screening ID: NLK-{Date.now().toString().slice(-6)}
            </p>
          </div>
          <button onClick={() => window.print()} className="flex items-center gap-2 px-4 py-2 rounded-xl border border-gray-200 text-xs font-semibold text-gray-700 hover:bg-gray-50">
            📄 Download Report
          </button>
        </div>

        {/* Congrats banner */}
        <div className="rounded-2xl p-5 mb-5 flex items-center gap-4" style={{ background: 'linear-gradient(135deg, #e6f7f5, #faf5ff)' }}>
          <span className="text-4xl">🏆</span>
          <div className="flex-1">
            <div className="text-lg font-bold" style={{ color: '#0d9488' }}>Great job, {name}!</div>
            <div className="text-sm text-gray-500">You have completed the AI screening. Here's a summary of your child's learning profile.</div>
          </div>
          <span className="text-4xl opacity-50">🧠</span>
        </div>

        {/* Two cards: Gauge + Domains */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-5 mb-5">
          <div className="bg-white rounded-2xl p-6 border border-gray-100">
            <div className="flex items-center gap-2 mb-3">
              <h2 className="font-bold text-gray-800 text-sm">Overall Dyslexia Risk</h2>
              <span className="text-gray-300 text-xs cursor-help">ⓘ</span>
            </div>
            <RiskGauge level={level} />
            <p className="text-xs text-gray-500 text-center mt-3 leading-relaxed">
              {name} {result.summary || MOCK.summary}
            </p>
          </div>

          <div className="bg-white rounded-2xl p-6 border border-gray-100">
            <div className="flex items-center gap-2 mb-3">
              <h2 className="font-bold text-gray-800 text-sm">Domain Performance</h2>
              <span className="text-gray-300 text-xs cursor-help">ⓘ</span>
            </div>
            {DOMAINS.map(({ key, icon, label }) => (
              <DomainBar key={key} icon={icon} label={label} score={getScore(key)} />
            ))}
          </div>
        </div>

        {/* Recommended Next Step */}
        <div className="rounded-2xl p-5 mb-5 flex items-center gap-4 bg-purple-50/60 border border-purple-100">
          <div className="w-11 h-11 rounded-xl bg-purple-100 flex items-center justify-center text-xl flex-shrink-0">✅</div>
          <div className="flex-1">
            <div className="font-bold text-purple-700 text-sm">Recommended Next Step</div>
            <div className="text-xs text-gray-500">Start {name}'s personalized learning path based on unique strengths and needs.</div>
          </div>
          <button onClick={startLearning} className="px-5 py-2.5 rounded-xl text-xs font-bold text-white" style={{ background: '#1e293b' }}>
            View Learning Path →
          </button>
          <button className="px-4 py-2.5 rounded-xl text-xs font-semibold border border-gray-200 text-gray-600 hover:bg-gray-50">
            Share Results ↗
          </button>
        </div>

        {/* Tips for Parents */}
        <h3 className="font-bold text-purple-700 text-sm mb-3">Tips for Parents</h3>
        <div className="grid grid-cols-4 gap-3 mb-6">
          {[
            { icon: '❤️', bg: '#fef2f2', title: 'Celebrate small wins', desc: 'Encourage effort and progress every day.' },
            { icon: '⏰', bg: '#f0fdf9', title: 'Practice regularly', desc: '10–15 minutes daily makes a big difference.' },
            { icon: '📚', bg: '#eff6ff', title: 'Read together', desc: 'Make reading fun and stress-free.' },
            { icon: '💬', bg: '#f5f3ff', title: "You're not alone", desc: "We're here to support you every step." },
          ].map((t) => (
            <div key={t.title} className="flex items-start gap-2.5 p-3.5 bg-white rounded-2xl border border-gray-100">
              <div className="w-8 h-8 rounded-full flex items-center justify-center text-sm flex-shrink-0" style={{ background: t.bg }}>{t.icon}</div>
              <div>
                <div className="text-xs font-bold text-gray-700">{t.title}</div>
                <div className="text-[11px] text-gray-400 mt-0.5 leading-relaxed">{t.desc}</div>
              </div>
            </div>
          ))}
        </div>

        {/* Footer */}
        <div className="text-center text-xs text-gray-400 py-3 border-t border-gray-100">
          🔒 All results are confidential and secure. This is not a medical diagnosis.
        </div>
      </main>
    </div>
  )
}
