import React, { createContext, useContext, useState } from 'react'
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import LoginScreen from './screens/LoginScreen'
import AccountTypeScreen from './screens/AccountTypeScreen'
import RegisterScreen from './screens/RegisterScreen'
import ScreeningIntroScreen from './screens/ScreeningIntroScreen'
import AssessmentScreen from './screens/AssessmentScreen'
import AnalyzingScreen from './screens/AnalyzingScreen'
import ResultsScreen from './screens/ResultsScreen'
import DashboardScreen from './screens/DashboardScreen'

// ── App Context ────────────────────────────────────────────────────────────────
export const AppContext = createContext(null)
export const useApp = () => useContext(AppContext)

const INITIAL = {
  userRole: null,
  childData: {},
  questions: [],
  responses: [],
  currentQuestion: 0,
  assessmentResult: null,
  learningLevel: 1,
  moduleProgress: {},
  currentModuleIndex: 0,
}

function AppProvider({ children }) {
  const [state, setState] = useState(INITIAL)
  const update = (patch) => setState((s) => ({ ...s, ...patch }))
  const reset  = () => setState(INITIAL)
  return (
    <AppContext.Provider value={{ ...state, update, reset }}>
      {children}
    </AppContext.Provider>
  )
}

// ── Router ─────────────────────────────────────────────────────────────────────
export default function App() {
  return (
    <BrowserRouter>
      <AppProvider>
        <Routes>
          <Route path="/"                element={<Navigate to="/login" replace />} />
          <Route path="/login"           element={<LoginScreen />} />
          <Route path="/account-type"    element={<AccountTypeScreen />} />
          <Route path="/register"        element={<RegisterScreen />} />
          <Route path="/screening-intro" element={<ScreeningIntroScreen />} />
          <Route path="/assessment"      element={<AssessmentScreen />} />
          <Route path="/analyzing"       element={<AnalyzingScreen />} />
          <Route path="/results"         element={<ResultsScreen />} />
          <Route path="/dashboard"       element={<DashboardScreen />} />
          <Route path="*"               element={<Navigate to="/login" replace />} />
        </Routes>
      </AppProvider>
    </BrowserRouter>
  )
}
