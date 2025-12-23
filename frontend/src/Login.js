import React, { useState } from 'react'
import axios from 'axios'
import { useNavigate } from 'react-router-dom'

export default function Login({ setIsLoggedIn }) {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const navigate = useNavigate()

  // ✅ API base URL (Vercel → PythonAnywhere)
  const API_BASE =
    process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000'

  const submit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      console.log('Login attempt', { username })

      // ✅ single correct request (no fallback)
      const res = await axios.post(
        `${API_BASE}/api/auth/token/`,
        { username, password },
        { withCredentials: true }
      )

      console.log('Token response', res.data)

      if (res.data?.access) {
        localStorage.setItem('access', res.data.access)
      }
      if (res.data?.refresh) {
        localStorage.setItem('refresh', res.data.refresh)
      }

      axios.defaults.withCredentials = true
      axios.defaults.headers.common['Authorization'] =
        `Bearer ${res.data.access}`

      if (setIsLoggedIn) setIsLoggedIn(true)

      // ✅ dashboard request uses API_BASE
      const dash = await axios.get(
        `${API_BASE}/api/university/dashboard/`,
        {
          headers: {
            Authorization: `Bearer ${res.data.access}`,
          },
        }
      )

      const role = dash.data.role

      if (role === 'administrator') navigate('/admin')
      else if (role === 'professor') navigate('/professor')
      else if (role === 'student') navigate('/student')
      else navigate('/')
    } catch (err) {
      console.error('Login error', err)

      let msg = 'Login failed — check credentials and server status.'
      if (err.response?.data) {
        msg += ` (${JSON.stringify(err.response.data)})`
      }

      setError(msg)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="login-card">
      <h2>Sign in</h2>

      <form onSubmit={submit}>
        <div className="form-row">
          <label>Username</label>
          <input
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="admin_user"
          />
        </div>

        <div className="form-row">
          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="admin123"
          />
        </div>

        {error && (
          <div style={{ color: '#ffb4b4', marginBottom: 12 }}>
            {error}
          </div>
        )}

        <div style={{ textAlign: 'right' }}>
          <button className="btn" type="submit" disabled={loading}>
            {loading ? 'Signing in...' : 'Sign in'}
          </button>
        </div>
      </form>
    </div>
  )
}
