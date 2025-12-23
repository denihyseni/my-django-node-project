import React, { useState, useEffect } from 'react'
import { Routes, Route, Link, useNavigate } from 'react-router-dom'
import axios from 'axios'
import Login from './Login'
import AdminDashboard from './pages/AdminDashboard'
import ProfessorDashboard from './pages/ProfessorDashboard'
import StudentDashboard from './pages/StudentDashboard'
import './styles.css'

export default function App(){
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [loading, setLoading] = useState(true)
  const navigate = useNavigate()

  useEffect(() => {
    const verifyToken = async () => {
      const token = localStorage.getItem('access')
      if (token) {
        try {
          // Verify token is still valid by making a test request
          await axios.get('/api/university/dashboard/', {
            headers: { Authorization: `Bearer ${token}` },
            withCredentials: true
          })
          setIsLoggedIn(true)
        } catch (err) {
          // Token invalid or expired
          console.log('Token invalid, clearing storage')
          localStorage.removeItem('access')
          localStorage.removeItem('refresh')
          setIsLoggedIn(false)
        }
      }
      setLoading(false)
    }

    verifyToken()
  }, [])

  const handleLogout = async () => {
    try {
      // Call logout endpoint to blacklist tokens
      await axios.post('/api/auth/logout/', {}, {
        headers: localStorage.getItem('access') ? { Authorization: `Bearer ${localStorage.getItem('access')}` } : {},
        withCredentials: true
      })
    } catch (err) {
      console.error('Logout error:', err)
    } finally {
      // Clear local storage and session
      localStorage.removeItem('access')
      localStorage.removeItem('refresh')
      sessionStorage.clear()
      setIsLoggedIn(false)
      navigate('/login')
    }
  }

  if (loading) {
    return <div className="app-root"><p style={{textAlign: 'center', marginTop: '50px'}}>Loading...</p></div>
  }

  return (
    <div className="app-root">
      <header className="topbar">
        <div className="brand">🎓 University Portal</div>
        <nav>
          {isLoggedIn ? (
            <button onClick={handleLogout} className="nav-link" style={{background:'none', border:'none', fontSize:'1rem', padding:0, cursor: 'pointer'}}>Logout</button>
          ) : (
            <Link to="/login" className="nav-link">Login</Link>
          )}
        </nav>
      </header>
      <main className="container">
        <Routes>
          <Route path="/login" element={<Login setIsLoggedIn={setIsLoggedIn}/>} />
          <Route path="/admin" element={isLoggedIn ? <AdminDashboard/> : <div className="home-hero"><h2>Access Denied</h2><p>You must be logged in to access this page.</p><p><Link to="/login" style={{color:'var(--accent)'}}>Click here to login</Link></p></div>} />
          <Route path="/professor" element={isLoggedIn ? <ProfessorDashboard/> : <div className="home-hero"><h2>Access Denied</h2><p>You must be logged in to access this page.</p><p><Link to="/login" style={{color:'var(--accent)'}}>Click here to login</Link></p></div>} />
          <Route path="/student" element={isLoggedIn ? <StudentDashboard/> : <div className="home-hero"><h2>Access Denied</h2><p>You must be logged in to access this page.</p><p><Link to="/login" style={{color:'var(--accent)'}}>Click here to login</Link></p></div>} />
          <Route path="/" element={<div className="home-hero"><h2>Welcome to the University Portal</h2><p>A comprehensive platform for managing students, professors, and courses.</p><p><Link to="/login" style={{color:'var(--accent)'}}>Click here to login</Link></p></div>} />
        </Routes>
      </main>
    </div>
  )
}
