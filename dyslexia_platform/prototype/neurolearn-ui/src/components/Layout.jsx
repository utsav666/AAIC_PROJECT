import React from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { useApp } from '../App'

// ── Sidebar ──────────────────────────────────────────────────────────────────
const NAV = [
  { icon: '🏠', label: 'Dashboard',    path: '/dashboard' },
  { icon: '🔬', label: 'Screening',    path: '/results' },
  { icon: '📚', label: 'Learning Path',path: '/dashboard' },
  { icon: '📖', label: 'Lessons',      path: '/dashboard' },
  { icon: '✏️', label: 'Practice',     path: '/dashboard' },
  { icon: '📈', label: 'Progress',     path: '/dashboard' },
  { icon: '📊', label: 'Reports',      path: '/dashboard' },
  { icon: '🏆', label: 'Achievements', path: '/dashboard' },
  { icon: '⚙️', label: 'Settings',     path: '/dashboard' },
  { icon: '❓', label: 'Help & Support',path: '/dashboard' },
]

export function Sidebar({ active = 'Dashboard' }) {
  const navigate = useNavigate()
  const { childData } = useApp()
  const name  = childData?.child_name || 'Nathaniel'
  const grade = childData?.grade || 'Grade 3'
  const age   = childData?.child_age || 9

  return (
    <aside className="w-56 flex-shrink-0 flex flex-col bg-white border-r border-gray-100 min-h-screen">
      {/* Logo */}
      <div className="flex flex-col items-center px-4 py-5">
        <div className="text-4xl mb-1">🧠</div>
        <div className="text-lg font-extrabold" style={{ color: '#1a3a5c' }}>NeuroLearn</div>
        <div className="text-xs font-bold tracking-[0.25em]" style={{ color: '#0d9488' }}>K I D S</div>
      </div>

      {/* Nav */}
      <nav className="flex-1 px-3 space-y-0.5 mt-2">
        {NAV.slice(0, 8).map((item) => {
          const isActive = item.label === active
          return (
            <button
              key={item.label}
              onClick={() => navigate(item.path)}
              className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-left transition-all"
              style={{
                background: isActive ? '#e6f7f5' : 'transparent',
                color: isActive ? '#0d9488' : '#64748b',
                fontWeight: isActive ? 600 : 400,
              }}
            >
              <span className="text-base opacity-80">{item.icon}</span>
              {item.label}
            </button>
          )
        })}
        {/* Divider before settings */}
        <div className="my-3 border-t border-gray-100" />
        {NAV.slice(8).map((item) => (
          <button
            key={item.label}
            onClick={() => navigate(item.path)}
            className="w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-gray-400 hover:text-gray-600 text-left"
          >
            <span className="text-base opacity-60">{item.icon}</span>
            {item.label}
          </button>
        ))}
      </nav>

      {/* Child profile */}
      <div className="px-3 pb-3">
        <div className="p-3 rounded-xl bg-gray-50 border border-gray-100 mb-3">
          <div className="flex items-center gap-2">
            <div
              className="w-10 h-10 rounded-full flex items-center justify-center text-white text-sm font-bold"
              style={{ background: 'linear-gradient(135deg, #0d9488, #7c3aed)' }}
            >
              {name[0]}
            </div>
            <div>
              <div className="text-sm font-bold text-gray-800">{name}</div>
              <div className="text-xs text-gray-400">{grade} · Age {age}</div>
            </div>
          </div>
          <button className="text-xs font-semibold mt-2 hover:underline" style={{ color: '#0d9488' }}>
            Switch Child &gt;
          </button>
        </div>

        {/* Upgrade */}
        <div className="p-3 rounded-xl border border-purple-100 bg-purple-50/50">
          <div className="text-xs font-bold text-purple-600 mb-1">⭐ Unlock more!</div>
          <div className="text-xs text-gray-500 mb-2 leading-relaxed">
            Get unlimited lessons, games and expert insights.
          </div>
          <button className="w-full py-2 rounded-lg text-xs font-bold text-white" style={{ background: '#7c3aed' }}>
            🎖️ Upgrade Now
          </button>
        </div>
      </div>
    </aside>
  )
}

// ── Step Indicator (5 steps as per mockup) ───────────────────────────────────
export function StepperBar({ current = 5 }) {
  const steps = ['Sign In', 'Choose Account Type', 'Create Account', 'AI Screening', 'Results']
  return (
    <div className="flex items-center justify-center gap-0 mb-6">
      {steps.map((label, i) => {
        const done   = i < current - 1
        const active = i === current - 1
        return (
          <React.Fragment key={i}>
            {i > 0 && (
              <div
                className="flex-1 h-0.5 max-w-16"
                style={{ background: done || active ? '#0d9488' : '#e2e8f0' }}
              />
            )}
            <div className="flex flex-col items-center gap-1">
              <div
                className="w-8 h-8 rounded-full flex items-center justify-center text-xs font-bold flex-shrink-0"
                style={{
                  background: done || active ? '#0d9488' : '#f1f5f9',
                  color: done || active ? 'white' : '#94a3b8',
                  border: active ? '3px solid #99f6e4' : 'none',
                }}
              >
                {done ? '✓' : i + 1}
              </div>
              <span className="text-[10px] text-gray-400 text-center max-w-16 leading-tight">{label}</span>
            </div>
          </React.Fragment>
        )
      })}
    </div>
  )
}
