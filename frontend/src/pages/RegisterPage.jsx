import React, { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { useAuth } from '../context/AuthContext'
import CyberBackground from '../components/CyberBackground'
import Button from '../components/Button'
import Input from '../components/Input'
import { FiMail, FiLock, FiUser, FiShield, FiCheck, FiAlertCircle, FiUpload, FiFile } from 'react-icons/fi'

const RegisterPage = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirmPassword: '',
    full_name: '',
    badge_number: '',
    department: ''
  })
  const [proofFile, setProofFile] = useState(null)
  const [proofFileName, setProofFileName] = useState('')
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)
  const [loading, setLoading] = useState(false)
  
  const { register } = useAuth()
  const navigate = useNavigate()

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    })
    setError('')
  }

  const handleFileChange = (e) => {
    const file = e.target.files[0]
    if (file) {
      // Validate file size (max 5MB)
      if (file.size > 5 * 1024 * 1024) {
        setError('Proof document must be less than 5MB')
        return
      }

      // Validate file type
      const allowedTypes = ['image/jpeg', 'image/png', 'image/jpg', 'application/pdf']
      if (!allowedTypes.includes(file.type)) {
        setError('Only PDF, JPG, and PNG files are allowed')
        return
      }

      setProofFileName(file.name)
      
      // Convert to base64
      const reader = new FileReader()
      reader.onloadend = () => {
        setProofFile(reader.result)
      }
      reader.readAsDataURL(file)
      setError('')
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    // Validate passwords match
    if (formData.password !== formData.confirmPassword) {
      setError('Passwords do not match')
      setLoading(false)
      return
    }

    // Validate password strength
    if (formData.password.length < 8) {
      setError('Password must be at least 8 characters')
      setLoading(false)
      return
    }

    const registrationData = {
      email: formData.email,
      password: formData.password,
      full_name: formData.full_name,
      badge_number: formData.badge_number,
      department: formData.department
    }

    // Add proof document if uploaded
    if (proofFile) {
      registrationData.proof_document = proofFile
    }

    const result = await register(registrationData)
    
    if (result.success) {
      setSuccess(true)
      setTimeout(() => {
        navigate('/login')
      }, 3000)
    } else {
      setError(result.error)
    }
    
    setLoading(false)
  }

  if (success) {
    return (
      <div className="min-h-screen relative flex items-center justify-center px-6">
        <CyberBackground />
        
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className="relative z-10 w-full max-w-md"
        >
          <div className="glass rounded-lg p-8 border-2 border-cyber-green border-opacity-50 text-center">
            <div className="w-20 h-20 bg-cyber-green bg-opacity-20 rounded-full flex items-center justify-center mx-auto mb-6">
              <FiCheck className="text-cyber-green" size={40} />
            </div>
            
            <h2 className="text-2xl font-bold text-cyber-green mb-4">
              Registration Successful!
            </h2>
            
            <p className="text-gray-300 mb-6">
              Your account has been created and is pending administrator approval.
              You will be notified once your account is approved.
            </p>
            
            <p className="text-sm text-gray-400 mb-6">
              Redirecting to login page...
            </p>
            
            <Link to="/login">
              <Button variant="success" size="lg" className="w-full">
                Go to Login
              </Button>
            </Link>
          </div>
        </motion.div>
      </div>
    )
  }

  return (
    <div className="min-h-screen relative flex items-center justify-center px-6 py-12">
      <CyberBackground />
      
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
        className="relative z-10 w-full max-w-2xl"
      >
        {/* Logo */}
        <div className="text-center mb-8">
          <FiShield className="text-cyber-blue mx-auto mb-4 animate-pulse" size={60} />
          <h1 className="text-3xl font-bold text-cyber-blue mb-2">Investigator Registration</h1>
          <p className="text-gray-400">Register for forensic investigation access</p>
        </div>

        {/* Registration Form */}
        <div className="glass rounded-lg p-8 border-2 border-cyber-blue border-opacity-30">
          {/* Warning Notice */}
          <div className="bg-yellow-500 bg-opacity-10 border border-yellow-500 rounded-lg p-4 mb-6">
            <p className="text-yellow-500 text-sm flex items-start gap-2">
              <FiAlertCircle className="flex-shrink-0 mt-0.5" size={16} />
              <span>
                This registration is for authorized law enforcement personnel only. 
                Your account will be reviewed and must be approved by an administrator before access is granted.
              </span>
            </p>
          </div>

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

            <div className="grid md:grid-cols-2 gap-6">
              <Input
                label="Full Name"
                type="text"
                name="full_name"
                value={formData.full_name}
                onChange={handleChange}
                placeholder="John Doe"
                icon={<FiUser size={20} />}
                required
              />

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
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              <Input
                label="Badge Number"
                type="text"
                name="badge_number"
                value={formData.badge_number}
                onChange={handleChange}
                placeholder="BADGE-12345"
                icon={<FiShield size={20} />}
                required
              />

              <Input
                label="Department"
                type="text"
                name="department"
                value={formData.department}
                onChange={handleChange}
                placeholder="Cyber Crime Division"
                icon={<FiUser size={20} />}
                required
              />
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              <Input
                label="Password"
                type="password"
                name="password"
                value={formData.password}
                onChange={handleChange}
                placeholder="Min. 8 characters"
                icon={<FiLock size={20} />}
                required
              />

              <Input
                label="Confirm Password"
                type="password"
                name="confirmPassword"
                value={formData.confirmPassword}
                onChange={handleChange}
                placeholder="Re-enter password"
                icon={<FiLock size={20} />}
                required
              />
            </div>

            {/* Proof Document Upload */}
            <div className="space-y-2">
              <label className="block text-sm font-medium text-gray-300">
                Proof of Identity (Optional)
                <span className="text-xs text-gray-500 ml-2">(Badge/ID/Official Document)</span>
              </label>
              <div className="relative">
                <input
                  type="file"
                  id="proof_document"
                  onChange={handleFileChange}
                  accept=".pdf,.jpg,.jpeg,.png"
                  className="hidden"
                />
                <label
                  htmlFor="proof_document"
                  className="flex items-center justify-center gap-3 w-full px-4 py-3 bg-cyber-dark border-2 border-cyber-blue border-opacity-30 rounded-lg cursor-pointer hover:border-cyber-green transition-all duration-300"
                >
                  <FiUpload className="text-cyber-blue" size={20} />
                  <span className="text-gray-300">
                    {proofFileName || 'Upload Proof Document (PDF, JPG, PNG - Max 5MB)'}
                  </span>
                </label>
                {proofFileName && (
                  <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mt-2 flex items-center gap-2 text-sm text-cyber-green"
                  >
                    <FiFile size={16} />
                    <span>{proofFileName}</span>
                  </motion.div>
                )}
              </div>
              <p className="text-xs text-gray-500">
                Uploading proof of identity helps expedite your account approval.
              </p>
            </div>

            <div className="bg-cyber-dark rounded-lg p-4">
              <p className="text-xs text-gray-400 mb-2">Password Requirements:</p>
              <ul className="text-xs text-gray-500 space-y-1">
                <li>• Minimum 8 characters</li>
                <li>• At least one uppercase letter</li>
                <li>• At least one lowercase letter</li>
                <li>• At least one number</li>
                <li>• At least one special character</li>
              </ul>
            </div>

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
                  Registering...
                </>
              ) : (
                <>
                  <FiShield size={20} />
                  Register Account
                </>
              )}
            </Button>
          </form>

          <div className="mt-6 text-center">
            <p className="text-gray-400 text-sm">
              Already have an account?{' '}
              <Link to="/login" className="text-cyber-blue hover:text-cyber-green transition-colors">
                Login here
              </Link>
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

export default RegisterPage
