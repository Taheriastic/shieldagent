import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { Play, FileText, AlertCircle, Zap, Shield } from 'lucide-react'
import { Button, Card, CardContent } from '../components/ui'
import { ComplianceScore, RecentJobs } from '../components/dashboard'
import { useDocuments } from '../hooks/useDocuments'
import { useJobs, useCreateJob, useJobEvidence } from '../hooks/useJobs'
import { getErrorMessage } from '../lib/axios'

export default function DashboardPage() {
  const navigate = useNavigate()
  const { data: documentsData } = useDocuments()
  const { data: jobsData } = useJobs()
  const createJob = useCreateJob()
  
  const [isRunning, setIsRunning] = useState(false)
  const [error, setError] = useState('')
  const [scanType, setScanType] = useState<'quick' | 'full'>('quick')

  // Get latest completed job for compliance score
  const latestJob = jobsData?.jobs.find((j) => j.status === 'SUCCEEDED')
  const { data: evidenceData } = useJobEvidence(latestJob?.id || '')

  const handleRunAnalysis = async () => {
    if (!documentsData?.documents.length) {
      setError('Please upload documents first')
      return
    }

    setError('')
    setIsRunning(true)

    try {
      const job = await createJob.mutateAsync({
        framework: 'soc2',
        document_ids: documentsData.documents.map((d) => d.id),
        scan_type: scanType,
      })
      navigate(`/jobs/${job.id}`)
    } catch (err) {
      setError(getErrorMessage(err))
    } finally {
      setIsRunning(false)
    }
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
          <p className="text-gray-500 mt-1">
            SOC 2 compliance overview and quick actions
          </p>
        </div>
        <div className="flex items-center gap-3">
          {/* Scan Type Selector */}
          <div className="flex rounded-lg border border-gray-200 overflow-hidden">
            <button
              onClick={() => setScanType('quick')}
              className={`flex items-center gap-2 px-4 py-2 text-sm font-medium transition-colors ${
                scanType === 'quick'
                  ? 'bg-primary-600 text-white'
                  : 'bg-white text-gray-700 hover:bg-gray-50'
              }`}
            >
              <Zap className="h-4 w-4" />
              Quick (8)
            </button>
            <button
              onClick={() => setScanType('full')}
              className={`flex items-center gap-2 px-4 py-2 text-sm font-medium transition-colors ${
                scanType === 'full'
                  ? 'bg-primary-600 text-white'
                  : 'bg-white text-gray-700 hover:bg-gray-50'
              }`}
            >
              <Shield className="h-4 w-4" />
              Full (51)
            </button>
          </div>
          <Button
            onClick={handleRunAnalysis}
            isLoading={isRunning}
            disabled={!documentsData?.documents.length}
            size="lg"
          >
            <Play className="h-4 w-4 mr-2" />
            Run Analysis
          </Button>
        </div>
      </div>

      {/* Error Alert */}
      {error && (
        <div className="p-4 bg-red-50 border border-red-200 rounded-lg flex items-start gap-3">
          <AlertCircle className="h-5 w-5 text-red-500 flex-shrink-0 mt-0.5" />
          <p className="text-sm text-red-700">{error}</p>
        </div>
      )}

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-primary-100 rounded-lg">
                <FileText className="h-6 w-6 text-primary-600" />
              </div>
              <div>
                <p className="text-sm text-gray-500">Documents</p>
                <p className="text-2xl font-bold text-gray-900">
                  {documentsData?.total || 0}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-green-100 rounded-lg">
                <Play className="h-6 w-6 text-green-600" />
              </div>
              <div>
                <p className="text-sm text-gray-500">Analysis Runs</p>
                <p className="text-2xl font-bold text-gray-900">
                  {jobsData?.total || 0}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-yellow-100 rounded-lg">
                <AlertCircle className="h-6 w-6 text-yellow-600" />
              </div>
              <div>
                <p className="text-sm text-gray-500">Pending Review</p>
                <p className="text-2xl font-bold text-gray-900">
                  {evidenceData?.needs_review || 0}
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Compliance Score */}
        {evidenceData ? (
          <ComplianceScore
            passing={evidenceData.passing}
            failing={evidenceData.failing}
            needsReview={evidenceData.needs_review}
            total={evidenceData.total}
          />
        ) : (
          <Card className="h-full">
            <CardContent className="py-12 text-center">
              <div className="inline-flex items-center justify-center w-16 h-16 rounded-full bg-gray-100 mb-4">
                <Play className="h-8 w-8 text-gray-400" />
              </div>
              <h3 className="text-lg font-medium text-gray-900">
                No Analysis Yet
              </h3>
              <p className="text-sm text-gray-500 mt-2 max-w-sm mx-auto">
                Upload your compliance documents and run your first analysis to
                see your compliance score.
              </p>
              <Button
                onClick={() => navigate('/documents')}
                variant="secondary"
                className="mt-4"
              >
                Upload Documents
              </Button>
            </CardContent>
          </Card>
        )}

        {/* Recent Jobs */}
        <RecentJobs jobs={jobsData?.jobs || []} />
      </div>
    </div>
  )
}
