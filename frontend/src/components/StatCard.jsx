import React from 'react'

const StatCard = ({ title, value, icon, color = 'blue', trend = null }) => {
  const colors = {
    blue: {
      bg: 'bg-cyber-blue bg-opacity-10',
      text: 'text-cyber-blue',
      border: 'border-cyber-blue'
    },
    green: {
      bg: 'bg-cyber-green bg-opacity-10',
      text: 'text-cyber-green',
      border: 'border-cyber-green'
    },
    red: {
      bg: 'bg-red-500 bg-opacity-10',
      text: 'text-red-500',
      border: 'border-red-500'
    },
    purple: {
      bg: 'bg-cyber-purple bg-opacity-10',
      text: 'text-cyber-purple',
      border: 'border-cyber-purple'
    }
  }

  const colorScheme = colors[color]

  return (
    <div className={`glass rounded-lg p-6 border-2 ${colorScheme.border} border-opacity-30 hover:border-opacity-100 transition-all duration-300 card-hover`}>
      <div className="flex items-start justify-between">
        <div>
          <p className="text-gray-400 text-sm mb-1">{title}</p>
          <h3 className={`text-3xl font-bold ${colorScheme.text}`}>{value}</h3>
          {trend && (
            <p className={`text-sm mt-2 ${trend > 0 ? 'text-green-400' : 'text-red-400'}`}>
              {trend > 0 ? '↑' : '↓'} {Math.abs(trend)}% from last month
            </p>
          )}
        </div>
        
        <div className={`${colorScheme.bg} ${colorScheme.text} p-3 rounded-lg`}>
          {icon}
        </div>
      </div>
    </div>
  )
}

export default StatCard
