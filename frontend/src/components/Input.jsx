import React from 'react'

const Input = ({ 
  label, 
  type = 'text', 
  value, 
  onChange, 
  placeholder = '',
  required = false,
  name = '',
  icon = null,
  error = ''
}) => {
  return (
    <div className="w-full">
      {label && (
        <label className="block text-cyber-blue font-medium mb-2">
          {label} {required && <span className="text-red-500">*</span>}
        </label>
      )}
      
      <div className="relative">
        {icon && (
          <div className="absolute left-3 top-1/2 transform -translate-y-1/2 text-cyber-blue">
            {icon}
          </div>
        )}
        
        <input
          type={type}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          required={required}
          name={name}
          className={`
            w-full bg-cyber-dark border-2 rounded-lg px-4 py-3 text-white
            focus:outline-none focus:border-cyber-blue transition-all duration-300
            ${icon ? 'pl-12' : ''}
            ${error ? 'border-red-500' : 'border-cyber-card'}
            placeholder-gray-500
          `}
        />
      </div>
      
      {error && (
        <p className="text-red-500 text-sm mt-1">{error}</p>
      )}
    </div>
  )
}

export default Input
