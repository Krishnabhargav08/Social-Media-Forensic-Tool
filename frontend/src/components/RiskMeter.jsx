import React from 'react'

const RiskMeter = ({ score, size = 'md' }) => {
  // Determine risk level and color
  let riskLevel = 'LOW'
  let riskColor = '#00ff88' // green
  let bgColor = 'rgba(0, 255, 136, 0.2)'

  if (score >= 75) {
    riskLevel = 'CRITICAL'
    riskColor = '#ff0044'
    bgColor = 'rgba(255, 0, 68, 0.2)'
  } else if (score >= 50) {
    riskLevel = 'HIGH'
    riskColor = '#ff6600'
    bgColor = 'rgba(255, 102, 0, 0.2)'
  } else if (score >= 25) {
    riskLevel = 'MEDIUM'
    riskColor = '#ffaa00'
    bgColor = 'rgba(255, 170, 0, 0.2)'
  }

  const sizes = {
    sm: { width: 120, height: 120, strokeWidth: 8 },
    md: { width: 160, height: 160, strokeWidth: 10 },
    lg: { width: 200, height: 200, strokeWidth: 12 }
  }

  const { width, height, strokeWidth } = sizes[size]
  const radius = (width - strokeWidth) / 2
  const circumference = 2 * Math.PI * radius
  const offset = circumference - (score / 100) * circumference

  return (
    <div className="flex flex-col items-center gap-4">
      <div className="relative">
        <svg width={width} height={height} className="transform -rotate-90">
          {/* Background circle */}
          <circle
            cx={width / 2}
            cy={height / 2}
            r={radius}
            fill="none"
            stroke={bgColor}
            strokeWidth={strokeWidth}
          />
          
          {/* Progress circle */}
          <circle
            cx={width / 2}
            cy={height / 2}
            r={radius}
            fill="none"
            stroke={riskColor}
            strokeWidth={strokeWidth}
            strokeDasharray={circumference}
            strokeDashoffset={offset}
            strokeLinecap="round"
            style={{
              transition: 'stroke-dashoffset 1s ease',
              filter: `drop-shadow(0 0 8px ${riskColor})`
            }}
          />
        </svg>
        
        {/* Center text */}
        <div className="absolute inset-0 flex flex-col items-center justify-center">
          <span className="text-4xl font-bold" style={{ color: riskColor }}>
            {score}
          </span>
          <span className="text-sm text-gray-400">/ 100</span>
        </div>
      </div>
      
      <div className="text-center">
        <div 
          className="px-4 py-2 rounded-lg font-bold text-sm"
          style={{ 
            backgroundColor: bgColor,
            color: riskColor,
            boxShadow: `0 0 15px ${bgColor}`
          }}
        >
          {riskLevel} RISK
        </div>
      </div>
    </div>
  )
}

export default RiskMeter
