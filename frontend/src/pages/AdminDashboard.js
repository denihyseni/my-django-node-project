import React, { useState, useEffect } from 'react'
import axios from 'axios'

export default function AdminDashboard() {
  const [stats, setStats] = useState(null)
  const [faculties, setFaculties] = useState([])
  const [subjects, setSubjects] = useState([])
  const [professors, setProfessors] = useState([])
  const [students, setStudents] = useState([])
  const [activeTab, setActiveTab] = useState('overview')
  const [loading, setLoading] = useState(false)
  const [formData, setFormData] = useState({})
  const [showForm, setShowForm] = useState(false)
  const [editingId, setEditingId] = useState(null)

  const token = localStorage.getItem('access')

  // ✅ ADD: API base (same fix as Login)
  const API_BASE =
    process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000'

  useEffect(() => {
    loadDashboardData()
    // eslint-disable-next-line
  }, [])

  const loadDashboardData = async () => {
    setLoading(true)
    try {
      const dashRes = await axios.get(
        `${API_BASE}/api/university/dashboard/`,
        { headers: { Authorization: `Bearer ${token}` } }
      )
      setStats(dashRes.data)

      const facRes = await axios.get(
        `${API_BASE}/api/university/faculties/`,
        { headers: { Authorization: `Bearer ${token}` } }
      )
      setFaculties(
        Array.isArray(facRes.data)
          ? facRes.data
          : facRes.data.results || []
      )

      const subRes = await axios.get(
        `${API_BASE}/api/university/subjects/`,
        { headers: { Authorization: `Bearer ${token}` } }
      )
      setSubjects(
        Array.isArray(subRes.data)
          ? subRes.data
          : subRes.data.results || []
      )

      const profRes = await axios.get(
        `${API_BASE}/api/university/professors/`,
        { headers: { Authorization: `Bearer ${token}` } }
      )
      setProfessors(
        Array.isArray(profRes.data)
          ? profRes.data
          : profRes.data.results || []
      )

      const studRes = await axios.get(
        `${API_BASE}/api/university/students/`,
        { headers: { Authorization: `Bearer ${token}` } }
      )
      setStudents(
        Array.isArray(studRes.data)
          ? studRes.data
          : studRes.data.results || []
      )
    } catch (err) {
      console.error('Load error:', err)
    } finally {
      setLoading(false)
    }
  }

  if (loading)
    return (
      <div className="admin-dashboard">
        <p>Loading...</p>
      </div>
    )

  return (
    <div className="admin-dashboard">
      <h1>Admin Dashboard - Full Control</h1>

      <div className="dashboard-nav">
        <button
          className={`nav-btn ${activeTab === 'overview' ? 'active' : ''}`}
          onClick={() => setActiveTab('overview')}
        >
          Overview
        </button>
        <button
          className={`nav-btn ${activeTab === 'subjects' ? 'active' : ''}`}
          onClick={() => setActiveTab('subjects')}
        >
          Subjects
        </button>
        <button
          className={`nav-btn ${activeTab === 'professors' ? 'active' : ''}`}
          onClick={() => setActiveTab('professors')}
        >
          Professors
        </button>
        <button
          className={`nav-btn ${activeTab === 'students' ? 'active' : ''}`}
          onClick={() => setActiveTab('students')}
        >
          Students
        </button>
      </div>

      {/* OVERVIEW */}
      {activeTab === 'overview' && stats && (
        <div className="stats-grid">
          <div className="stat-card">
            <h3>Total Students</h3>
            <p className="stat-number">{stats.total_students}</p>
          </div>
          <div className="stat-card">
            <h3>Total Professors</h3>
            <p className="stat-number">{stats.total_professors}</p>
          </div>
          <div className="stat-card">
            <h3>Total Subjects</h3>
            <p className="stat-number">{stats.total_subjects}</p>
          </div>
          <div className="stat-card">
            <h3>Total Enrollments</h3>
            <p className="stat-number">{stats.total_enrollments}</p>
          </div>
        </div>
      )}

      {/* SUBJECTS */}
      {activeTab === 'subjects' && (
        <div className="table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>Subject</th>
                <th>Faculty</th>
                <th>Professor</th>
                <th>Credits</th>
                <th>Max Students</th>
              </tr>
            </thead>
            <tbody>
              {subjects.map(s => (
                <tr key={s.id}>
                  <td>{s.name}</td>
                  <td>
                    {faculties.find(f => f.id === s.faculty)?.name || 'N/A'}
                  </td>
                  <td>
                    {s.professor?.user?.username || 'Unassigned'}
                  </td>
                  <td>{s.credits}</td>
                  <td>{s.max_students}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* PROFESSORS */}
      {activeTab === 'professors' && (
        <div className="table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>Username</th>
                <th>Email</th>
                <th>Faculty</th>
                <th>Title</th>
              </tr>
            </thead>
            <tbody>
              {professors.map(p => (
                <tr key={p.id}>
                  <td>{p.user.username}</td>
                  <td>{p.user.email}</td>
                  <td>
                    {faculties.find(f => f.id === p.faculty)?.name || 'N/A'}
                  </td>
                  <td>{p.title || '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {/* STUDENTS */}
      {activeTab === 'students' && (
        <div className="table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th>Username</th>
                <th>Email</th>
                <th>Faculty</th>
                <th>Enrollment #</th>
              </tr>
            </thead>
            <tbody>
              {students.map(s => (
                <tr key={s.id}>
                  <td>{s.user.username}</td>
                  <td>{s.user.email}</td>
                  <td>
                    {faculties.find(f => f.id === s.faculty)?.name || 'N/A'}
                  </td>
                  <td>{s.enrollment_number || '-'}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
