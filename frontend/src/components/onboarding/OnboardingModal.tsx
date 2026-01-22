import { useState, useEffect } from 'react'
import { 
  Shield, 
  Zap, 
  CheckCircle, 
  ChevronRight, 
  ChevronLeft,
  Upload,
  BarChart3,
  Sparkles,
  X
} from 'lucide-react'
import { Button } from '../ui'

interface OnboardingStep {
  id: number
  title: string
  description: string
  icon: React.ReactNode
  image?: string
  features?: string[]
}

const steps: OnboardingStep[] = [
  {
    id: 1,
    title: 'Welcome to ShieldAgent',
    description: 'Your AI-powered SOC 2 compliance automation platform. Streamline your compliance journey with intelligent document analysis.',
    icon: <Shield className="h-12 w-12 text-primary-600" />,
    features: [
      'Automated evidence collection',
      'AI-powered document analysis',
      'Real-time compliance scoring',
      'Gap identification & remediation'
    ]
  },
  {
    id: 2,
    title: 'Upload Your Documents',
    description: 'Start by uploading your security policies, procedures, and compliance documents. We support PDF, CSV, JSON, and text files.',
    icon: <Upload className="h-12 w-12 text-blue-600" />,
    features: [
      'Security policies & procedures',
      'Access control lists (CSV)',
      'System configurations (JSON)',
      'Audit logs & reports'
    ]
  },
  {
    id: 3,
    title: 'AI-Powered Analysis',
    description: 'Our Gemini AI analyzes your documents against SOC 2 Trust Service Criteria, identifying evidence and gaps automatically.',
    icon: <Sparkles className="h-12 w-12 text-purple-600" />,
    features: [
      '50+ SOC 2 controls covered',
      '5 Trust Service Categories',
      'Intelligent pattern recognition',
      'Context-aware analysis'
    ]
  },
  {
    id: 4,
    title: 'Review Your Results',
    description: 'Get a comprehensive compliance dashboard showing your score, evidence found, and actionable recommendations.',
    icon: <BarChart3 className="h-12 w-12 text-green-600" />,
    features: [
      'Compliance score by category',
      'Evidence mapping to controls',
      'Gap analysis with severity',
      'Remediation suggestions'
    ]
  },
  {
    id: 5,
    title: 'Ready to Start!',
    description: 'You\'re all set to begin your compliance journey. Upload your first document and run your initial analysis.',
    icon: <CheckCircle className="h-12 w-12 text-green-600" />,
    features: [
      'Quick scan: 8 key controls (~2 min)',
      'Full scan: 50+ controls (~10 min)',
      'Export reports as PDF',
      'Track progress over time'
    ]
  }
]

interface OnboardingModalProps {
  isOpen: boolean
  onClose: () => void
  onComplete: () => void
}

