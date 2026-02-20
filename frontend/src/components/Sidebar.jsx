import React from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { FiHome, FiUsers, FiFolder, FiLogOut, FiShield } from 'react-icons/fi'

const Sidebar = ({ active = 'dashboard' }) => {
  const { user, logout } = useAuth()
  const navigate = useNavigate()

  const handleLogout = () => {
    logout()
    navigate('/')
  }

  const adminMenuItems = [
    { id: 'dashboard', icon: <FiHome size={20} />, label: 'Dashboard', path: '/admin/dashboard' },
    { id: 'users', icon: <FiUsers size={20} />, label: 'User Management', path: '/admin/dashboard' },
    { id: 'cases', icon: <FiFolder size={20} />, label: 'All Cases', path: '/admin/dashboard' },
  ]

  const investigatorMenuItems = [
    { id: 'dashboard', icon: <FiHome size={20} />, label: 'Dashboard', path: '/investigator/dashboard' },
    { id: 'cases', icon: <FiFolder size={20} />, label: 'My Cases', path: '/investigator/dashboard' },
  ]

  const menuItems = user?.role === 'admin' ? adminMenuItems : investigatorMenuItems

  return (
    <div className="w-64 h-screen bg-cyber-card border-r border-cyber-blue border-opacity-30 fixed left-0 top-0 flex flex-col">
      {/* Logo */}
      <div className="p-6 border-b border-cyber-blue border-opacity-30">
        <div className="flex items-center gap-3">
          <FiShield className="text-cyber-blue" size={32} />
          <div>
            <h1 className="text-lg font-bold text-cyber-blue">Forensic Tool</h1>
            <p className="text-xs text-gray-400">{user?.role?.toUpperCase()}</p>
          </div>
        </div>
      </div>

      {/* Menu Items */}
      <nav className="flex-1 p-4 space-y-2">
        {menuItems.map((item) => (
          <Link
            key={item.id}
            to={item.path}
            className={`
              flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-300
              ${active === item.id 
                ? 'bg-cyber-blue text-cyber-dark font-semibold' 
                : 'text-gray-300 hover:bg-cyber-dark hover:text-cyber-blue'}
            `}
          >
            {item.icon}
            <span>{item.label}</span>
          </Link>
        ))}
      </nav>

      {/* User Info & Logout */}
      <div className="p-4 border-t border-cyber-blue border-opacity-30">
        <div className="mb-3 p-3 bg-cyber-dark rounded-lg">
          <p className="text-sm font-medium text-cyber-green">{user?.full_name}</p>
          <p className="text-xs text-gray-400">{user?.email}</p>
          <p className="text-xs text-gray-500 mt-1">Badge: {user?.badge_number}</p>
        </div>
        
        <button
          onClick={handleLogout}
          className="w-full flex items-center gap-3 px-4 py-3 rounded-lg text-red-400 hover:bg-red-900 hover:bg-opacity-20 transition-all duration-300"
        >
          <FiLogOut size={20} />
          <span>Logout</span>
        </button>
      </div>
    </div>
  )
}

export default Sidebar
