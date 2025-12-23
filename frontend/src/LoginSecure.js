import React, { useState } from 'react'
import axios from 'axios'
import { useNavigate } from 'react-router-dom'
import './LoginSecure.css'

export default function LoginSecure({ setIsLoggedIn }) {
    const [username, setUsername] = useState('')
    const [password, setPassword] = useState('')
    const [error, setError] = useState('')
    const [loading, setLoading] = useState(false)
    const navigate = useNavigate()

    const handleLogin = async (e) => {
        e.preventDefault()
        setLoading(true)
        setError('')

        try {
            // Login with credentials
            // Tokens will be automatically stored in HttpOnly cookies by the browser
            const response = await axios.post(
                'http://127.0.0.1:8000/api/auth/token/',
                { username, password },
                { 
                    withCredentials: true,  // Critical for cookies
                    headers: {
                        'Content-Type': 'application/json',
                    }
                }
            )

            if (response.status === 200) {
                // Tokens are now in HttpOnly cookies (not accessible via JS)
                setIsLoggedIn(true)
                navigate('/dashboard')
            }
        } catch (err) {
            const errorMsg = err.response?.data?.error || 
                           err.response?.data?.detail ||
                           'Login failed. Check credentials.'
            setError(errorMsg)
            console.error('Login error:', err)
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="login-container-secure">
            <div className="login-card">
                <h1>University Management System</h1>
                <p className="subtitle">Secure Login with HttpOnly Cookies</p>
                
                {error && (
                    <div className="error-message" role="alert">
                        ⚠️ {error}
                    </div>
                )}
                
                <form onSubmit={handleLogin}>
                    <div className="form-group">
                        <label htmlFor="username">Username</label>
                        <input
                            id="username"
                            type="text"
                            placeholder="Enter your username"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            required
                            disabled={loading}
                            autoComplete="username"
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="password">Password</label>
                        <input
                            id="password"
                            type="password"
                            placeholder="Enter your password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                            disabled={loading}
                            autoComplete="current-password"
                        />
                    </div>

                    <button 
                        type="submit" 
                        disabled={loading}
                        className="login-button"
                    >
                        {loading ? (
                            <>
                                <span className="spinner"></span>
                                Logging in...
                            </>
                        ) : (
                            'Login'
                        )}
                    </button>
                </form>

                <div className="credentials-section">
                    <h3>Test Credentials</h3>
                    <p className="note">🔒 Tokens are stored securely in HttpOnly cookies</p>
                    
                    <div className="credential-list">
                        <div className="credential-item admin">
                            <strong>Admin</strong>
                            <code>admin_user / admin123</code>
                            <span className="badge">Full Access</span>
                        </div>
                        
                        <div className="credential-item professor">
                            <strong>Professor</strong>
                            <code>professor1 / prof123</code>
                            <span className="badge">Grade Management</span>
                        </div>
                        
                        <div className="credential-item student">
                            <strong>Student</strong>
                            <code>student1 / student123</code>
                            <span className="badge">View Grades</span>
                        </div>
                    </div>
                </div>

                <div className="security-features">
                    <h4>🔐 Security Features Enabled</h4>
                    <ul>
                        <li>✅ HttpOnly Cookies (JavaScript cannot access tokens)</li>
                        <li>✅ Secure Flag (HTTPS only in production)</li>
                        <li>✅ SameSite=Strict (CSRF protection)</li>
                        <li>✅ Rate Limiting (5 attempts per 15 minutes)</li>
                        <li>✅ Session Tracking (IP & User-Agent logging)</li>
                        <li>✅ Token Rotation (New refresh token on refresh)</li>
                        <li>✅ Automatic Token Refresh (15-min expiry)</li>
                        <li>✅ Login Attempt Monitoring</li>
                    </ul>
                </div>
            </div>
        </div>
    )
}