export default function OnboardingModal({ isOpen, onComplete }: OnboardingModalProps) {
  const [currentStep, setCurrentStep] = useState(0)
  const [isAnimating, setIsAnimating] = useState(false)

  useEffect(() => {
    if (isOpen) {
      setCurrentStep(0)
    }
  }, [isOpen])

  if (!isOpen) return null

  const step = steps[currentStep]
  const isFirstStep = currentStep === 0
  const isLastStep = currentStep === steps.length - 1

  const goToNext = () => {
    if (isLastStep) {
      onComplete()
      return
    }
    setIsAnimating(true)
    setTimeout(() => {
      setCurrentStep(prev => prev + 1)
      setIsAnimating(false)
    }, 150)
  }

  const goToPrev = () => {
    if (isFirstStep) return
    setIsAnimating(true)
    setTimeout(() => {
      setCurrentStep(prev => prev - 1)
      setIsAnimating(false)
    }, 150)
  }

  const skipOnboarding = () => {
    onComplete()
  }

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center">
      {/* Backdrop */}
      <div 
        className="absolute inset-0 bg-gray-900/80 backdrop-blur-sm"
        onClick={skipOnboarding}
      />
      
      {/* Modal */}
      <div className="relative bg-white rounded-2xl shadow-2xl w-full max-w-2xl mx-4 overflow-hidden">
        {/* Close button */}
        <button
          onClick={skipOnboarding}
          className="absolute top-4 right-4 p-2 text-gray-400 hover:text-gray-600 z-10"
        >
          <X className="h-5 w-5" />
        </button>

        {/* Progress bar */}
        <div className="absolute top-0 left-0 right-0 h-1 bg-gray-100">
          <div 
            className="h-full bg-primary-600 transition-all duration-300"
            style={{ width: `${((currentStep + 1) / steps.length) * 100}%` }}
          />
        </div>

        {/* Content */}
        <div className={`p-8 pt-12 transition-opacity duration-150 ${isAnimating ? 'opacity-0' : 'opacity-100'}`}>
          {/* Icon */}
          <div className="flex justify-center mb-6">
            <div className="p-4 bg-gray-50 rounded-full">
              {step.icon}
            </div>
          </div>

          {/* Title */}
          <h2 className="text-2xl font-bold text-gray-900 text-center mb-3">
            {step.title}
          </h2>

          {/* Description */}
          <p className="text-gray-600 text-center mb-8 max-w-md mx-auto">
            {step.description}
          </p>

          {/* Features */}
          {step.features && (
            <div className="bg-gray-50 rounded-xl p-6 mb-8">
              <ul className="grid grid-cols-1 md:grid-cols-2 gap-3">
                {step.features.map((feature, index) => (
                  <li key={index} className="flex items-center gap-2 text-sm text-gray-700">
                    <CheckCircle className="h-4 w-4 text-green-500 flex-shrink-0" />
                    {feature}
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Step indicators */}
          <div className="flex justify-center gap-2 mb-8">
            {steps.map((_, index) => (
              <button
                key={index}
                onClick={() => setCurrentStep(index)}
                className={`h-2 rounded-full transition-all duration-300 ${
                  index === currentStep 
                    ? 'w-8 bg-primary-600' 
                    : 'w-2 bg-gray-300 hover:bg-gray-400'
                }`}
              />
            ))}
          </div>

          {/* Navigation buttons */}
          <div className="flex justify-between">
            <Button
              variant="ghost"
              onClick={goToPrev}
              disabled={isFirstStep}
              className={isFirstStep ? 'invisible' : ''}
            >
              <ChevronLeft className="h-4 w-4 mr-1" />
              Back
            </Button>

            <Button onClick={goToNext} size="lg">
              {isLastStep ? (
                <>
                  Get Started
                  <Zap className="h-4 w-4 ml-2" />
                </>
              ) : (
                <>
                  Next
                  <ChevronRight className="h-4 w-4 ml-1" />
                </>
              )}
            </Button>
          </div>
        </div>

        {/* Skip button */}
        {!isLastStep && (
          <div className="pb-6 text-center">
            <button
              onClick={skipOnboarding}
              className="text-sm text-gray-400 hover:text-gray-600"
            >
              Skip tutorial
            </button>
          </div>
        )}
      </div>
    </div>
  )
}


// Hook to manage onboarding state
export function useOnboarding() {
  const STORAGE_KEY = 'shieldagent_onboarding_complete'
  
  const [showOnboarding, setShowOnboarding] = useState(false)
  const [hasCompleted, setHasCompleted] = useState(true)

  useEffect(() => {
    const completed = localStorage.getItem(STORAGE_KEY)
    if (!completed) {
      setShowOnboarding(true)
      setHasCompleted(false)
    }
  }, [])

  const completeOnboarding = () => {
    localStorage.setItem(STORAGE_KEY, 'true')
    setShowOnboarding(false)
    setHasCompleted(true)
  }

  const resetOnboarding = () => {
    localStorage.removeItem(STORAGE_KEY)
    setShowOnboarding(true)
    setHasCompleted(false)
  }

  return {
    showOnboarding,
    hasCompleted,
    completeOnboarding,
    resetOnboarding,
    closeOnboarding: () => setShowOnboarding(false),
  }
}
