import React, { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useApp } from '../App'
import { Sidebar } from '../components/Layout'
import { getModules } from '../api'

const SKILL_COLORS = ['#0d9488','#f59e0b','#7c3aed','#ef4444','#2563eb','#ec4899']
const MODULE_ICONS = ['🔤','📖','💬','👂','🧩','🎮']
const MODULE_SUBTITLES = ['Letters & Sounds','Decode & Read Words','Learn New Words','Listen & Understand','Understand & Answer','Play & Learn']

// ── Learning Path Journey (matching mockup road with level nodes) ─────────────
function LearningPathBanner({ level, levelData, completedPct }) {
  return (
    <div className="rounded-3xl p-6 mb-6 text-white relative overflow-hidden" style={{ background: 'linear-gradient(135deg, #0d9488 0%, #7c3aed 100%)' }}>
      {/* Cloud decorations */}
      <div className="absolute top-2 right-20 text-white/10 text-6xl">☁️</div>
      <div className="absolute top-8 right-60 text-white/10 text-4xl">☁️</div>

      <div className="flex items-start justify-between mb-4 relative z-10">
        <div className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-2xl bg-white/20 flex items-center justify-center text-2xl">🎯</div>
          <div>
            <div className="text-xs font-bold opacity-60 uppercase tracking-wider">Your Learning Path</div>
            <div className="text-xl font-bold">{levelData?.name || 'Build Strong Readers'}</div>
            <div className="text-sm opacity-70 mt-0.5">{levelData?.description || 'Personalized for your strengths and areas to improve.'}</div>
          </div>
        </div>
      </div>

      {/* Progress bar */}
      <div className="relative z-10 mb-3">
        <div className="h-2 rounded-full bg-white/20 overflow-hidden mb-1">
          <div className="h-full rounded-full bg-white transition-all" style={{ width: `${completedPct}%` }} />
        </div>
        <div className="flex justify-between text-xs opacity-70">
          <span>Level {level} · Early Reader</span>
          <span>{completedPct}% Complete</span>
        </div>
      </div>

      {/* Level road/path */}
      <div className="flex items-center gap-0 mt-4 relative z-10">
        {[1, 2, 3, 4, 5].map((l, i) => {
          const done   = l < level
          const curr   = l === level
          const locked = l > level
          return (
            <React.Fragment key={l}>
              {i > 0 && (
                <div className="flex-1 h-0.5 relative">
                  <div className="absolute inset-0" style={{ background: done ? 'rgba(255,255,255,0.8)' : 'rgba(255,255,255,0.2)' }} />
                  {/* Road dots */}
                  <div className="absolute inset-0 flex items-center justify-around">
                    {[...Array(3)].map((_, di) => (
                      <div key={di} className="w-1 h-1 rounded-full" style={{ background: done ? 'rgba(255,255,255,0.5)' : 'rgba(255,255,255,0.1)' }} />
                    ))}
                  </div>
                </div>
              )}
              <div className="flex flex-col items-center gap-1">
                <div
                  className="w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0 shadow-md"
                  style={{
                    background: done ? 'white' : curr ? 'white' : 'rgba(255,255,255,0.15)',
                    color: done ? '#10b981' : curr ? '#7c3aed' : 'rgba(255,255,255,0.4)',
                    border: curr ? '3px solid rgba(255,255,255,0.6)' : 'none',
                  }}
                >
                  {done ? '✓' : locked ? '🔒' : l}
                </div>
                <span className="text-[10px] opacity-60">Level {l}</span>
              </div>
            </React.Fragment>
          )
        })}
      </div>
    </div>
  )
}

