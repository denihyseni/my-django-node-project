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
      // Load student dashboard data
      const dashRes = await axios.get('/api/university/dashboard/', {
        headers: { Authorization: `Bearer ${token}` }
      })
      setData(dashRes.data)
      setEnrollments(dashRes.data.enrollments || [])

      // Load all available courses
      const coursesRes = await axios.get('/api/university/subjects/', {
        headers: { Authorization: `Bearer ${token}` }
      })
      const allCourses = coursesRes.data.results || coursesRes.data
      setAvailableCourses(allCourses)
    } catch (err) {
      console.error('Load error:', err)
    } finally {
      setLoading(false)
    }
  }

  const handleEnroll = async (subjectId) => {
    setEnrollingId(subjectId)
    try {
      const student = data?.student_id || 1 // Will be fetched properly
      
      // First get the student ID
      const studRes = await axios.get('/api/university/students/', {
        headers: { Authorization: `Bearer ${token}` }
      })
      const students = studRes.data.results || studRes.data
      const currentStudent = students.find(s => s.user.username === data?.username)

      if (!currentStudent) {
        alert('Could not find student profile')
        setEnrollingId(null)
        return
      }

      await axios.post('/api/university/enrollments/', {
        student: currentStudent.id,
        subject: subjectId,
        grade: '',
        score: null
      }, {
        headers: { Authorization: `Bearer ${token}` }
      })

      alert('Successfully enrolled in course!')
      loadDashboardData()
    } catch (err) {
      console.error('Enrollment error:', err)
      if (err.response?.data?.non_field_errors?.[0]?.includes('unique')) {
        alert('You are already enrolled in this course')
      } else {
        alert('Failed to enroll in course')
      }
    } finally {
      setEnrollingId(null)
    }
  }

  if (loading) return <div className="admin-dashboard"><p>Loading...</p></div>

  const enrolledCourseIds = enrollments.map(e => e.id) // Note: will need to adjust based on actual enrollment structure

  return (
    <div className="admin-dashboard">
      <h1>Student Dashboard</h1>
      <p className="subtitle">Welcome, {data?.username}!</p>

      <div className="dashboard-nav">
        <button className={`nav-btn ${activeTab === 'enrolled' ? 'active' : ''}`} onClick={() => setActiveTab('enrolled')}>
          My Enrollments ({enrollments.length})
        </button>
        <button className={`nav-btn ${activeTab === 'available' ? 'active' : ''}`} onClick={() => setActiveTab('available')}>
          Available Courses
        </button>
      </div>

      {activeTab === 'enrolled' && (
        <div>
          <h3>Your Enrolled Courses</h3>
          {enrollments.length === 0 ? (
            <p className="muted">You are not enrolled in any courses yet.</p>
          ) : (
            <div className="cards-grid">
              {enrollments.map(enrollment => (
                <div key={enrollment.id} className="course-card">
                  <h4>{enrollment.subject}</h4>
                  <p><strong>Professor:</strong> {enrollment.professor}</p>
                  <p>
                    <strong>Grade:</strong> <span style={{
                      fontSize: '18px',
                      fontWeight: 'bold',
                      color: enrollment.grade === 'A' ? '#4caf50' : enrollment.grade === 'F' ? '#f44336' : '#ff9800'
                    }}>
                      {enrollment.grade}
                    </span>
                  </p>
                  {enrollment.score && <p><strong>Score:</strong> {enrollment.score}/100</p>}
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {activeTab === 'available' && (
        <div>
          <h3>Available Courses for Enrollment</h3>
          {availableCourses.length === 0 ? (
            <p className="muted">No courses available.</p>
          ) : (
            <div className="cards-grid">
              {availableCourses.map(course => {
                const isEnrolled = enrollments.some(e => e.subject === course.name)
                return (
                  <div key={course.id} className="course-card">
                    <h4>{course.name}</h4>
                    <p className="muted">{course.description}</p>
                    <p><strong>Faculty:</strong> ID {course.faculty}</p>
                    <p><strong>Credits:</strong> {course.credits}</p>
                    <p><strong>Professor:</strong> {course.professor ? course.professor.user.username : 'TBD'}</p>
                    <button
                      className={`btn ${isEnrolled ? 'disabled' : ''}`}
                      onClick={() => handleEnroll(course.id)}
                      disabled={isEnrolled || enrollingId === course.id}
                      style={{ cursor: isEnrolled ? 'not-allowed' : 'pointer' }}
                    >
                      {enrollingId === course.id ? 'Enrolling...' : isEnrolled ? 'Already Enrolled' : 'Enroll Now'}
                    </button>
                  </div>
                )
              })}
            </div>
          )}
        </div>
      )}
    </div>
  )
}
