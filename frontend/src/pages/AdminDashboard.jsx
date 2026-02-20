import React, { useState, useEffect } from 'react'
import axios from 'axios'
import Sidebar from '../components/Sidebar'
import StatCard from '../components/StatCard'
import Card from '../components/Card'
import Button from '../components/Button'
import { FiUsers, FiFolder, FiAlertTriangle, FiCheck, FiX, FiClock, FiFileText, FiEye } from 'react-icons/fi'

const AdminDashboard = () => {
  const [stats, setStats] = useState(null)
  const [pendingUsers, setPendingUsers] = useState([])
  const [highRiskCases, setHighRiskCases] = useState([])
  const [loading, setLoading] = useState(true)
  const [viewingProof, setViewingProof] = useState(null)

  useEffect(() => {
    fetchDashboardData()
  }, [])

  const fetchDashboardData = async () => {
    try {
      const [statsRes, usersRes, casesRes] = await Promise.all([
        axios.get('/api/admin/statistics'),
        axios.get('/api/admin/pending-users'),
        axios.get('/api/admin/high-risk-cases')
      ])

      setStats(statsRes.data)
      setPendingUsers(usersRes.data.users)
      setHighRiskCases(casesRes.data.cases)
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleApproveUser = async (userId) => {
    try {
      await axios.post(`/api/admin/approve-user/${userId}`)
      fetchDashboardData() // Refresh data
    } catch (error) {
      console.error('Failed to approve user:', error)
      alert('Failed to approve user')
    }
  }

  const handleRejectUser = async (userId) => {
    try {
      await axios.post(`/api/admin/reject-user/${userId}`)
      fetchDashboardData() // Refresh data
    } catch (error) {
      console.error('Failed to reject user:', error)
      alert('Failed to reject user')
    }
  }

  if (loading) {
    return (
      <div className="flex">
        <Sidebar active="dashboard" />
        <div className="ml-64 flex-1 p-8 flex items-center justify-center">
          <div className="loading w-16 h-16 border-4 border-cyber-blue border-t-transparent rounded-full"></div>
        </div>
      </div>
    )
  }

  return (
    <div className="flex min-h-screen bg-cyber-darker cyber-bg">
      <Sidebar active="dashboard" />
      
      <div className="ml-64 flex-1 p-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-cyber-blue mb-2">Admin Dashboard</h1>
          <p className="text-gray-400">System monitoring and user management</p>
        </div>

        {/* Statistics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard
            title="Total Users"
            value={stats?.total_users || 0}
            icon={<FiUsers size={24} />}
            color="blue"
          />
          
          <StatCard
            title="Pending Approvals"
            value={stats?.pending_users || 0}
            icon={<FiClock size={24} />}
            color="purple"
          />
          
          <StatCard
            title="Active Cases"
            value={stats?.active_cases || 0}
            icon={<FiFolder size={24} />}
            color="green"
          />
          
          <StatCard
            title="High Risk Cases"
            value={stats?.high_risk_cases || 0}
            icon={<FiAlertTriangle size={24} />}
            color="red"
          />
        </div>

        {/* Pending User Approvals */}
        <Card className="mb-8">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-cyber-green">Pending User Approvals</h2>
            <span className="bg-cyber-blue bg-opacity-20 text-cyber-blue px-3 py-1 rounded-full text-sm font-semibold">
              {pendingUsers.length} Pending
            </span>
          </div>

          {pendingUsers.length === 0 ? (
            <p className="text-gray-400 text-center py-8">No pending user approvals</p>
          ) : (
            <div className="space-y-4">
              {pendingUsers.map((user) => (
                <div
                  key={user._id}
                  className="bg-cyber-dark rounded-lg p-4 border border-cyber-blue border-opacity-20 hover:border-opacity-50 transition-all"
                >
                  <div className="flex items-start justify-between">
                    <div className="flex-1">
                      <h3 className="text-lg font-semibold text-white">{user.full_name}</h3>
                      <p className="text-sm text-gray-400">{user.email}</p>
                      <div className="flex gap-4 mt-2 flex-wrap">
                        <span className="text-xs text-gray-500">Badge: {user.badge_number}</span>
                        <span className="text-xs text-gray-500">Dept: {user.department}</span>
                        <span className="text-xs text-gray-500">
                          Registered: {new Date(user.created_at).toLocaleDateString()}
                        </span>
                        {user.has_proof && (
                          <span className="text-xs text-cyber-green flex items-center gap-1">
                            <FiFileText size={12} /> Proof Submitted
                          </span>
                        )}
                      </div>
                    </div>
                    
                    <div className="flex gap-3 ml-4">
                      {user.has_proof && (
                        <Button
                          variant="secondary"
                          size="sm"
                          onClick={() => setViewingProof(user)}
                          icon={<FiEye />}
                        >
                          View Proof
                        </Button>
                      )}
                      
                      <Button
                        variant="success"
                        size="sm"
                        onClick={() => handleApproveUser(user._id)}
                        icon={<FiCheck />}
                      >
                        Approve
                      </Button>
                      
                      <Button
                        variant="danger"
                        size="sm"
                        onClick={() => handleRejectUser(user._id)}
                        icon={<FiX />}
                      >
                        Reject
                      </Button>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </Card>

        {/* High Risk Cases */}
        <Card className="glow-red">
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-red-500">High Risk Cases Alert</h2>
            <FiAlertTriangle className="text-red-500 animate-pulse" size={24} />
          </div>

          {highRiskCases.length === 0 ? (
            <p className="text-gray-400 text-center py-8">No high-risk cases detected</p>
          ) : (
            <div className="space-y-4">
              {highRiskCases.map((caseItem) => (
                <div
                  key={caseItem._id}
                  className="bg-red-900 bg-opacity-10 border border-red-500 border-opacity-30 rounded-lg p-4"
                >
                  <div className="flex justify-between items-start">
                    <div>
                      <h3 className="text-lg font-semibold text-white">
                        Target: {caseItem.target_username}
                      </h3>
                      <p className="text-sm text-gray-400">Platform: {caseItem.platform}</p>
                      <p className="text-sm text-gray-400 mt-1">
                        Case ID: <span className="font-mono text-xs">{caseItem._id}</span>
                      </p>
                    </div>
                    
                    <div className="text-right">
                      <div className={`
                        px-3 py-1 rounded-full text-sm font-bold
                        ${caseItem.risk_level === 'critical' 
                          ? 'bg-red-500 text-white' 
                          : 'bg-orange-500 text-white'}
                      `}>
                        {caseItem.risk_level?.toUpperCase()}
                      </div>
                      <p className="text-lg font-bold text-red-500 mt-2">
                        Risk: {caseItem.risk_score}/100
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </Card>
      </div>

      {/* Proof Document Modal */}
      {viewingProof && (
        <div 
          className="fixed inset-0 bg-black bg-opacity-80 flex items-center justify-center z-50 p-4"
          onClick={() => setViewingProof(null)}
        >
          <div 
            className="glass rounded-lg p-6 max-w-4xl w-full max-h-[90vh] overflow-auto border-2 border-cyber-blue"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex justify-between items-center mb-4">
              <div>
                <h3 className="text-2xl font-bold text-cyber-green">Proof Document</h3>
                <p className="text-gray-400 text-sm">{viewingProof.full_name} - {viewingProof.email}</p>
              </div>
              <button 
                onClick={() => setViewingProof(null)}
                className="text-gray-400 hover:text-white transition-colors"
              >
                <FiX size={24} />
              </button>
            </div>
            
            <div className="bg-cyber-darker rounded-lg p-4 mb-4">
              <div className="grid grid-cols-2 gap-4 text-sm">
                <div>
                  <span className="text-gray-500">Badge Number:</span>
                  <span className="text-white ml-2">{viewingProof.badge_number}</span>
                </div>
                <div>
                  <span className="text-gray-500">Department:</span>
                  <span className="text-white ml-2">{viewingProof.department}</span>
                </div>
              </div>
            </div>

            {viewingProof.proof_document ? (
              <div className="bg-white rounded-lg p-4">
                <img 
                  src={viewingProof.proof_document} 
                  alt="Proof Document" 
                  className="w-full h-auto rounded"
                />
              </div>
            ) : (
              <p className="text-gray-400 text-center py-8">No proof document available</p>
            )}

            <div className="flex justify-end gap-3 mt-6">
              <Button
                variant="danger"
                onClick={() => {
                  handleRejectUser(viewingProof._id)
                  setViewingProof(null)
                }}
                icon={<FiX />}
              >
                Reject
              </Button>
              <Button
                variant="success"
                onClick={() => {
                  handleApproveUser(viewingProof._id)
                  setViewingProof(null)
                }}
                icon={<FiCheck />}
              >
                Approve
              </Button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default AdminDashboard