// ── Module Card (matching mockup with colored left border) ────────────────────
function ModuleCard({ title, subtitle, idx, pct, color, onClick, status }) {
  const icon = MODULE_ICONS[idx % MODULE_ICONS.length]
  return (
    <button
      onClick={onClick}
      className="bg-white rounded-2xl p-4 border border-gray-100 text-left hover:shadow-lg hover:-translate-y-0.5 transition-all flex items-center gap-4"
      style={{ borderLeft: `4px solid ${color}` }}
    >
      <div className="w-11 h-11 rounded-xl flex items-center justify-center text-xl flex-shrink-0" style={{ background: color + '15' }}>
        {icon}
      </div>
      <div className="flex-1 min-w-0">
        <div className="text-sm font-bold text-gray-800">{title}</div>
        <div className="text-xs text-gray-400 mt-0.5">{subtitle}</div>
        <div className="mt-2 flex items-center gap-2">
          <div className="flex-1 h-1.5 rounded-full bg-gray-100 overflow-hidden">
            <div className="h-full rounded-full" style={{ width: `${pct}%`, background: color }} />
          </div>
          <span className="text-xs text-gray-400">{pct}% Complete</span>
        </div>
      </div>
      <div
        className="w-8 h-8 rounded-full flex items-center justify-center text-sm flex-shrink-0"
        style={{ background: color, color: 'white' }}
      >
        →
      </div>
    </button>
  )
}

// ── Right sidebar panels ─────────────────────────────────────────────────────
function RightSidebar({ completedModules, totalModules, level }) {
  const levelPct = totalModules > 0 ? Math.round((completedModules / totalModules) * 100) : 0
  return (
    <aside className="w-72 flex-shrink-0 border-l border-gray-100 bg-white p-5 space-y-4 overflow-y-auto">
      {/* Streak */}
      <div className="p-4 rounded-2xl bg-amber-50 border border-amber-100">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <span className="text-xl">🔥</span>
            <div>
              <div className="font-bold text-gray-800 text-sm">Learning Streak</div>
            </div>
          </div>
          <div className="text-2xl font-extrabold text-amber-500">7</div>
        </div>
        <div className="text-xs text-gray-400 mb-2">days · Great job! Keep it up!</div>
        <div className="flex gap-1.5">
          {['M','T','W','T','F','S','S'].map((d, i) => (
            <div key={i} className="flex-1 flex flex-col items-center gap-1">
              <div
                className="w-full aspect-square rounded-lg flex items-center justify-center text-[10px]"
                style={{ background: i < 6 ? '#10b981' : '#e5e7eb', color: i < 6 ? 'white' : '#94a3b8' }}
              >
                {i < 6 ? '✓' : ''}
              </div>
              <span className="text-[10px] text-gray-400">{d}</span>
            </div>
          ))}
        </div>
      </div>

      {/* Weekly Progress */}
      <div className="p-4 rounded-2xl border border-gray-100">
        <div className="flex items-center justify-between mb-2">
          <span className="font-bold text-gray-800 text-sm">Weekly Progress</span>
          <span className="text-xs text-gray-400">This Week</span>
        </div>
        <div className="flex flex-col items-center">
          <WeeklyGauge pct={0.75} />
          <div className="text-xs text-gray-500 mt-2 text-center leading-relaxed">
            ⭐ You're making great progress! Keep learning a little every day.
          </div>
        </div>
      </div>

      {/* Next Milestone */}
      <div className="p-4 rounded-2xl border border-gray-100">
        <div className="font-bold text-gray-800 text-sm mb-2">Next Milestone</div>
        <div className="flex items-center gap-3 mb-2">
          <span className="text-3xl">🏆</span>
          <div>
            <div className="text-sm font-bold text-gray-800">Super Reader</div>
            <div className="text-xs text-gray-400">Complete 10 lessons with 80% or higher</div>
          </div>
        </div>
        <div className="h-2 rounded-full bg-gray-100 overflow-hidden">
          <div className="h-full rounded-full" style={{ width: `${levelPct}%`, background: '#0d9488' }} />
        </div>
        <div className="text-xs text-gray-400 mt-1 text-right">{completedModules} / {totalModules}</div>
      </div>
    </aside>
  )
}

