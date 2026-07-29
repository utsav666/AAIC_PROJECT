import React from 'react'

// ── Brand Panel (left column on auth screens) ──────────────────────────────────
export function BrandPanel() {
  return (
    <div
      className="w-full h-full min-h-screen flex flex-col items-center justify-center p-10"
      style={{ background: 'linear-gradient(160deg, #0d9488 0%, #7c3aed 65%, #ec4899 100%)' }}
    >
      <div className="text-7xl mb-4 select-none">🧠</div>
      <div className="text-white text-center mb-6">
        <div className="text-4xl font-extrabold tracking-tight">NeuroLearn</div>
        <div className="text-xs font-bold tracking-widest mt-1 opacity-75">KIDS</div>
        <div className="w-10 h-1 bg-white/30 rounded mx-auto my-3" />
        <h2 className="text-xl font-bold leading-snug max-w-xs mx-auto">
          Empowering Every Child to Read, Learn &amp; Thrive
        </h2>
        <p className="text-sm opacity-70 mt-3 max-w-xs leading-relaxed mx-auto">
          AI-powered dyslexia assessment and personalised learning pathways for children aged 5–16.
        </p>
      </div>

      {/* Feature pills */}
      <div className="grid grid-cols-2 gap-2 w-full max-w-xs mt-4">
        {[
          ['🎯', 'AI Assessment'],
          ['📚', 'Adaptive Learning'],
          ['📈', 'Track Progress'],
          ['🔒', 'Safe & Trusted'],
        ].map(([icon, label]) => (
          <div
            key={label}
            className="flex items-center gap-2 rounded-xl px-3 py-2"
            style={{ background: 'rgba(255,255,255,0.15)' }}
          >
            <span className="text-lg">{icon}</span>
            <span className="text-white text-xs font-semibold">{label}</span>
          </div>
        ))}
      </div>

      {/* Kids illustration placeholder */}
      <div className="mt-8 text-6xl opacity-30 select-none">📖✏️🌟</div>
    </div>
  )
}

// ── Feature Bar (bottom of auth screens) ──────────────────────────────────────
export function FeatureBar() {
  return (
    <div className="grid grid-cols-2 md:grid-cols-4 gap-4 px-8 py-4 bg-white/60 backdrop-blur-sm border-t border-white/50">
      {[
        { icon: '🎯', title: 'AI Assessment',    desc: 'Smart screening technology' },
        { icon: '📚', title: 'Adaptive Learning', desc: 'Personalised to your child' },
        { icon: '📈', title: 'Track Progress',    desc: 'See growth over time' },
        { icon: '🔒', title: 'Trusted & Safe',   desc: 'PDPA compliant' },
      ].map((f) => (
        <div key={f.title} className="flex items-center gap-3">
          <span className="text-2xl">{f.icon}</span>
          <div>
            <div className="text-xs font-bold text-gray-700">{f.title}</div>
            <div className="text-xs text-gray-400">{f.desc}</div>
          </div>
        </div>
      ))}
    </div>
  )
}

// ── Footer ─────────────────────────────────────────────────────────────────────
export function Footer() {
  return (
    <div className="flex items-center justify-between px-8 py-3 bg-white/40 border-t border-white/30 text-xs text-gray-400">
      <span>© 2026 NeuroLearn KIDS. All rights reserved.</span>
      <div className="flex gap-4">
        <a href="#" className="hover:text-teal-600">Privacy Policy</a>
        <a href="#" className="hover:text-teal-600">Terms of Use</a>
        <a href="#" className="hover:text-teal-600">Help</a>
      </div>
    </div>
  )
}

// ── Step Indicator ─────────────────────────────────────────────────────────────
export function StepIndicator({ steps, current }) {
  return (
    <div className="flex items-start justify-center gap-0 mb-8">
      {steps.map((label, i) => {
        const done   = i < current
        const active = i === current
        return (
          <React.Fragment key={i}>
            {i > 0 && (
              <div
                className="h-0.5 w-12 mt-4 flex-shrink-0"
                style={{ background: done ? '#0d9488' : '#e2e8f0' }}
              />
            )}
            <div className="flex flex-col items-center gap-1 min-w-0">
              <div
                className="w-8 h-8 rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0"
                style={{
                  background: done || active ? '#0d9488' : '#e2e8f0',
                  color: done || active ? 'white' : '#94a3b8',
                }}
              >
                {done ? '✓' : i + 1}
              </div>
              <span
                className="text-xs font-medium text-center leading-tight"
                style={{ color: active ? '#0d9488' : '#94a3b8', maxWidth: 72 }}
              >
                {label}
              </span>
            </div>
          </React.Fragment>
        )
      })}
    </div>
  )
}

