import React from 'react'
import { motion } from 'framer-motion'

const CyberBackground = () => {
  return (
    <div className="fixed inset-0 overflow-hidden pointer-events-none">
      {/* Grid Background */}
      <div className="absolute inset-0 cyber-bg opacity-30"></div>
      
      {/* Animated Gradient Orbs */}
      <motion.div
        className="absolute w-96 h-96 bg-cyber-blue opacity-10 rounded-full blur-3xl"
        animate={{
          x: [0, 100, 0],
          y: [0, -100, 0],
        }}
        transition={{
          duration: 20,
          repeat: Infinity,
          ease: "easeInOut"
        }}
        style={{ top: '10%', left: '10%' }}
      />
      
      <motion.div
        className="absolute w-96 h-96 bg-cyber-green opacity-10 rounded-full blur-3xl"
        animate={{
          x: [0, -100, 0],
          y: [0, 100, 0],
        }}
        transition={{
          duration: 15,
          repeat: Infinity,
          ease: "easeInOut"
        }}
        style={{ bottom: '10%', right: '10%' }}
      />
      
      {/* Scan Lines Effect */}
      <div className="absolute inset-0 opacity-5">
        <div className="h-full w-full bg-gradient-to-b from-transparent via-cyber-blue to-transparent animate-pulse-slow"></div>
      </div>
    </div>
  )
}

export default CyberBackground
