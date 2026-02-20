import React from 'react'
import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import CyberBackground from '../components/CyberBackground'
import Button from '../components/Button'
import { FiShield, FiLock, FiSearch, FiFileText } from 'react-icons/fi'

const LandingPage = () => {
  return (
    <div className="min-h-screen relative overflow-hidden">
      <CyberBackground />
      
      <div className="relative z-10">
        {/* Hero Section */}
        <div className="container mx-auto px-6 py-20">
          <motion.div
            initial={{ opacity: 0, y: -50 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center mb-20"
          >
            <div className="flex justify-center mb-6">
              <FiShield className="text-cyber-blue animate-pulse" size={80} />
            </div>
            
            <h1 className="text-6xl font-bold mb-6 bg-gradient-to-r from-cyber-blue via-cyber-green to-cyber-purple bg-clip-text text-transparent">
              Social Media Forensic Tool
            </h1>
            
            <p className="text-xl text-gray-300 mb-8 max-w-3xl mx-auto">
              Advanced Digital Investigation Platform for Law Enforcement
            </p>
            
            <p className="text-gray-400 mb-12 max-w-2xl mx-auto">
              Secure forensic investigation web application for verified officials to collect, analyze, 
              and preserve digital evidence from social media platforms.
            </p>
            
            <div className="flex gap-4 justify-center">
              <Link to="/login">
                <Button variant="primary" size="lg">
                  <FiLock size={20} />
                  Official Login
                </Button>
              </Link>
              
              <Link to="/register">
                <Button variant="secondary" size="lg">
                  Register as Investigator
                </Button>
              </Link>
            </div>
          </motion.div>

          {/* Features Grid */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.4, duration: 0.8 }}
            className="grid md:grid-cols-2 lg:grid-cols-4 gap-6 mb-20"
          >
            <FeatureCard
              icon={<FiSearch size={40} />}
              title="Data Collection"
              description="Automated scraping of publicly available social media data"
              delay={0.5}
            />
            
            <FeatureCard
              icon={<FiShield size={40} />}
              title="AI Analysis"
              description="Advanced sentiment analysis and threat detection"
              delay={0.6}
            />
            
            <FeatureCard
              icon={<FiLock size={40} />}
              title="Encrypted Reports"
              description="Password-protected PDF reports with SHA-256 integrity"
              delay={0.7}
            />
            
            <FeatureCard
              icon={<FiFileText size={40} />}
              title="Evidence Preservation"
              description="Cryptographic hash verification for legal compliance"
              delay={0.8}
            />
          </motion.div>

          {/* Security Notice */}
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 1, duration: 0.8 }}
            className="glass rounded-lg p-8 max-w-4xl mx-auto border-2 border-yellow-500 border-opacity-30"
          >
            <h3 className="text-2xl font-bold text-yellow-500 mb-4 flex items-center gap-3">
              <FiShield size={30} />
              Security Notice
            </h3>
            
            <div className="text-gray-300 space-y-2">
              <p>• This platform is restricted to authorized law enforcement personnel only</p>
              <p>• All access attempts are logged and monitored</p>
              <p>• New registrations require administrator approval</p>
              <p>• Unauthorized access is subject to legal prosecution</p>
            </div>
          </motion.div>
        </div>
      </div>
    </div>
  )
}

const FeatureCard = ({ icon, title, description, delay }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 50 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay, duration: 0.6 }}
      className="glass rounded-lg p-6 text-center card-hover"
    >
      <div className="text-cyber-blue mb-4 flex justify-center">
        {icon}
      </div>
      <h3 className="text-xl font-bold text-cyber-green mb-2">{title}</h3>
      <p className="text-gray-400 text-sm">{description}</p>
    </motion.div>
  )
}

export default LandingPage
