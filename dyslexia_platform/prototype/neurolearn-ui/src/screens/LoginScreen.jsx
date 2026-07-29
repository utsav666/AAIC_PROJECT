import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'

export default function LoginScreen() {
  const navigate = useNavigate()
  const [email, setEmail]       = useState('')
  const [password, setPassword] = useState('')
  const [showPw, setShowPw]     = useState(false)

  const handleLogin = (e) => { e.preventDefault(); navigate('/account-type') }

  return (
    <div className="min-h-screen flex flex-col" style={{ background: 'linear-gradient(160deg, #e8faf8 0%, #ede9fe 50%, #fce8f3 100%)' }}>
      {/* Main two-column area */}
      <div className="flex flex-1">
        {/* ── Left Brand Panel ─────────────────────────────────────── */}
        <div className="hidden lg:flex w-[380px] flex-shrink-0 flex-col items-center px-10 pt-14 pb-8 relative">
          {/* Decorative dots */}
          <div className="absolute top-6 right-6 grid grid-cols-3 gap-1.5 opacity-30">
            {[...Array(9)].map((_,i) => <div key={i} className="w-2 h-2 rounded-full bg-purple-300" />)}
          </div>

          {/* Brain Logo + Brand */}
          <div className="text-6xl mb-2">🧠</div>
          <div className="text-3xl font-extrabold" style={{ color: '#0d9488' }}>NeuroLearn</div>
          <div className="text-xs font-bold tracking-[0.3em] mt-1" style={{ color: '#0d9488' }}>KIDS</div>

          <div className="mt-8 text-left w-full">
            <h2 className="text-2xl font-bold text-gray-800 leading-snug mb-3">
              AI-Powered Learning<br/>for Every Unique Mind
            </h2>
            <div className="w-10 h-1 rounded bg-pink-300 mb-4" />
            <p className="text-sm text-gray-500 leading-relaxed">
              Personalized support to help children with dyslexia learn to read, build confidence and thrive.
            </p>
          </div>

          {/* Kids illustration */}
          <div className="mt-auto flex items-end justify-center w-full relative">
            <div className="absolute -top-10 left-4 text-3xl opacity-60">📖</div>
            <div className="absolute -top-6 right-8 text-2xl opacity-60">💬</div>
            <div className="text-7xl">👦🏻👧🏻</div>
          </div>
        </div>

        {/* ── Right Login Card ────────────────────────────────────── */}
        <div className="flex-1 flex flex-col items-center justify-center p-8">
          <div className="bg-white rounded-3xl shadow-xl p-10 w-full max-w-md">
            {/* Mobile logo */}
            <div className="lg:hidden text-center mb-6">
              <span className="text-4xl">🧠</span>
              <div className="text-xl font-extrabold" style={{ color: '#0d9488' }}>NeuroLearn <span className="text-purple-600">KIDS</span></div>
            </div>

            <h1 className="text-3xl font-bold text-gray-800 text-center mb-1">Welcome Back!</h1>
            <p className="text-gray-400 text-sm text-center mb-8">Sign in to continue your learning journey.</p>

            <form onSubmit={handleLogin} className="space-y-5">
              {/* Email */}
              <div className="relative">
                <span className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-300">✉️</span>
                <input
                  type="email" value={email} onChange={e => setEmail(e.target.value)}
                  placeholder="Email address"
                  className="w-full pl-12 pr-4 py-3.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-200 focus:border-teal-400 placeholder:text-gray-300"
                  required
                />
              </div>

              {/* Password */}
              <div className="relative">
                <span className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-300">🔒</span>
                <input
                  type={showPw ? 'text' : 'password'} value={password} onChange={e => setPassword(e.target.value)}
                  placeholder="Password"
                  className="w-full pl-12 pr-12 py-3.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-200 focus:border-teal-400 placeholder:text-gray-300"
                  required
                />
                <button type="button" onClick={() => setShowPw(!showPw)} className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-300 hover:text-gray-500 text-sm">
                  {showPw ? '🙈' : '👁️'}
                </button>
              </div>

              {/* Forgot */}
              <div className="text-right">
                <a href="#" className="text-xs font-semibold hover:underline" style={{ color: '#0d9488' }}>Forgot Password?</a>
              </div>

              {/* Login Button */}
              <button type="submit" className="w-full py-3.5 rounded-xl text-white font-semibold text-sm" style={{ background: '#0d9488' }}>
                Log In
              </button>
            </form>

            {/* Divider */}
            <div className="flex items-center gap-3 my-6">
              <div className="flex-1 h-px bg-gray-100" />
              <span className="text-xs text-gray-300">or continue with</span>
              <div className="flex-1 h-px bg-gray-100" />
            </div>

            {/* Social */}
            <div className="space-y-3 mb-6">
              <button type="button" className="w-full flex items-center justify-center gap-3 py-3 border border-gray-200 rounded-xl text-sm font-medium text-gray-700 hover:bg-gray-50">
                <span className="text-lg">🇬</span> Continue with Google
              </button>
              <button type="button" className="w-full flex items-center justify-center gap-3 py-3 border border-gray-200 rounded-xl text-sm font-medium text-gray-700 hover:bg-gray-50">
                <span className="text-lg">🍎</span> Continue with Apple
              </button>
            </div>

            {/* Create account */}
            <p className="text-center text-sm text-gray-400 mb-6">
              New to NeuroLearn Kids?{' '}
              <button type="button" onClick={() => navigate('/account-type')} className="font-semibold hover:underline" style={{ color: '#0d9488' }}>
                Create an Account
              </button>
            </p>

            {/* Security badge */}
            <div className="flex items-center gap-3 p-3 rounded-xl bg-gray-50 border border-gray-100">
              <div className="w-9 h-9 rounded-full bg-teal-50 flex items-center justify-center text-lg flex-shrink-0">🛡️</div>
              <div>
                <div className="text-xs font-bold" style={{ color: '#0d9488' }}>Safe. Secure. Private.</div>
                <div className="text-[11px] text-gray-400">We protect your child's data and privacy with enterprise-grade security.</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* ── Feature Bar ─────────────────────────────────────────── */}
      <div className="bg-white border-t border-gray-100 px-10 py-6">
        <div className="max-w-4xl mx-auto grid grid-cols-3 gap-6">
          {[
            { icon: '🧠', bg: '#ede9fe', title: 'AI-Powered Assessment', desc: 'Identifies learning strengths and needs.' },
            { icon: '📚', bg: '#e6f7f5', title: 'Adaptive Learning', desc: 'Personalized lessons that grow with your child.' },
            { icon: '📈', bg: '#fce8f3', title: 'Track Progress', desc: 'Real-time insights for parents and educators.' },
          ].map(f => (
            <div key={f.title} className="flex items-center gap-3">
              <div className="w-11 h-11 rounded-full flex items-center justify-center text-xl flex-shrink-0" style={{ background: f.bg }}>{f.icon}</div>
              <div>
                <div className="text-sm font-bold text-gray-800">{f.title}</div>
                <div className="text-xs text-gray-400">{f.desc}</div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* ── Footer ──────────────────────────────────────────────── */}
      <div className="flex items-center justify-between px-10 py-4 text-xs text-gray-400" style={{ background: 'linear-gradient(90deg, #e8faf8, #ede9fe)' }}>
        <span>© 2026 NeuroLearn Kids. All rights reserved.</span>
        <div className="flex gap-4">
          <a href="#" className="hover:text-teal-600">Privacy Policy</a>
          <span>|</span>
          <a href="#" className="hover:text-teal-600">Terms of Use</a>
          <span>|</span>
          <a href="#" className="hover:text-teal-600">Help Center</a>
        </div>
      </div>
    </div>
  )
}
