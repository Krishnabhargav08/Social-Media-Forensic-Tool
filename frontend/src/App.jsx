import React from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { AuthProvider, useAuth } from './context/AuthContext'

// Pages
import LandingPage from './pages/LandingPage'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import AdminDashboard from './pages/AdminDashboard'
import InvestigatorDashboard from './pages/InvestigatorDashboard'
import CaseDetails from './pages/CaseDetails'

// Protected Route Component
const ProtectedRoute = ({ children, requiredRole }) => {
  const { user, loading } = useAuth()

  if (loading) {
    return (
      <div className="min-h-screen bg-cyber-darker flex items-center justify-center">
        <div className="loading w-16 h-16 border-4 border-cyber-blue border-t-transparent rounded-full"></div>
      </div>
    )
  }

  if (!user) {
    return <Navigate to="/login" />
  }

  if (requiredRole && user.role !== requiredRole) {
    return <Navigate to="/" />
  }

  return children
}

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App min-h-screen bg-cyber-darker">
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/register" element={<RegisterPage />} />
            
            <Route
              path="/admin/dashboard"
              element={
                <ProtectedRoute requiredRole="admin">
                  <AdminDashboard />
                </ProtectedRoute>
              }
            />
            
            <Route
              path="/investigator/dashboard"
              element={
                <ProtectedRoute requiredRole="investigator">
                  <InvestigatorDashboard />
                </ProtectedRoute>
              }
            />
            
            <Route
              path="/case/:caseId"
              element={
                <ProtectedRoute>
                  <CaseDetails />
                </ProtectedRoute>
              }
            />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  )
}

export default App
