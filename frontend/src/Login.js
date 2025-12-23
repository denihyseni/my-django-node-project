import React, { useState } from 'react'
import axios from 'axios'
import { useNavigate } from 'react-router-dom'

export default function Login({ setIsLoggedIn }){
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const navigate = useNavigate()

  const submit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    try{
      console.log('Login attempt', { username })
      let res
      try{
        res = await axios.post('/api/auth/token/', { username, password }, { withCredentials: true })
      }catch(err){
        console.warn('Relative token request failed, trying full URL', err && err.message)
        res = await axios.post('http://127.0.0.1:8000/api/auth/token/', { username, password }, { withCredentials: true })
      }
      console.log('Token response', res && res.data)
      // Save tokens returned by the secure endpoint (also set as HttpOnly cookies)
      if(res.data?.access) localStorage.setItem('access', res.data.access)
      if(res.data?.refresh) localStorage.setItem('refresh', res.data.refresh)
      axios.defaults.withCredentials = true
      if(setIsLoggedIn) setIsLoggedIn(true)
      axios.defaults.headers.common['Authorization'] = `Bearer ${res.data.access}`
      const dash = await axios.get('/api/university/dashboard/', {
        headers: { Authorization: `Bearer ${res.data.access}` }
      })
      const role = dash.data.role
      if(role === 'administrator') navigate('/admin')
      else if(role === 'professor') navigate('/professor')
      else if(role === 'student') navigate('/student')
      else navigate('/')
    }catch(err){
      console.error('Login error', err)
      let msg = 'Login failed — check credentials and server status.'
      if(err.response && err.response.data) msg += ` (${JSON.stringify(err.response.data)})`
      setError(msg)
    }finally{ setLoading(false) }
  }

  return (
    <div className="login-card">
      <h2>Sign in</h2>
      <form onSubmit={submit}>
        <div className="form-row">
          <label>Username</label>
          <input value={username} onChange={e=>setUsername(e.target.value)} placeholder="admin_user" />
        </div>
        <div className="form-row">
          <label>Password</label>
          <input type="password" value={password} onChange={e=>setPassword(e.target.value)} placeholder="admin123" />
        </div>
        {error && <div style={{color:'#ffb4b4',marginBottom:12}}>{error}</div>}
        <div style={{textAlign:'right'}}>
          <button className="btn" type="submit" disabled={loading}>{loading? 'Signing in...':'Sign in'}</button>
        </div>
      </form>
      <hr style={{opacity:0.3, margin:'20px 0'}} />
      <p className="muted" style={{fontSize:'0.9rem'}}>
        <strong>Test Credentials:</strong><br/>
        • Admin: admin_user / admin123<br/>
        • Professor: professor1 / prof123<br/>
        • Student: student1 / student123
      </p>
    </div>
  )
}
