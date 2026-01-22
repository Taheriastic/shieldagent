import { useState, useEffect, useCallback } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import {
  ArrowLeft,
  Loader2,
  CheckCircle,
  XCircle,
  Clock,
  RefreshCw,
} from 'lucide-react'
import { Button, Card, CardContent, Badge, Progress } from '../components/ui'
import { AnalysisDashboard } from '../components/dashboard'
import { api, getErrorMessage } from '../lib/axios'

interface JobStatus {
  id: string
  status: 'PENDING' | 'RUNNING' | 'SUCCEEDED' | 'FAILED'
  framework: string
  created_at: string
  updated_at: string
  progress?: number
  current_step?: string
  error_message?: string
}

interface ControlResult {
  control_id: string
  status: string
  summary?: string
  confidence?: number
  category?: string
  title?: string
  evidence_quote?: string
  gaps?: string[]
}

interface CategoryResult {
  name: string
  count: number
}

interface AnalysisResult {
  job_id: string
  total_controls: number
  passing: number
  failing: number
  needs_review: number
  controls: ControlResult[]
  categories: CategoryResult[]
}

export default function AnalysisPage() {
  const { jobId } = useParams()
  const navigate = useNavigate()
  const [job, setJob] = useState<JobStatus | null>(null)
  const [results, setResults] = useState<AnalysisResult | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState('')

  const loadJob = useCallback(async () => {
    try {
      const response = await api.get(`/jobs/${jobId}`)
      setJob(response.data)
      setError('')
    } catch (err) {
      setError(getErrorMessage(err))
    } finally {
      setIsLoading(false)
    }
  }, [jobId])

  const loadResults = useCallback(async () => {
    try {
      const response = await api.get(`/jobs/${jobId}/evidence`)
      // Transform to dashboard format
      setResults({
        job_id: jobId!,
        total_controls: response.data.total,
        passing: response.data.passing,
        failing: response.data.failing,
        needs_review: response.data.needs_review,
        controls: response.data.evidence || [],
        categories: [],
      })
    } catch (err) {
      console.error('Failed to load results:', err)
    }
  }, [jobId])

  useEffect(() => {
    if (jobId) {
      loadJob()
    }
  }, [jobId, loadJob])

  useEffect(() => {
    // Poll for job status while running
    if (job && (job.status === 'PENDING' || job.status === 'RUNNING')) {
      const interval = setInterval(loadJob, 2000)
      return () => clearInterval(interval)
    }
  }, [job, loadJob])

  useEffect(() => {
    // Load results when job succeeds
    if (job?.status === 'SUCCEEDED') {
      loadResults()
    }
  }, [job?.status, loadResults])

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'SUCCEEDED':
        return <CheckCircle className="h-8 w-8 text-green-500" />
      case 'FAILED':
        return <XCircle className="h-8 w-8 text-red-500" />
      case 'RUNNING':
        return <Loader2 className="h-8 w-8 text-blue-500 animate-spin" />
      default:
        return <Clock className="h-8 w-8 text-gray-400" />
    }
  }

  const getStatusText = (status: string) => {
    switch (status) {
      case 'SUCCEEDED':
        return 'Analysis Complete'
      case 'FAILED':
        return 'Analysis Failed'
      case 'RUNNING':
        return 'Analyzing Documents...'
      default:
        return 'Waiting to Start'
    }
  }

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-[400px]">
        <Loader2 className="h-8 w-8 animate-spin text-primary-600" />
      </div>
    )
  }

  if (error) {
    return (
      <div className="p-6 text-center">
        <XCircle className="h-12 w-12 text-red-500 mx-auto mb-4" />
        <h2 className="text-lg font-medium text-gray-900 mb-2">Error Loading Analysis</h2>
        <p className="text-gray-500 mb-4">{error}</p>
        <Button onClick={() => navigate('/')}>
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Dashboard
        </Button>
      </div>
    )
  }

  // Show loading state while job is running
  if (job && (job.status === 'PENDING' || job.status === 'RUNNING')) {
    return (
      <div className="space-y-6">
        <Button variant="ghost" onClick={() => navigate('/')}>
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Dashboard
        </Button>

        <Card>
          <CardContent className="py-12 text-center">
            {getStatusIcon(job.status)}
            <h2 className="text-xl font-medium text-gray-900 mt-4 mb-2">
              {getStatusText(job.status)}
            </h2>
            <p className="text-gray-500 mb-6">
              {job.current_step || 'Preparing analysis...'}
            </p>
            
            {job.progress !== undefined && (
              <div className="max-w-md mx-auto">
                <Progress value={job.progress} className="h-2" />
                <p className="text-sm text-gray-500 mt-2">{job.progress}% complete</p>
              </div>
            )}

            <div className="mt-8 p-4 bg-gray-50 rounded-lg max-w-md mx-auto">
              <div className="flex items-center justify-between text-sm">
                <span className="text-gray-500">Framework:</span>
                <Badge>{job.framework}</Badge>
              </div>
              <div className="flex items-center justify-between text-sm mt-2">
                <span className="text-gray-500">Started:</span>
                <span className="text-gray-900">
                  {new Date(job.created_at).toLocaleTimeString()}
                </span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    )
  }

  // Show error state
  if (job?.status === 'FAILED') {
    return (
      <div className="space-y-6">
        <Button variant="ghost" onClick={() => navigate('/')}>
          <ArrowLeft className="h-4 w-4 mr-2" />
          Back to Dashboard
        </Button>

        <Card className="border-red-200 bg-red-50">
          <CardContent className="py-12 text-center">
            <XCircle className="h-12 w-12 text-red-500 mx-auto" />
            <h2 className="text-xl font-medium text-red-900 mt-4 mb-2">
              Analysis Failed
            </h2>
            <p className="text-red-700 mb-6">
              {job.error_message || 'An error occurred during analysis'}
            </p>
            <Button onClick={() => navigate('/documents')}>
              <RefreshCw className="h-4 w-4 mr-2" />
              Try Again
            </Button>
          </CardContent>
        </Card>
      </div>
    )
  }

  // Show results
  return (
    <div className="space-y-6">
      <Button variant="ghost" onClick={() => navigate('/')}>
        <ArrowLeft className="h-4 w-4 mr-2" />
        Back to Dashboard
      </Button>

      {results ? (
        <AnalysisDashboard 
          results={{
            job_id: results.job_id,
            created_at: job?.created_at || new Date().toISOString(),
            scan_type: 'quick',
            total_controls: results.total_controls,
            passing: results.passing,
            failing: results.failing,
            needs_review: results.needs_review,
            controls: results.controls.map(e => ({
              control_id: e.control_id,
              category: e.category || 'General',
              title: e.title || e.control_id,
              status: (e.status === 'pass' || e.status === 'fail' || e.status === 'needs_review') 
                ? e.status 
                : 'needs_review',
              confidence: e.confidence || 0.5,
              summary: e.summary || '',
              evidence_quote: e.evidence_quote,
              gaps: e.gaps || [],
            })),
            categories: [],
          }}
          onRunAnalysis={() => navigate('/documents')}
        />
      ) : (
        <div className="text-center py-12">
          <Loader2 className="h-8 w-8 animate-spin text-primary-600 mx-auto" />
          <p className="text-gray-500 mt-4">Loading results...</p>
        </div>
      )}
    </div>
  )
}
