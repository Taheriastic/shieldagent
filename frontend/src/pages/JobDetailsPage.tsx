import { useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import {
  ArrowLeft,
  Loader2,
  CheckCircle,
  XCircle,
  Clock,
  AlertCircle,
  Play,
  RefreshCw,
} from 'lucide-react'
import { Button, Card, CardHeader, CardTitle, CardContent, Progress, Badge } from '../components/ui'
import { ComplianceScore, ControlCard, GapsReport } from '../components/dashboard'
import { useJob, useJobEvidence, useJobGaps, useRunJob } from '../hooks/useJobs'
import { useControls } from '../hooks/useControls'
import { formatDate } from '../lib/utils'
import { getErrorMessage } from '../lib/axios'

export default function JobDetailsPage() {
  const { jobId } = useParams<{ jobId: string }>()
  const { data: job, isLoading: jobLoading } = useJob(jobId || '')
  const { data: evidence } = useJobEvidence(jobId || '')
  const { data: gaps } = useJobGaps(jobId || '')
  const { data: controls } = useControls()
  const runJob = useRunJob()
  
  const [runError, setRunError] = useState('')

  const handleRunAnalysis = async () => {
    if (!jobId) return
    setRunError('')
    try {
      await runJob.mutateAsync(jobId)
    } catch (err) {
      setRunError(getErrorMessage(err))
    }
  }

  if (jobLoading) {
    return (
      <div className="flex items-center justify-center h-96">
        <Loader2 className="h-8 w-8 text-primary-600 animate-spin" />
      </div>
    )
  }

  if (!job) {
    return (
      <div className="text-center py-12">
        <AlertCircle className="h-12 w-12 text-gray-400 mx-auto mb-4" />
        <h2 className="text-lg font-medium text-gray-900">Job not found</h2>
        <Link to="/" className="text-primary-600 hover:text-primary-700 mt-2 inline-block">
          Return to dashboard
        </Link>
      </div>
    )
  }

  const getStatusIcon = () => {
    switch (job.status) {
      case 'SUCCEEDED':
        return <CheckCircle className="h-6 w-6 text-green-500" />
      case 'FAILED':
        return <XCircle className="h-6 w-6 text-red-500" />
      case 'RUNNING':
        return <Loader2 className="h-6 w-6 text-blue-500 animate-spin" />
      default:
        return <Clock className="h-6 w-6 text-gray-400" />
    }
  }

  const getControlById = (controlId: string) => {
    return controls?.controls.find((c) => c.control_id === controlId)
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div>
        <Link
          to="/"
          className="inline-flex items-center text-sm text-gray-500 hover:text-gray-700 mb-4"
        >
          <ArrowLeft className="h-4 w-4 mr-1" />
          Back to Dashboard
        </Link>

        <div className="flex items-center justify-between">
          <div className="flex items-center gap-4">
            {getStatusIcon()}
            <div>
              <h1 className="text-2xl font-bold text-gray-900">
                {job.job_type.toUpperCase()} Analysis
              </h1>
              <p className="text-gray-500 mt-1">
                Started {formatDate(job.created_at)}
              </p>
            </div>
          </div>
          <Badge variant="status" status={job.status.toLowerCase()} className="text-base px-4 py-1.5">
            {job.status}
          </Badge>
        </div>
      </div>

      {/* Progress for running jobs */}
      {job.status === 'RUNNING' && (
        <Card>
          <CardContent className="py-6">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm font-medium text-gray-700">
                Analyzing controls...
              </span>
              <span className="text-sm text-gray-500">
                {job.progress}/{job.total_controls}
              </span>
            </div>
            <Progress value={job.progress} max={job.total_controls} />
          </CardContent>
        </Card>
      )}

      {/* Error message */}
      {job.status === 'FAILED' && job.error_message && (
        <Card className="border-red-200 bg-red-50">
          <CardContent className="py-4">
            <div className="flex items-start gap-3">
              <XCircle className="h-5 w-5 text-red-500 flex-shrink-0 mt-0.5" />
              <div className="flex-1">
                <p className="font-medium text-red-800">Analysis Failed</p>
                <p className="text-sm text-red-700 mt-1">{job.error_message}</p>
              </div>
              <Button
                onClick={handleRunAnalysis}
                isLoading={runJob.isPending}
                size="sm"
              >
                <RefreshCw className="h-4 w-4 mr-1" />
                Retry
              </Button>
            </div>
          </CardContent>
        </Card>
      )}

      {/* Run error */}
      {runError && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
          <AlertCircle className="h-5 w-5 text-red-500 flex-shrink-0 mt-0.5" />
          <p className="text-sm text-red-700">{runError}</p>
        </div>
      )}

      {/* Pending job - show run button */}
      {job.status === 'PENDING' && (
        <Card>
          <CardContent className="py-8 text-center">
            <Clock className="h-12 w-12 text-gray-400 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              Analysis Pending
            </h3>
            <p className="text-sm text-gray-500 mb-4">
              Click below to start the compliance analysis with Gemini AI
            </p>
            <Button
              onClick={handleRunAnalysis}
              isLoading={runJob.isPending}
              size="lg"
            >
              <Play className="h-4 w-4 mr-2" />
              Start Analysis
            </Button>
          </CardContent>
        </Card>
      )}

      {/* Results for completed jobs */}
      {job.status === 'SUCCEEDED' && evidence && (
        <>
          {/* Summary */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <ComplianceScore
              passing={evidence.passing}
              failing={evidence.failing}
              needsReview={evidence.needs_review}
              total={evidence.total}
            />

            {/* Quick Stats */}
            <Card>
              <CardHeader>
                <CardTitle>Analysis Summary</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-2 gap-4">
                  <div className="p-4 bg-gray-50 rounded-lg">
                    <p className="text-sm text-gray-500">Total Controls</p>
                    <p className="text-2xl font-bold text-gray-900">
                      {evidence.total}
                    </p>
                  </div>
                  <div className="p-4 bg-green-50 rounded-lg">
                    <p className="text-sm text-green-600">Passing</p>
                    <p className="text-2xl font-bold text-green-700">
                      {evidence.passing}
                    </p>
                  </div>
                  <div className="p-4 bg-red-50 rounded-lg">
                    <p className="text-sm text-red-600">Failing</p>
                    <p className="text-2xl font-bold text-red-700">
                      {evidence.failing}
                    </p>
                  </div>
                  <div className="p-4 bg-yellow-50 rounded-lg">
                    <p className="text-sm text-yellow-600">Needs Review</p>
                    <p className="text-2xl font-bold text-yellow-700">
                      {evidence.needs_review}
                    </p>
                  </div>
                </div>
                {job.completed_at && (
                  <p className="text-xs text-gray-500 mt-4">
                    Completed {formatDate(job.completed_at)}
                  </p>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Gaps Report */}
          {gaps && gaps.gaps.length > 0 && (
            <GapsReport gaps={gaps.gaps} />
          )}

          {/* Evidence Items */}
          <div>
            <h2 className="text-lg font-semibold text-gray-900 mb-4">
              Control Evidence ({evidence.total})
            </h2>
            <div className="grid grid-cols-1 gap-4">
              {evidence.evidence_items.map((item) => (
                <ControlCard
                  key={item.id}
                  evidence={item}
                  control={getControlById(item.control_id)}
                />
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  )
}
