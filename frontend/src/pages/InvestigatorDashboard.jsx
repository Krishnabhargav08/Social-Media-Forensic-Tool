import React, { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'
import Sidebar from '../components/Sidebar'
import StatCard from '../components/StatCard'
import Card from '../components/Card'
import Button from '../components/Button'
import Input from '../components/Input'
import { FiFolder, FiPlus, FiSearch, FiClock, FiCheck } from 'react-icons/fi'

const InvestigatorDashboard = () => {
  const [cases, setCases] = useState([])
  const [loading, setLoading] = useState(true)
  const [showNewCaseModal, setShowNewCaseModal] = useState(false)
  const [newCase, setNewCase] = useState({
    target_username: '',
    platform: 'twitter',
    description: ''
  })
  const navigate = useNavigate()

  useEffect(() => {
    fetchCases()
  }, [])

  const fetchCases = async () => {
    try {
      const response = await axios.get('/api/cases/')
      setCases(response.data.cases)
    } catch (error) {
      console.error('Failed to fetch cases:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleCreateCase = async (e) => {
    e.preventDefault()
    
    try {
      const response = await axios.post('/api/cases/', newCase)
      alert('Case created successfully!')
      setShowNewCaseModal(false)
      setNewCase({ target_username: '', platform: 'twitter', description: '' })
      fetchCases()
    } catch (error) {
      console.error('Failed to create case:', error)
      alert('Failed to create case: ' + (error.response?.data?.error || 'Unknown error'))
    }
  }

  const activeCases = cases.filter(c => c.status === 'active')
  const completedCases = cases.filter(c => c.status === 'completed')

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
        <div className="mb-8 flex justify-between items-center">
          <div>
            <h1 className="text-4xl font-bold text-cyber-blue mb-2">Investigator Dashboard</h1>
            <p className="text-gray-400">Manage your forensic investigations</p>
          </div>
          
          <Button
            variant="primary"
            size="lg"
            onClick={() => setShowNewCaseModal(true)}
            icon={<FiPlus />}
          >
            New Investigation
          </Button>
        </div>

        {/* Statistics */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
          <StatCard
            title="Total Cases"
            value={cases.length}
            icon={<FiFolder size={24} />}
            color="blue"
          />
          
          <StatCard
            title="Active Cases"
            value={activeCases.length}
            icon={<FiClock size={24} />}
            color="purple"
          />
          
          <StatCard
            title="Completed Cases"
            value={completedCases.length}
            icon={<FiCheck size={24} />}
            color="green"
          />
        </div>

        {/* Cases List */}
        <Card>
          <div className="flex justify-between items-center mb-6">
            <h2 className="text-2xl font-bold text-cyber-green">My Cases</h2>
            <div className="flex gap-3">
              <select className="bg-cyber-dark border-2 border-cyber-blue border-opacity-30 rounded-lg px-4 py-2 text-white focus:outline-none focus:border-cyber-blue">
                <option value="all">All Cases</option>
                <option value="active">Active</option>
                <option value="completed">Completed</option>
              </select>
            </div>
          </div>

          {cases.length === 0 ? (
            <div className="text-center py-12">
              <FiFolder className="mx-auto text-gray-600 mb-4" size={60} />
              <p className="text-gray-400 mb-4">No cases yet</p>
              <Button
                variant="primary"
                onClick={() => setShowNewCaseModal(true)}
                icon={<FiPlus />}
              >
                Create Your First Case
              </Button>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {cases.map((caseItem) => (
                <div
                  key={caseItem._id}
                  onClick={() => navigate(`/case/${caseItem._id}`)}
                  className="bg-cyber-dark rounded-lg p-4 border-2 border-cyber-blue border-opacity-20 hover:border-opacity-100 cursor-pointer transition-all card-hover"
                >
                  <div className="flex justify-between items-start mb-3">
                    <div className="flex-1">
                      <h3 className="text-lg font-semibold text-white mb-1">
                        {caseItem.target_username}
                      </h3>
                      <p className="text-sm text-gray-400 capitalize">{caseItem.platform}</p>
                    </div>
                    
                    <span className={`
                      px-2 py-1 rounded text-xs font-bold
                      ${caseItem.status === 'active' 
                        ? 'bg-purple-500 bg-opacity-20 text-purple-400' 
                        : 'bg-green-500 bg-opacity-20 text-green-400'}
                    `}>
                      {caseItem.status}
                    </span>
                  </div>

                  {caseItem.risk_score > 0 && (
                    <div className="mb-3">
                      <div className="flex justify-between text-xs mb-1">
                        <span className="text-gray-400">Risk Score</span>
                        <span className={`font-bold ${
                          caseItem.risk_score >= 75 ? 'text-red-500' :
                          caseItem.risk_score >= 50 ? 'text-orange-500' :
                          caseItem.risk_score >= 25 ? 'text-yellow-500' :
                          'text-green-500'
                        }`}>
                          {caseItem.risk_score}/100
                        </span>
                      </div>
                      <div className="w-full bg-gray-700 rounded-full h-2">
                        <div
                          className={`h-2 rounded-full ${
                            caseItem.risk_score >= 75 ? 'bg-red-500' :
                            caseItem.risk_score >= 50 ? 'bg-orange-500' :
                            caseItem.risk_score >= 25 ? 'bg-yellow-500' :
                            'bg-green-500'
                          }`}
                          style={{ width: `${caseItem.risk_score}%` }}
                        />
                      </div>
                    </div>
                  )}

                  <div className="text-xs text-gray-500">
                    Created: {new Date(caseItem.created_at).toLocaleDateString()}
                  </div>
                </div>
              ))}
            </div>
          )}
        </Card>
      </div>

      {/* New Case Modal */}
      {showNewCaseModal && (
        <div className="fixed inset-0 bg-black bg-opacity-70 flex items-center justify-center z-50 p-6">
          <div className="glass rounded-lg p-8 max-w-md w-full border-2 border-cyber-blue">
            <h2 className="text-2xl font-bold text-cyber-blue mb-6">New Investigation Case</h2>
            
            <form onSubmit={handleCreateCase} className="space-y-4">
              <Input
                label="Target Username"
                type="text"
                value={newCase.target_username}
                onChange={(e) => setNewCase({ ...newCase, target_username: e.target.value })}
                placeholder="@username"
                icon={<FiSearch />}
                required
              />

              <div>
                <label className="block text-cyber-blue font-medium mb-2">
                  Platform <span className="text-red-500">*</span>
                </label>
                <select
                  value={newCase.platform}
                  onChange={(e) => setNewCase({ ...newCase, platform: e.target.value })}
                  className="w-full bg-cyber-dark border-2 border-cyber-card rounded-lg px-4 py-3 text-white focus:outline-none focus:border-cyber-blue"
                  required
                >
                  <option value="twitter">Twitter</option>
                  <option value="instagram">Instagram</option>
                  <option value="facebook">Facebook</option>
                  <option value="linkedin">LinkedIn</option>
                </select>
              </div>

              <div>
                <label className="block text-cyber-blue font-medium mb-2">
                  Description (Optional)
                </label>
                <textarea
                  value={newCase.description}
                  onChange={(e) => setNewCase({ ...newCase, description: e.target.value })}
                  placeholder="Case details..."
                  className="w-full bg-cyber-dark border-2 border-cyber-card rounded-lg px-4 py-3 text-white focus:outline-none focus:border-cyber-blue resize-none"
                  rows="3"
                />
              </div>

              <div className="flex gap-3 pt-4">
                <Button
                  type="submit"
                  variant="primary"
                  className="flex-1"
                >
                  Create Case
                </Button>
                
                <Button
                  type="button"
                  variant="secondary"
                  onClick={() => setShowNewCaseModal(false)}
                  className="flex-1"
                >
                  Cancel
                </Button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

export default InvestigatorDashboard