function WeeklyGauge({ pct = 0.75 }) {
  const cx = 60, cy = 55, r = 40, sw = 12
  const angle = Math.PI * (1 - Math.min(pct, 0.99))
  const ex = cx + r * Math.cos(angle)
  const ey = cy - r * Math.sin(angle)
  const topX = cx, topY = cy - r
  const bgPath = `M ${cx - r} ${cy} A ${r} ${r} 0 0 0 ${topX} ${topY} A ${r} ${r} 0 0 0 ${cx + r} ${cy}`
  const fillPath = `M ${cx - r} ${cy} A ${r} ${r} 0 0 0 ${ex.toFixed(1)} ${ey.toFixed(1)}`
  return (
    <svg viewBox="0 0 120 65" style={{ width: 120 }}>
      <path d={bgPath} fill="none" stroke="#e5e7eb" strokeWidth={sw} strokeLinecap="round" />
      <path d={fillPath} fill="none" stroke="#0d9488" strokeWidth={sw} strokeLinecap="round" />
      <text x={cx} y={cy + 2} textAnchor="middle" fill="#0d9488" fontSize="16" fontWeight="700" fontFamily="Lexend, sans-serif">
        {Math.round(pct * 100)}%
      </text>
      <text x={cx} y={cy + 14} textAnchor="middle" fill="#94a3b8" fontSize="8" fontFamily="Lexend, sans-serif">
        Overall Progress
      </text>
    </svg>
  )
}

