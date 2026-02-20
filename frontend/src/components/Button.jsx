import React from 'react'

const Button = ({ 
  children, 
  onClick, 
  variant = 'primary', 
  size = 'md',
  type = 'button',
  disabled = false,
  className = '',
  icon = null
}) => {
  const baseClasses = "btn-cyber font-semibold rounded-lg transition-all duration-300 flex items-center justify-center gap-2"
  
  const variants = {
    primary: "bg-cyber-blue text-cyber-dark hover:bg-opacity-80 border-2 border-cyber-blue",
    secondary: "bg-transparent text-cyber-blue border-2 border-cyber-blue hover:bg-cyber-blue hover:text-cyber-dark",
    danger: "bg-red-600 text-white hover:bg-red-700 border-2 border-red-600",
    success: "bg-cyber-green text-cyber-dark hover:bg-opacity-80 border-2 border-cyber-green",
  }
  
  const sizes = {
    sm: "px-4 py-2 text-sm",
    md: "px-6 py-3 text-base",
    lg: "px-8 py-4 text-lg"
  }
  
  const disabledClasses = disabled ? "opacity-50 cursor-not-allowed" : "cursor-pointer"

  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled}
      className={`${baseClasses} ${variants[variant]} ${sizes[size]} ${disabledClasses} ${className}`}
    >
      {icon && <span>{icon}</span>}
      {children}
    </button>
  )
}

export default Button
