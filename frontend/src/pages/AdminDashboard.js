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

  useEffect(() => {
    loadDashboardData()
  }, [])

  const loadDashboardData = async () => {
    setLoading(true)
    try {
      const dashRes = await axios.get('/api/university/dashboard/', {
        headers: { Authorization: `Bearer ${token}` }
      })
      setStats(dashRes.data)

      const facRes = await axios.get('/api/university/faculties/', {
        headers: { Authorization: `Bearer ${token}` }
      })
      setFaculties(facRes.data.results || facRes.data)

      const subRes = await axios.get('/api/university/subjects/', {
        headers: { Authorization: `Bearer ${token}` }
      })
      setSubjects(subRes.data.results || subRes.data)

      const profRes = await axios.get('/api/university/professors/', {
        headers: { Authorization: `Bearer ${token}` }
      })
      setProfessors(profRes.data.results || profRes.data)

      const studRes = await axios.get('/api/university/students/', {
        headers: { Authorization: `Bearer ${token}` }
      })
      setStudents(studRes.data.results || studRes.data)
    } catch (err) {
      console.error('Load error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleAddSubject = async (e) => {
    e.preventDefault()
    try {
      const payload = {
        name: formData.name,
        description: formData.description,
        faculty: parseInt(formData.faculty),
        professor_id: formData.professor ? parseInt(formData.professor) : null,
        credits: parseInt(formData.credits) || 3,
        max_students: parseInt(formData.max_students) || 30,
      }

      if (editingId) {
        await axios.patch(`/api/university/subjects/${editingId}/`, payload, {
          headers: { Authorization: `Bearer ${token}` }
        })
        alert('Subject updated')
        setEditingId(null)
      } else {
        await axios.post('/api/university/subjects/', payload, {
          headers: { Authorization: `Bearer ${token}` }
        })
        alert('Subject created')
      }
      setFormData({})
      setShowForm(false)
      loadDashboardData()
    } catch (err) {
      alert('Failed to save subject')
    }
  }

  const handleDeleteSubject = async (id) => {
    if (window.confirm('Delete this subject?')) {
      try {
        await axios.delete(`/api/university/subjects/${id}/`, {
          headers: { Authorization: `Bearer ${token}` }
        })
        alert('Subject deleted')
        loadDashboardData()
      } catch (err) {
        alert('Failed to delete')
      }
    }
  }

  const handleAddProfessor = async (e) => {
    e.preventDefault()
    try {
      const payload = {
        user: {
          username: formData.prof_username,
          email: formData.prof_email,
        },
        title: formData.prof_title || '',
        faculty: formData.prof_faculty ? parseInt(formData.prof_faculty) : null
      }

      // Only include password if provided
      if (formData.prof_password) {
        payload.user.password = formData.prof_password
      }

      if (formData.edit_prof_id) {
        // Edit existing professor
        await axios.patch(`/api/university/professors/${formData.edit_prof_id}/`, payload, {
          headers: { Authorization: `Bearer ${token}` }
        })
        alert('Professor updated successfully')
      } else {
        // Create new professor
        payload.user.password = formData.prof_password // Password required for new
        await axios.post('/api/university/professors/', payload, {
          headers: { Authorization: `Bearer ${token}` }
        })
        alert('Professor created successfully')
      }
      setFormData({})
      setShowForm(false)
      setEditingId(null)
      loadDashboardData()
    } catch (err) {
      console.error('Error:', err.response?.data || err.message)
      alert('Failed to save professor: ' + (err.response?.data?.detail || err.message))
    }
  }

  const handleAddStudent = async (e) => {
    e.preventDefault()
    try {
      const payload = {
        user: {
          username: formData.stu_username,
          email: formData.stu_email,
        },
        enrollment_number: formData.stu_enrollment || '',
        faculty: formData.stu_faculty ? parseInt(formData.stu_faculty) : null
      }

      // Only include password if provided
      if (formData.stu_password) {
        payload.user.password = formData.stu_password
      }

      if (formData.edit_stu_id) {
        // Edit existing student
        await axios.patch(`/api/university/students/${formData.edit_stu_id}/`, payload, {
          headers: { Authorization: `Bearer ${token}` }
        })
        alert('Student updated successfully')
      } else {
        // Create new student
        payload.user.password = formData.stu_password // Password required for new
        await axios.post('/api/university/students/', payload, {
          headers: { Authorization: `Bearer ${token}` }
        })
        alert('Student created successfully')
      }
      setFormData({})
      setShowForm(false)
      setEditingId(null)
      loadDashboardData()
    } catch (err) {
      console.error('Error:', err.response?.data || err.message)
      alert('Failed to save student: ' + (err.response?.data?.detail || err.message))
    }
  }

  const handleAssignCourses = async (e) => {
    e.preventDefault()
    try {
      const selected = formData.assigned_subjects || []
      
      // Update each subject to assign to the professor
      for (const subjectId of selected) {
        const subject = subjects.find(s => s.id === parseInt(subjectId))
        await axios.patch(`/api/university/subjects/${subjectId}/`, {
          ...subject,
          professor_id: parseInt(formData.assign_prof_id)
        }, {
          headers: { Authorization: `Bearer ${token}` }
        })
      }
      
      alert(`${selected.length} course(s) assigned successfully`)
      setFormData({})
      setShowForm(false)
      setEditingId(null)
      loadDashboardData()
    } catch (err) {
      console.error('Error:', err.response?.data || err.message)
      alert('Failed to assign courses: ' + (err.response?.data?.detail || err.message))
    }
  }

  if (loading) return <div className="admin-dashboard"><p>Loading...</p></div>

  return (
    <div className="admin-dashboard">
      <h1>Admin Dashboard - Full Control</h1>
      <div className="dashboard-nav">
        <button className={`nav-btn ${activeTab === 'overview' ? 'active' : ''}`} onClick={() => setActiveTab('overview')}>Overview</button>
        <button className={`nav-btn ${activeTab === 'subjects' ? 'active' : ''}`} onClick={() => setActiveTab('subjects')}>Subjects</button>
        <button className={`nav-btn ${activeTab === 'professors' ? 'active' : ''}`} onClick={() => setActiveTab('professors')}>Professors</button>
        <button className={`nav-btn ${activeTab === 'students' ? 'active' : ''}`} onClick={() => setActiveTab('students')}>Students</button>
      </div>

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

      {activeTab === 'subjects' && (
        <div>
          <button className="btn" onClick={() => {
            setShowForm(!showForm)
            if (editingId) setEditingId(null)
          }} style={{marginBottom:'20px'}}>
            {showForm ? 'Cancel' : 'Add New Subject'}
          </button>

          {showForm && (
            <form onSubmit={handleAddSubject} className="form-card">
              <h3>{editingId ? 'Edit Subject' : 'Create New Subject'}</h3>
              <input placeholder="Subject Name" value={formData.name || ''} onChange={(e) => setFormData({ ...formData, name: e.target.value })} required />
              <textarea placeholder="Description" value={formData.description || ''} onChange={(e) => setFormData({ ...formData, description: e.target.value })} />
              <select value={formData.faculty || ''} onChange={(e) => setFormData({ ...formData, faculty: e.target.value })} required>
                <option value="">Select Faculty</option>
                {faculties.map(f => <option key={f.id} value={f.id}>{f.name}</option>)}
              </select>
              <select value={formData.professor || ''} onChange={(e) => setFormData({ ...formData, professor: e.target.value })}>
                <option value="">Select Professor (Optional)</option>
                {professors.map(p => <option key={p.id} value={p.id}>{p.user.username}</option>)}
              </select>
              <input type="number" placeholder="Credits" value={formData.credits || 3} onChange={(e) => setFormData({ ...formData, credits: e.target.value })} />
              <input type="number" placeholder="Max Students" value={formData.max_students || 30} onChange={(e) => setFormData({ ...formData, max_students: e.target.value })} />
              <button type="submit" className="btn">{editingId ? 'Update' : 'Create'} Subject</button>
            </form>
          )}

          <div className="table-container">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Subject</th>
                  <th>Faculty</th>
                  <th>Professor</th>
                  <th>Credits</th>
                  <th>Max Students</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {subjects.map(s => (
                  <tr key={s.id}>
                    <td>{s.name}</td>
                    <td>{faculties.find(f => f.id === s.faculty)?.name || 'N/A'}</td>
                    <td>{s.professor ? s.professor.user.username : 'Unassigned'}</td>
                    <td>{s.credits}</td>
                    <td>{s.max_students}</td>
                    <td><button className="btn-small" onClick={() => {setFormData(s); setEditingId(s.id); setShowForm(true)}}>Edit</button><button className="btn-small danger" onClick={() => handleDeleteSubject(s.id)}>Delete</button></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {activeTab === 'professors' && (
        <div>
          <button className="btn" onClick={() => {
            setShowForm(!showForm)
            setEditingId(showForm ? null : 'prof')
            setFormData({})
          }} style={{marginBottom:'20px'}}>
            {showForm && editingId === 'prof' ? 'Cancel' : 'Add New Professor'}
          </button>

          {showForm && editingId === 'prof' && (
            <form onSubmit={(e) => handleAddProfessor(e)} className="form-card">
              <h3>{formData.edit_prof_id ? 'Edit Professor' : 'Create New Professor'}</h3>
              <input placeholder="Username" value={formData.prof_username || formData.user?.username || ''} onChange={(e) => setFormData({ ...formData, prof_username: e.target.value })} required={!formData.edit_prof_id} />
              <input type="email" placeholder="Email" value={formData.prof_email || formData.user?.email || ''} onChange={(e) => setFormData({ ...formData, prof_email: e.target.value })} required={!formData.edit_prof_id} />
              <input type="password" placeholder="Password (leave blank to keep existing)" value={formData.prof_password || ''} onChange={(e) => setFormData({ ...formData, prof_password: e.target.value })} />
              <input placeholder="Title" value={formData.prof_title || formData.title || ''} onChange={(e) => setFormData({ ...formData, prof_title: e.target.value })} />
              <select value={formData.prof_faculty || formData.faculty || ''} onChange={(e) => setFormData({ ...formData, prof_faculty: e.target.value })}>
                <option value="">Select Faculty</option>
                {faculties.map(f => <option key={f.id} value={f.id}>{f.name}</option>)}
              </select>
              <button type="submit" className="btn">{formData.edit_prof_id ? 'Update' : 'Create'} Professor</button>
            </form>
          )}

          {showForm && editingId === 'assign' && (
            <form onSubmit={(e) => handleAssignCourses(e)} className="form-card">
              <h3>Assign Courses to Professor</h3>
              <p style={{marginBottom: '10px'}}><strong>Professor:</strong> {professors.find(p => p.id === parseInt(formData.assign_prof_id))?.user.username}</p>
              <select multiple value={formData.assigned_subjects || []} onChange={(e) => {
                const selected = Array.from(e.target.selectedOptions, option => option.value);
                setFormData({ ...formData, assigned_subjects: selected })
              }} style={{minHeight: '150px', padding: '8px', fontSize: '14px'}}>
                <option value="">-- Select Courses (Hold Ctrl/Cmd to select multiple) --</option>
                {subjects.filter(s => s.faculty === professors.find(p => p.id === parseInt(formData.assign_prof_id))?.faculty).map(s => (
                  <option key={s.id} value={s.id}>{s.name}</option>
                ))}
              </select>
              <button type="submit" className="btn">Assign Courses</button>
            </form>
          )}

          <div className="table-container">
            <table className="data-table">
              <thead>
                <tr><th>Username</th><th>Email</th><th>Faculty</th><th>Title</th><th>Courses</th><th>Actions</th></tr>
              </thead>
              <tbody>
                {professors.map(p => (
                  <tr key={p.id}>
                    <td>{p.user.username}</td>
                    <td>{p.user.email}</td>
                    <td>{faculties.find(f => f.id === p.faculty)?.name || 'N/A'}</td>
                    <td>{p.title || '-'}</td>
                    <td>{subjects.filter(s => s.professor?.id === p.id).length}</td>
                    <td>
                      <button className="btn-small" onClick={() => {setFormData({...p, edit_prof_id: p.id}); setEditingId('prof'); setShowForm(true)}}>Edit</button>
                      <button className="btn-small" onClick={() => {setFormData({assign_prof_id: p.id}); setEditingId('assign'); setShowForm(true)}}>Assign Courses</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {activeTab === 'students' && (
        <div>
          <button className="btn" onClick={() => {
            setShowForm(!showForm)
            setEditingId(showForm ? null : 'stu')
            setFormData({})
          }} style={{marginBottom:'20px'}}>
            {showForm && editingId === 'stu' ? 'Cancel' : 'Add New Student'}
          </button>

          {showForm && editingId === 'stu' && (
            <form onSubmit={(e) => handleAddStudent(e)} className="form-card">
              <h3>{formData.edit_stu_id ? 'Edit Student' : 'Create New Student'}</h3>
              <input placeholder="Username" value={formData.stu_username || formData.user?.username || ''} onChange={(e) => setFormData({ ...formData, stu_username: e.target.value })} required={!formData.edit_stu_id} />
              <input type="email" placeholder="Email" value={formData.stu_email || formData.user?.email || ''} onChange={(e) => setFormData({ ...formData, stu_email: e.target.value })} required={!formData.edit_stu_id} />
              <input type="password" placeholder="Password (leave blank to keep existing)" value={formData.stu_password || ''} onChange={(e) => setFormData({ ...formData, stu_password: e.target.value })} />
              <input placeholder="Enrollment Number" value={formData.stu_enrollment || formData.enrollment_number || ''} onChange={(e) => setFormData({ ...formData, stu_enrollment: e.target.value })} />
              <select value={formData.stu_faculty || formData.faculty || ''} onChange={(e) => setFormData({ ...formData, stu_faculty: e.target.value })}>
                <option value="">Select Faculty</option>
                {faculties.map(f => <option key={f.id} value={f.id}>{f.name}</option>)}
              </select>
              <button type="submit" className="btn">{formData.edit_stu_id ? 'Update' : 'Create'} Student</button>
            </form>
          )}

          <div className="table-container">
            <table className="data-table">
              <thead>
                <tr><th>Username</th><th>Email</th><th>Faculty</th><th>Enrollment #</th><th>Actions</th></tr>
              </thead>
              <tbody>
                {students.map(s => (
                  <tr key={s.id}>
                    <td>{s.user.username}</td>
                    <td>{s.user.email}</td>
                    <td>{faculties.find(f => f.id === s.faculty)?.name || 'N/A'}</td>
                    <td>{s.enrollment_number || '-'}</td>
                    <td><button className="btn-small" onClick={() => {setFormData({...s, edit_stu_id: s.id}); setEditingId('stu'); setShowForm(true)}}>Edit</button></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}
