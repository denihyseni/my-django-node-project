import React, { useState, useEffect } from 'react'
import axios from 'axios'

export default function StudentDashboard() {
  const [data, setData] = useState(null)
  const [enrollments, setEnrollments] = useState([])
  const [availableCourses, setAvailableCourses] = useState([])
  const [activeTab, setActiveTab] = useState('enrolled')
  const [loading, setLoading] = useState(false)
  const [enrollingId, setEnrollingId] = useState(null)

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
      setEnrollments(dashRes.data.enrollments || [])

      const coursesRes = await axios.get('/api/university/subjects/', {
        headers: { Authorization: `Bearer ${token}` }
      })
      setAvailableCourses(coursesRes.data.results || coursesRes.data)
    } catch (err) {
      console.error('Load error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleEnroll = async (subjectId) => {
    setEnrollingId(subjectId)
    try {
      const studRes = await axios.get('/api/university/students/', {
        headers: { Authorization: `Bearer ${token}` }
      })
      const students = studRes.data.results || studRes.data
      const currentStudent = students.find(
        s => s.user.username === data?.username
      )

      if (!currentStudent) {
        alert('Student profile not found')
        return
      }

      await axios.post(
        '/api/university/enrollments/',
        {
          student: currentStudent.id,
          subject: subjectId
        },
        {
          headers: { Authorization: `Bearer ${token}` }
        }
      )

      alert('Successfully enrolled!')
      loadDashboardData()
    } catch (err) {
      console.error('Enrollment error:', err)
      alert(
        err.response?.data?.detail ||
        'Failed to enroll in course'
      )
    } finally {
      setEnrollingId(null)
    }
  }

  if (loading)
    return <div className="admin-dashboard"><p>Loading...</p></div>

  const enrolledSubjectIds = enrollments.map(e => e.subject?.id)

  return (
    <div className="admin-dashboard">
      <h1>Student Dashboard</h1>
      <p className="subtitle">Welcome, {data?.username}!</p>

      <div className="dashboard-nav">
        <button
          className={`nav-btn ${activeTab === 'enrolled' ? 'active' : ''}`}
          onClick={() => setActiveTab('enrolled')}
        >
          My Enrollments ({enrollments.length})
        </button>
        <button
          className={`nav-btn ${activeTab === 'available' ? 'active' : ''}`}
          onClick={() => setActiveTab('available')}
        >
          Available Courses
        </button>
      </div>

      {activeTab === 'enrolled' && (
        <div>
          <h3>Your Enrolled Courses</h3>
          {enrollments.length === 0 ? (
            <p className="muted">You are not enrolled in any courses.</p>
          ) : (
            <div className="cards-grid">
              {enrollments.map(e => (
                <div key={e.id} className="course-card">
                  <h4>{e.subject?.name}</h4>
                  <p>
                    <strong>Professor:</strong>{' '}
                    {e.subject?.professor
                      ? e.subject.professor.user.username
                      : 'TBD'}
                  </p>
                  <p>
                    <strong>Grade:</strong>{' '}
                    <span style={{ fontWeight: 'bold' }}>
                      {e.grade || 'Not graded'}
                    </span>
                  </p>
                  {e.score !== null && (
                    <p><strong>Score:</strong> {e.score}/100</p>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {activeTab === 'available' && (
        <div>
          <h3>Available Courses</h3>
          <div className="cards-grid">
            {availableCourses.map(course => {
              const isEnrolled = enrolledSubjectIds.includes(course.id)
              return (
                <div key={course.id} className="course-card">
                  <h4>{course.name}</h4>
                  <p className="muted">{course.description}</p>
                  <p><strong>Credits:</strong> {course.credits}</p>
                  <p>
                    <strong>Professor:</strong>{' '}
                    {course.professor
                      ? course.professor.user.username
                      : 'TBD'}
                  </p>
                  <button
                    className="btn"
                    disabled={isEnrolled || enrollingId === course.id}
                    onClick={() => handleEnroll(course.id)}
                  >
                    {enrollingId === course.id
                      ? 'Enrolling...'
                      : isEnrolled
                        ? 'Already Enrolled'
                        : 'Enroll'}
                  </button>
                </div>
              )
            })}
          </div>
        </div>
      )}
    </div>
  )
}
