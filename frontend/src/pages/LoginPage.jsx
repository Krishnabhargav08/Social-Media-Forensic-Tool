import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useAuth } from '../context/AuthContext'
import CyberBackground from '../components/CyberBackground'
import Button from '../components/Button'
import Input from '../components/Input'
import { FiMail, FiLock, FiShield, FiAlertCircle } from 'react-icons/fi'

const LoginPage = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: ''
  })
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  
  const { login } = useAuth()
  const navigate = useNavigate()

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
    setError('')
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    const result = await login(formData.email, formData.password)
    
    if (result.success) {
      // Redirect based on role
      if (result.user.role === 'admin') {
        navigate('/admin/dashboard')
      } else {
        navigate('/investigator/dashboard')
      }
    } else {
      setError(result.error)
    }
    
    setLoading(false)
  }

  return (
    <div className="min-h-screen relative flex items-center justify-center px-6">
      <CyberBackground />
      
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="relative z-10 w-full max-w-md"
      >
        {/* Logo */}
        <div className="text-center mb-8">
          <FiShield className="text-cyber-blue mx-auto mb-4 animate-pulse" size={60} />
          <h1 className="text-3xl font-bold text-cyber-blue mb-2">Official Login</h1>
          <p className="text-gray-400">Social Media Forensic Tool</p>
        </div>

        {/* Login Form */}
        <div className="glass rounded-lg p-8 border-2 border-cyber-blue border-opacity-30">
          <form onSubmit={handleSubmit} className="space-y-6">
            {error && (
              <motion.div
                initial={{ opacity: 0, y: -10 }}
                animate={{ opacity: 1, y: 0 }}
                className="bg-red-500 bg-opacity-10 border border-red-500 rounded-lg p-4 flex items-start gap-3"
              >
                <FiAlertCircle className="text-red-500 flex-shrink-0 mt-0.5" size={20} />
                <p className="text-red-500 text-sm">{error}</p>
              </motion.div>
            )}

            <Input
              label="Email Address"
              type="email"
              name="email"
              value={formData.email}
              onChange={handleChange}
              placeholder="investigator@agency.gov"
              icon={<FiMail size={20} />}
              required
            />

            <Input
              label="Password"
              type="password"
              name="password"
              value={formData.password}
              onChange={handleChange}
              placeholder="Enter your password"
              icon={<FiLock size={20} />}
              required
            />

            <Button
              type="submit"
              variant="primary"
              size="lg"
              className="w-full"
              disabled={loading}
            >
              {loading ? (
                <>
                  <div className="loading w-5 h-5 border-2 border-cyber-dark border-t-transparent rounded-full"></div>
                  Authenticating...
                </>
              ) : (
                <>
                  <FiLock size={20} />
                  Secure Login
                </>
              )}
            </Button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-gray-400 text-sm">
              Don't have an account?{' '}
              <Link to="/register" className="text-cyber-blue hover:text-cyber-green transition-colors">
                Register as Investigator
              </Link>
            </p>
          </div>

          <div className="mt-6 pt-6 border-t border-cyber-blue border-opacity-20">
            <p className="text-xs text-gray-500 text-center">
              🔒 Secure encrypted connection
              <br />
              All access attempts are logged for security
            </p>
          </div>
        </div>

        <div className="mt-6 text-center">
          <Link to="/" className="text-cyber-blue hover:text-cyber-green transition-colors text-sm">
            ← Back to Home
          </Link>
        </div>
      </motion.div>
    </div>
  )
}

export default LoginPage
