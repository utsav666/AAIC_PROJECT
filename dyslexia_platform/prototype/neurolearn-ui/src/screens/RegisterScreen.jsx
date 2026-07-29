import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useApp } from '../App'
import { StepIndicator } from '../components/Shared'
import { registerUser } from '../api'

export default function RegisterScreen() {
  const navigate = useNavigate()
  const { userRole, update } = useApp()
  const [loading, setLoading] = useState(false)
  const [error, setError]     = useState('')

  const [form, setForm] = useState({
    parent_name: '', parent_email: '', parent_mobile: '', password: '',
    child_name: '', child_dob: '', child_age: '', child_gender: '',
    grade: '', school: '', reading_level: '', previous_diagnosis: 'No', concerns: '',
  })
  const set = (k) => (e) => setForm(f => ({ ...f, [k]: e.target.value }))

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!form.parent_name || !form.child_name || !form.child_age) { setError('Please fill in the required fields.'); return }
    setLoading(true); setError('')
    try {
      await registerUser({ ...form, child_age: parseInt(form.child_age), user_role: userRole || 'parent' })
      update({ childData: { ...form, child_age: parseInt(form.child_age), user_role: userRole } })
      navigate('/screening-intro')
    } catch (err) { setError(err?.response?.data?.detail || 'Registration failed.') }
    finally { setLoading(false) }
  }

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

          <div className="flex items-center gap-2 mt-6 w-full">
            <div className="w-8 h-8 rounded-full bg-gray-100 flex items-center justify-center text-sm">🔒</div>
            <div>
              <div className="text-xs font-bold text-gray-700">Your data is safe with us</div>
              <div className="text-[11px] text-gray-400">We use enterprise-grade security to protect your family's information.</div>
            </div>
          </div>
        </div>

        {/* ── Right Card ──────────────────────────────────────── */}
        <div className="flex-1 flex flex-col items-center justify-start p-8 overflow-y-auto">
          <div className="bg-white rounded-3xl shadow-xl p-10 w-full max-w-xl my-4">
            {/* Step indicator */}
            <StepIndicator steps={['Sign In', 'Choose Account Type', 'Create Account']} current={2} />

            <h1 className="text-3xl font-bold text-gray-800 text-center mb-1">Let's get started!</h1>
            <div className="w-10 h-1 rounded bg-pink-300 mx-auto my-3" />
            <p className="text-gray-400 text-sm text-center mb-8">
              Please provide a few details to set up your account and your child's learning profile.
            </p>

            {error && (
              <div className="mb-4 p-3 rounded-xl bg-red-50 border border-red-200 text-sm text-red-600 text-center">{error}</div>
            )}

            <form onSubmit={handleSubmit} className="space-y-6">
              {/* ── Parent / Guardian Details ────────────────── */}
              <div>
                <div className="flex items-center gap-2 mb-4">
                  <span className="text-lg">👤</span>
                  <span className="font-bold text-sm" style={{ color: '#0d9488' }}>Parent / Guardian Details</span>
                </div>
                <div className="grid grid-cols-2 gap-3">
                  <FieldIcon icon="👤" placeholder="Full Name" value={form.parent_name} onChange={set('parent_name')} required />
                  <FieldIcon icon="✉️" placeholder="Email Address" type="email" value={form.parent_email} onChange={set('parent_email')} required />
                  <FieldIcon icon="📱" placeholder="+65  Mobile Number" value={form.parent_mobile} onChange={set('parent_mobile')} />
                  <div>
                    <FieldIcon icon="🔒" placeholder="Create Password" type="password" value={form.password} onChange={set('password')} required />
                    <div className="text-[10px] text-gray-400 mt-1 pl-1">Password must be at least 8 characters</div>
                  </div>
                </div>
              </div>

              {/* ── Child's Details ──────────────────────────── */}
              <div>
                <div className="flex items-center gap-2 mb-4">
                  <span className="text-lg">👶</span>
                  <span className="font-bold text-sm" style={{ color: '#0d9488' }}>Child's Details</span>
                </div>
                <div className="grid grid-cols-2 gap-3">
                  <FieldIcon icon="👤" placeholder="Child's Full Name" value={form.child_name} onChange={set('child_name')} required />
                  <FieldIcon icon="📅" placeholder="Date of Birth" type="date" value={form.child_dob} onChange={set('child_dob')} />
                  <SelectIcon icon="😊" value={form.child_gender} onChange={set('child_gender')} placeholder="Gender"
                    options={['Male','Female','Prefer not to say']} />
                  <FieldIcon icon="🎓" placeholder="Current Grade / Age" value={form.child_age} onChange={set('child_age')} type="number" min="4" max="16" required />
                  <div className="col-span-2">
                    <FieldIcon icon="🏫" placeholder="School (Optional)" value={form.school} onChange={set('school')} />
                  </div>
                </div>
              </div>

              {/* ── Learning Profile ─────────────────────────── */}
              <div>
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-lg">📋</span>
                  <span className="font-bold text-sm" style={{ color: '#db2777' }}>Learning Profile (Optional)</span>
                </div>
                <div className="text-xs text-gray-400 mb-4 pl-7">This helps us personalize your child's learning experience.</div>
                <div className="grid grid-cols-2 gap-3">
                  <SelectIcon icon="📖" value={form.reading_level} onChange={set('reading_level')} placeholder="How would you describe your child's reading level?"
                    options={['Below grade level','At grade level','Above grade level','Not sure']} />
                  <SelectIcon icon="🔍" value={form.previous_diagnosis} onChange={set('previous_diagnosis')} placeholder="Has your child been assessed for dyslexia?"
                    options={['No','Yes — diagnosed','Yes — not diagnosed','Unsure']} />
                  <div className="col-span-2 relative">
                    <span className="absolute left-4 top-4 text-gray-300">💬</span>
                    <textarea
                      value={form.concerns}
                      onChange={e => setForm(f => ({ ...f, concerns: e.target.value.slice(0, 250) }))}
                      placeholder="Any specific learning concerns or goals?"
                      rows={2}
                      className="w-full pl-12 pr-4 py-3.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-200 focus:border-teal-400 placeholder:text-gray-300 resize-none"
                    />
                    <div className="text-[10px] text-gray-400 text-right mt-0.5">{form.concerns.length} / 250</div>
                  </div>
                </div>
              </div>

              {/* Submit */}
              <button type="submit" disabled={loading}
                className="w-full py-4 rounded-xl text-white font-semibold text-sm flex items-center justify-center gap-2"
                style={{ background: '#0d9488' }}>
                {loading ? 'Creating...' : 'Create Account & Continue'} <span className="text-white">➜</span>
              </button>

              <p className="text-center text-xs text-gray-400">
                🔒 By creating an account, you agree to our{' '}
                <a href="#" className="font-semibold hover:underline" style={{ color: '#0d9488' }}>Terms of Use</a> and{' '}
                <a href="#" className="font-semibold hover:underline" style={{ color: '#0d9488' }}>Privacy Policy</a>.
              </p>

              <p className="text-center text-sm text-gray-400">
                Already have an account?{' '}
                <button type="button" onClick={() => navigate('/login')} className="font-bold hover:underline" style={{ color: '#1e293b' }}>Sign In</button>
              </p>
            </form>
          </div>
        </div>
      </div>

      {/* Feature bar */}
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

// ── Reusable input with icon ─────────────────────────────────────────────────
function FieldIcon({ icon, ...props }) {
  return (
    <div className="relative">
      <span className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-300 text-sm">{icon}</span>
      <input
        {...props}
        className="w-full pl-12 pr-4 py-3.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-200 focus:border-teal-400 placeholder:text-gray-300"
      />
    </div>
  )
}

function SelectIcon({ icon, value, onChange, placeholder, options }) {
  return (
    <div className="relative">
      <span className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-300 text-sm">{icon}</span>
      <select
        value={value} onChange={onChange}
        className="w-full pl-12 pr-4 py-3.5 border border-gray-200 rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-teal-200 focus:border-teal-400 appearance-none bg-white"
        style={{ color: value ? '#1e293b' : '#d1d5db' }}
      >
        <option value="" disabled>{placeholder}</option>
        {options.map(o => <option key={o} value={o} style={{ color: '#1e293b' }}>{o}</option>)}
      </select>
      <span className="absolute right-4 top-1/2 -translate-y-1/2 text-gray-300 text-xs pointer-events-none">▼</span>
    </div>
  )
}
