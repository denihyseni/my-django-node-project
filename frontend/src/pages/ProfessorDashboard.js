import React, { useState, useEffect } from 'react'
import axios from 'axios'

export default function ProfessorDashboard() {
  const [data, setData] = useState(null)
  const [courses, setCourses] = useState([])
  const [enrollments, setEnrollments] = useState([])
  const [activeTab, setActiveTab] = useState('courses')
  const [loading, setLoading] = useState(false)
  const [editingEnrollmentId, setEditingEnrollmentId] = useState(null)
  const [grade, setGrade] = useState('')

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
      setData(dashRes.data)

      // Load enrollments for this professor's courses
      const enrollRes = await axios.get('/api/university/enrollments/', {
        headers: { Authorization: `Bearer ${token}` }
      })
      const allEnrollments = enrollRes.data.results || enrollRes.data
      setEnrollments(allEnrollments)
    } catch (err) {
      console.error('Load error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleGradeChange = async (enrollmentId, newGrade) => {
    try {
      await axios.patch(`/api/university/enrollments/${enrollmentId}/`, {
        grade: newGrade
      }, {
        headers: { Authorization: `Bearer ${token}` }
      })
      alert('Grade updated successfully')
      setEditingEnrollmentId(null)
      loadDashboardData()
    } catch (err) {
      console.error('Error updating grade:', err)
      alert('Failed to update grade')
    }
  }

  if (loading) return <div className="admin-dashboard"><p>Loading...</p></div>

  const coursesList = data?.courses || []

  return (
    <div className="admin-dashboard">
      <h1>Professor Dashboard</h1>
      <p className="subtitle">Welcome, {data?.username}!</p>

      <div className="dashboard-nav">
        <button className={`nav-btn ${activeTab === 'courses' ? 'active' : ''}`} onClick={() => setActiveTab('courses')}>
          My Courses ({coursesList.length})
        </button>
        <button className={`nav-btn ${activeTab === 'grades' ? 'active' : ''}`} onClick={() => setActiveTab('grades')}>
          Student Grades
        </button>
      </div>

      {activeTab === 'courses' && (
        <div>
          <h3>Your Courses</h3>
          {coursesList.length === 0 ? (
            <p className="muted">No courses assigned.</p>
          ) : (
            <div className="cards-grid">
              {coursesList.map(course => (
                <div key={course.id} className="course-card">
                  <h4>{course.name}</h4>
                  <p><strong>Credits:</strong> {course.credits}</p>
                  <p><strong>Enrolled Students:</strong> {course.students_count}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {activeTab === 'grades' && (
        <div>
          <h3>Manage Student Grades</h3>
          {enrollments.length === 0 ? (
            <p className="muted">No enrolled students.</p>
          ) : (
            <div className="table-container">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>Student</th>
                    <th>Course</th>
                    <th>Current Grade</th>
                    <th>Score</th>
                    <th>Action</th>
                  </tr>
                </thead>
                <tbody>
                  {enrollments.map(enrollment => (
                    <tr key={enrollment.id}>
                      <td>{enrollment.student_username}</td>
                      <td>{enrollment.subject_name}</td>
                      <td>
                        {editingEnrollmentId === enrollment.id ? (
                          <select value={grade} onChange={(e) => setGrade(e.target.value)}>
                            <option value="">Not Graded</option>
                            <option value="A">A (90-100)</option>
                            <option value="B">B (80-89)</option>
                            <option value="C">C (70-79)</option>
                            <option value="D">D (60-69)</option>
                            <option value="F">F (Below 60)</option>
                          </select>
                        ) : (
                          enrollment.grade || 'Not Graded'
                        )}
                      </td>
                      <td>{enrollment.score || '-'}</td>
                      <td>
                        {editingEnrollmentId === enrollment.id ? (
                          <>
                            <button className="btn-small" onClick={() => handleGradeChange(enrollment.id, grade)}>Save</button>
                            <button className="btn-small" onClick={() => setEditingEnrollmentId(null)}>Cancel</button>
                          </>
                        ) : (
                          <button className="btn-small" onClick={() => {
                            setEditingEnrollmentId(enrollment.id)
                            setGrade(enrollment.grade || '')
                          }}>Edit</button>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