// ── Dashboard Screen ─────────────────────────────────────────────────────────
export default function DashboardScreen() {
  const navigate = useNavigate()
  const { childData, learningLevel, moduleProgress, currentModuleIndex, update } = useApp()

  const [modules, setModules]   = useState([])
  const [levelData, setLevelData] = useState(null)

  const name  = childData?.child_name || 'Nathaniel'
  const level = learningLevel || 3

  useEffect(() => {
    getModules(level)
      .then((d) => { setLevelData(d.data); setModules(d.data?.modules || []) })
      .catch(() => {})
  }, [level])

  const completedModules = Object.values(moduleProgress).filter(v => v === 'passed').length
  const totalModules     = modules.length || 4
  const levelPct         = Math.round((completedModules / totalModules) * 100)

  // Fallback module cards if API doesn't return
  const displayModules = modules.length > 0 ? modules.slice(0, 6) : [
    { name: 'Phonics' }, { name: 'Word Reading' }, { name: 'Vocabulary' },
    { name: 'Listening' }, { name: 'Comprehension' }, { name: 'Learning Games' },
  ]

  return (
    <div className="flex min-h-screen" style={{ background: '#f8fafc' }}>
      <Sidebar active="Learning" />

      <main className="flex-1 overflow-y-auto min-w-0">
        {/* Top bar */}
        <div className="flex items-center justify-between px-6 py-4 bg-white border-b border-gray-100">
          <div>
            <h1 className="text-2xl font-bold text-gray-800">Welcome back, {name}! 👋</h1>
            <p className="text-sm text-gray-400">Let's continue your learning journey today.</p>
          </div>
          <div className="flex items-center gap-3">
            <div className="relative">
              <span className="text-xl cursor-pointer">🔔</span>
              <div className="absolute -top-1 -right-1 w-4 h-4 rounded-full bg-red-500 text-white text-[9px] flex items-center justify-center font-bold">3</div>
            </div>
            <div className="flex items-center gap-2 pl-3 border-l border-gray-100">
              <div className="w-9 h-9 rounded-full flex items-center justify-center text-xl" style={{ background: '#fce8f3' }}>🧠</div>
              <div>
                <div className="text-xs font-bold text-gray-700">AI Buddy</div>
                <div className="text-[10px] text-gray-400">Your learning companion</div>
              </div>
            </div>
          </div>
        </div>

        <div className="p-6 space-y-6">
          {/* Learning Path Banner */}
          <LearningPathBanner level={level} levelData={levelData} completedPct={levelPct} />

          {/* Today's Goals */}
          <div>
            <div className="flex items-center gap-2 mb-3">
              <span className="text-lg">🎯</span>
              <h2 className="font-bold text-gray-800">Today's Goals</h2>
            </div>
            <div className="grid grid-cols-3 gap-4">
              {[
                { icon: '📚', label: 'Complete 3 Lessons', progress: `${Math.min(completedModules, 3)} / 3`, pct: Math.min(completedModules / 3, 1), color: '#2563eb' },
                { icon: '⏱️', label: 'Practice for 15 mins', progress: '10 / 15 mins', pct: 0.67, color: '#2563eb' },
                { icon: '⭐', label: 'Score 80% or higher', progress: '1 / 1', pct: 1, color: '#10b981' },
              ].map((g) => (
                <div key={g.label} className="bg-white rounded-2xl p-4 border border-gray-100 flex items-center gap-3">
                  <div className="w-10 h-10 rounded-xl flex items-center justify-center text-xl" style={{ background: g.color + '10' }}>
                    {g.icon}
                  </div>
                  <div className="flex-1">
                    <div className="text-xs font-bold text-gray-700">{g.label}</div>
                    <div className="text-xs text-gray-400 mb-1.5">{g.progress}</div>
                    <div className="h-1.5 rounded-full bg-gray-100 overflow-hidden">
                      <div className="h-full rounded-full" style={{ width: `${g.pct * 100}%`, background: g.color }} />
                    </div>
                  </div>
                  {g.pct >= 1 && <span className="text-lg text-green-500">✓</span>}
                </div>
              ))}
            </div>
          </div>

          {/* Continue Learning */}
          <div>
            <h2 className="font-bold text-gray-800 mb-3">Continue Learning</h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {displayModules.map((m, i) => (
                <ModuleCard
                  key={m.name || i}
                  title={m.name || `Module ${i + 1}`}
                  subtitle={MODULE_SUBTITLES[i] || m.description || ''}
                  idx={i}
                  pct={moduleProgress[i] === 'passed' ? 100 : i === currentModuleIndex ? 20 : [70,55,40,60,35,80][i] || 0}
                  color={SKILL_COLORS[i % SKILL_COLORS.length]}
                  onClick={() => { update({ currentModuleIndex: i }); navigate('/screening-intro') }}
                  status={moduleProgress[i]}
                />
              ))}
            </div>
          </div>

          {/* AI Tutor Banner */}
          <div className="rounded-2xl p-5 flex items-center gap-4 border border-pink-100" style={{ background: '#fdf2f8' }}>
            <div className="text-4xl">🤖</div>
            <div className="flex-1">
              <div className="font-bold text-gray-800">AI Tutor is here to help!</div>
              <div className="text-sm text-gray-500">Ask questions, get hints, and learn in a fun way.</div>
            </div>
            <button className="px-5 py-2.5 rounded-xl text-sm font-semibold border-2 border-purple-200 text-purple-700 hover:bg-purple-50">
              Chat with AI Tutor ✨
            </button>
          </div>

          {/* Footer */}
          <div className="flex items-center justify-center gap-2 text-xs text-gray-400 pt-4 border-t border-gray-100">
            <span>🔒</span>
            <span className="font-semibold" style={{ color: '#0d9488' }}>A safe learning environment</span>
            <span>— We protect your child's data and privacy with enterprise-grade security.</span>
          </div>

          <div className="flex items-center justify-between text-xs text-gray-400 pb-4">
            <span>© 2026 NeuroLearn Kids. All rights reserved.</span>
            <div className="flex gap-4">
              <a href="#" className="hover:text-teal-600">Privacy Policy</a>
              <a href="#" className="hover:text-teal-600">Terms of Use</a>
              <a href="#" className="hover:text-teal-600">Help Center</a>
            </div>
          </div>
        </div>
      </main>

      <RightSidebar completedModules={completedModules} totalModules={totalModules} level={level} />
    </div>
  )
}
