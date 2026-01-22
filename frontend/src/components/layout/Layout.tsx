import { useState } from 'react'
import { Outlet, NavLink, useNavigate } from 'react-router-dom'
import {
  Shield,
  LayoutDashboard,
  FileText,
  LogOut,
  User,
  BookOpen,
  HelpCircle,
  Play,
} from 'lucide-react'
import { useAuth } from '../../hooks/useAuth'
import { useOnboarding } from '../onboarding'
import { cn } from '../../lib/utils'
import DemoMode from '../demo/DemoMode'

export default function Layout() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const { resetOnboarding } = useOnboarding()
  const [isDemoOpen, setIsDemoOpen] = useState(false)

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const navItems = [
    { to: '/', icon: LayoutDashboard, label: 'Dashboard' },
    { to: '/documents', icon: FileText, label: 'Documents' },
    { to: '/controls', icon: BookOpen, label: 'SOC 2 Controls' },
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Sidebar */}
      <aside className="fixed inset-y-0 left-0 w-64 bg-white border-r border-gray-200">
        {/* Logo */}
        <div className="flex items-center gap-2 px-6 py-5 border-b border-gray-200">
          <Shield className="h-8 w-8 text-primary-600" />
          <span className="text-xl font-bold text-gray-900">ShieldAgent</span>
        </div>

        {/* Navigation */}
        <nav className="p-4 space-y-1">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === '/'}
              className={({ isActive }) =>
                cn(
                  'flex items-center gap-3 px-4 py-2.5 rounded-lg text-sm font-medium transition-colors',
                  isActive
                    ? 'bg-primary-50 text-primary-700'
                    : 'text-gray-600 hover:bg-gray-100'
                )
              }
            >
              <item.icon className="h-5 w-5" />
              {item.label}
            </NavLink>
          ))}
          
          {/* Demo Mode Button */}
          <button
            onClick={() => setIsDemoOpen(true)}
            className="flex items-center gap-3 w-full px-4 py-2.5 rounded-lg text-sm font-medium text-indigo-600 hover:bg-indigo-50 transition-colors border border-indigo-200 mt-4"
          >
            <Play className="h-5 w-5" />
            Try Demo Mode
          </button>
        </nav>

        {/* User section */}
        <div className="absolute bottom-0 left-0 right-0 p-4 border-t border-gray-200">
          <div className="flex items-center gap-3 px-4 py-2">
            <div className="flex-shrink-0 h-9 w-9 rounded-full bg-primary-100 flex items-center justify-center">
              <User className="h-5 w-5 text-primary-600" />
            </div>
            <div className="flex-1 min-w-0">
              <p className="text-sm font-medium text-gray-900 truncate">
                {user?.full_name || user?.email}
              </p>
              <p className="text-xs text-gray-500 truncate">{user?.email}</p>
            </div>
          </div>
          <button
            onClick={resetOnboarding}
            className="flex items-center gap-3 w-full px-4 py-2.5 mt-2 rounded-lg text-sm font-medium text-gray-600 hover:bg-gray-100 transition-colors"
          >
            <HelpCircle className="h-5 w-5" />
            Show Tutorial
          </button>
          <button
            onClick={handleLogout}
            className="flex items-center gap-3 w-full px-4 py-2.5 mt-1 rounded-lg text-sm font-medium text-gray-600 hover:bg-gray-100 transition-colors"
          >
            <LogOut className="h-5 w-5" />
            Sign out
          </button>
        </div>
      </aside>

      {/* Main content */}
      <main className="pl-64">
        <div className="max-w-7xl mx-auto px-8 py-8">
          <Outlet />
        </div>
      </main>
      
      {/* Demo Mode Modal */}
      <DemoMode isOpen={isDemoOpen} onClose={() => setIsDemoOpen(false)} />
    </div>
  )
}