// ── Gauge Chart (semicircle) ───────────────────────────────────────────────────
const SEVERITY_COLORS = { 1: '#10b981', 2: '#22c55e', 3: '#eab308', 4: '#f97316', 5: '#ef4444' }
const SEVERITY_LABELS = { 1: 'MINIMAL', 2: 'MILD', 3: 'MODERATE', 4: 'SIGNIFICANT', 5: 'SEVERE' }

export function GaugeChart({ level = 2 }) {
  const cx = 100, cy = 92, r = 72, sw = 16
  const inner = r - sw / 2   // stroke drawn at its center line

  // pct 0→1 mapped from level 1→5 (cap at 0.99 to avoid degenerate arc)
  const pct    = Math.min((level - 1) / 4, 0.99)
  const color  = SEVERITY_COLORS[level] || '#22c55e'
  const slabel = SEVERITY_LABELS[level] || ''

  // Background arc: full semicircle split into 2 × 90° to avoid degeneracy
  const topX   = cx
  const topY   = cy - inner
  const bgPath = `M ${cx - inner} ${cy} A ${inner} ${inner} 0 0 0 ${topX} ${topY} A ${inner} ${inner} 0 0 0 ${cx + inner} ${cy}`

  // Filled arc: from left, counter-clockwise (sweep=0) to fill point
  const angle    = Math.PI * (1 - pct)                     // π (left) → 0 (right)
  const ex       = cx + inner * Math.cos(angle)
  const ey       = cy - inner * Math.sin(angle)            // SVG y inverted
  const fillPath = pct < 0.01
    ? null
    : `M ${cx - inner} ${cy} A ${inner} ${inner} 0 0 0 ${ex.toFixed(2)} ${ey.toFixed(2)}`

  return (
    <svg viewBox="0 0 200 115" style={{ width: '100%', maxWidth: 300 }}>
      {/* Background track */}
      <path d={bgPath} fill="none" stroke="#e5e7eb" strokeWidth={sw} strokeLinecap="round" />
      {/* Filled track */}
      {fillPath && (
        <path d={fillPath} fill="none" stroke={color} strokeWidth={sw} strokeLinecap="round" />
      )}
      {/* Level number */}
      <text x={cx} y={cy - 2} textAnchor="middle" fill={color}
            fontSize="40" fontWeight="700" fontFamily="Lexend, sans-serif">
        {level}
      </text>
      {/* Severity label */}
      <text x={cx} y={cy + 18} textAnchor="middle" fill="#6b7280"
            fontSize="11" fontFamily="Lexend, sans-serif">
        {slabel}
      </text>
      {/* Scale endpoints */}
      <text x={cx - inner - 8} y={cy + 6} textAnchor="end"   fill="#d1d5db" fontSize="10">1</text>
      <text x={cx + inner + 8} y={cy + 6} textAnchor="start" fill="#d1d5db" fontSize="10">5</text>
    </svg>
  )
}

// ── Input field ────────────────────────────────────────────────────────────────
export function Input({ label, ...props }) {
  return (
    <div>
      {label && <label className="block text-sm font-semibold text-gray-700 mb-1.5">{label}</label>}
      <input
        {...props}
        className={`w-full px-4 py-3 border border-gray-200 rounded-xl text-sm
          focus:outline-none focus:ring-2 focus:border-transparent
          placeholder:text-gray-300 ${props.className || ''}`}
        style={{ focusRingColor: '#0d9488', ...props.style }}
        onFocus={(e) => { e.target.style.boxShadow = '0 0 0 3px rgba(13,148,136,0.2)'; e.target.style.borderColor = '#0d9488'; if (props.onFocus) props.onFocus(e) }}
        onBlur={(e)  => { e.target.style.boxShadow = ''; e.target.style.borderColor = '#e5e7eb'; if (props.onBlur) props.onBlur(e) }}
      />
    </div>
  )
}

// ── Section header used in forms ───────────────────────────────────────────────
export function SectionHeader({ icon, title, color = '#7c3aed' }) {
  return (
    <div className="flex items-center gap-3 mb-4 mt-2">
      <div className="w-9 h-9 rounded-xl flex items-center justify-center text-lg flex-shrink-0"
           style={{ background: color + '18' }}>
        {icon}
      </div>
      <span className="font-bold text-gray-800">{title}</span>
    </div>
  )
}
