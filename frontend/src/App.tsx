import { Routes, Route, Navigate } from 'react-router-dom'
import { useAuth } from './hooks/useAuth'
import Layout from './components/layout/Layout'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import DashboardPage from './pages/DashboardPage'
import DocumentsPage from './pages/DocumentsPage'
import JobDetailsPage from './pages/JobDetailsPage'
import ControlsPage from './pages/ControlsPage'
import AnalysisPage from './pages/AnalysisPage'
import { OnboardingModal, useOnboarding } from './components/onboarding'

function App() {
  const { isAuthenticated, isLoading } = useAuth()
  const { showOnboarding, completeOnboarding, closeOnboarding } = useOnboarding()

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <>
      {/* Onboarding Modal - shows on first visit */}
      {isAuthenticated && (
        <OnboardingModal 
          isOpen={showOnboarding} 
          onClose={closeOnboarding}
          onComplete={completeOnboarding}
        />
      )}

      <Routes>
        {/* Public routes */}
        <Route
          path="/login"
          element={isAuthenticated ? <Navigate to="/" replace /> : <LoginPage />}
        />
        <Route
          path="/register"
          element={isAuthenticated ? <Navigate to="/" replace /> : <RegisterPage />}
        />

        {/* Protected routes */}
        <Route
          path="/"
          element={isAuthenticated ? <Layout /> : <Navigate to="/login" replace />}
        >
          <Route index element={<DashboardPage />} />
          <Route path="documents" element={<DocumentsPage />} />
          <Route path="controls" element={<ControlsPage />} />
          <Route path="jobs/:jobId" element={<JobDetailsPage />} />
          <Route path="analysis/:jobId" element={<AnalysisPage />} />
        </Route>

        {/* Catch all */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </>
  )
}

export default App
