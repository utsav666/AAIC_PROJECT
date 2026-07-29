import axios from 'axios'

const api = axios.create({ baseURL: '/' })

export const registerUser   = (data)         => api.post('/api/register', data).then(r => r.data)
export const getQuestions   = (age)          => api.get(`/api/questions/${age}`).then(r => r.data)
export const assess         = (data)         => api.post('/api/assess', data).then(r => r.data)
export const getModules     = (level)        => api.get(`/api/modules/${level}`).then(r => r.data)
export const getModuleDetail= (level, idx)   => api.get(`/api/module/${level}/${idx}`).then(r => r.data)
export const genPractice    = (data)         => api.post('/api/practice', data).then(r => r.data)
export const genExam        = (data)         => api.post('/api/exam/generate', data).then(r => r.data)
export const evalExam       = (data)         => api.post('/api/exam/evaluate', data).then(r => r.data)
