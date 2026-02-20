import React from 'react'

const Card = ({ children, className = '', hover = true, glow = false }) => {
  const baseClasses = "glass rounded-lg p-6 transition-all duration-300"
  const hoverClasses = hover ? "card-hover" : ""
  const glowClasses = glow ? "glow-blue" : ""

  return (
    <div className={`${baseClasses} ${hoverClasses} ${glowClasses} ${className}`}>
      {children}
    </div>
  )
}

export default Card
