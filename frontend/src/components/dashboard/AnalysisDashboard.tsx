import { useState } from 'react'
import {
  AlertTriangle,
  CheckCircle,
  XCircle,
  Download,
  RefreshCw,
  ChevronRight,
  Target,
  BarChart3,
  PieChart,
} from 'lucide-react'
import { Button, Card, CardHeader, CardTitle, CardContent, Badge, Progress } from '../ui'

interface ControlResult {
  control_id: string
  category: string
  title: string
  status: 'pass' | 'fail' | 'needs_review'
  confidence: number
  summary: string
  evidence_quote?: string
  gaps: string[]
}

interface AnalysisResults {
  job_id: string
  created_at: string
  scan_type: 'quick' | 'full'
  total_controls: number
  passing: number
  failing: number
  needs_review: number
  controls: ControlResult[]
  categories: {
    name: string
    passing: number
    total: number
  }[]
}

// Mock data for demonstration
const mockResults: AnalysisResults = {
  job_id: 'job-123',
  created_at: new Date().toISOString(),
  scan_type: 'quick',
  total_controls: 8,
  passing: 5,
  failing: 1,
  needs_review: 2,
  controls: [
    {
      control_id: 'CC6.1',
      category: 'Logical and Physical Access',
      title: 'Logical Access Security',
      status: 'pass',
      confidence: 0.92,
      summary: 'Strong access controls found including MFA, RBAC, and quarterly access reviews.',
      evidence_quote: 'Multi-factor authentication required for all remote access',
      gaps: [],
    },
    {
      control_id: 'CC6.2',
      category: 'Logical and Physical Access',
      title: 'User Registration',
      status: 'pass',
      confidence: 0.88,
      summary: 'Documented user onboarding procedures with manager approval workflow.',
      evidence_quote: 'HR notifies IT of new hires 3 days before start date',
      gaps: [],
    },
    {
      control_id: 'CC6.3',
      category: 'Logical and Physical Access',
      title: 'Access Removal',
      status: 'needs_review',
      confidence: 0.65,
      summary: 'Some termination procedures exist but lack automated deprovisioning.',
      gaps: ['No automated deprovisioning', 'Missing transfer procedures'],
    },
    {
      control_id: 'CC7.2',
      category: 'System Operations',
      title: 'Security Monitoring',
      status: 'needs_review',
      confidence: 0.55,
      summary: 'Basic monitoring mentioned but no SIEM or 24/7 coverage documented.',
      gaps: ['No SIEM solution documented', 'Missing 24/7 monitoring procedures'],
    },
    {
      control_id: 'CC7.3',
      category: 'System Operations',
      title: 'Incident Response',
      status: 'pass',
      confidence: 0.85,
      summary: 'Incident response plan with severity levels and communication procedures.',
      evidence_quote: 'Security incidents reported within 1 hour',
      gaps: [],
    },
    {
      control_id: 'CC8.1',
      category: 'Change Management',
      title: 'Change Management Process',
      status: 'pass',
      confidence: 0.90,
      summary: 'Formal change approval process with CAB and documentation requirements.',
      evidence_quote: 'All changes require CAB approval before deployment',
      gaps: [],
    },
    {
      control_id: 'CC9.1',
      category: 'Risk Mitigation',
      title: 'Risk Assessment',
      status: 'fail',
      confidence: 0.78,
      summary: 'No documented risk assessment methodology or risk register found.',
      gaps: ['Missing risk assessment methodology', 'No risk register', 'No risk treatment plans'],
    },
    {
      control_id: 'A1.2',
      category: 'Availability',
      title: 'Backup and Recovery',
      status: 'pass',
      confidence: 0.95,
      summary: 'Comprehensive backup procedures with defined RTO/RPO and regular testing.',
      evidence_quote: 'Daily incremental backups, weekly full backups, 4-hour RTO',
      gaps: [],
    },
  ],
  categories: [
    { name: 'Logical and Physical Access', passing: 2, total: 3 },
    { name: 'System Operations', passing: 1, total: 2 },
    { name: 'Change Management', passing: 1, total: 1 },
    { name: 'Risk Mitigation', passing: 0, total: 1 },
    { name: 'Availability', passing: 1, total: 1 },
  ],
}

interface AnalysisDashboardProps {
  results?: AnalysisResults
  isLoading?: boolean
  onRunAnalysis?: () => void
}

export default function AnalysisDashboard({ 
  results = mockResults, 
  isLoading = false,
  onRunAnalysis 
}: AnalysisDashboardProps) {
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null)
  const [statusFilter, setStatusFilter] = useState<string | null>(null)

  const complianceScore = results ? Math.round((results.passing / results.total_controls) * 100) : 0
  
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600'
    if (score >= 60) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getScoreBgColor = (score: number) => {
    if (score >= 80) return 'bg-green-50 border-green-200'
    if (score >= 60) return 'bg-yellow-50 border-yellow-200'
    return 'bg-red-50 border-red-200'
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'pass':
        return <CheckCircle className="h-5 w-5 text-green-500" />
      case 'fail':
        return <XCircle className="h-5 w-5 text-red-500" />
      default:
        return <AlertTriangle className="h-5 w-5 text-yellow-500" />
    }
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'pass':
        return <Badge variant="success">Pass</Badge>
      case 'fail':
        return <Badge variant="error">Fail</Badge>
      default:
        return <Badge variant="warning">Review</Badge>
    }
  }

  const filteredControls = results?.controls.filter(control => {
    if (selectedCategory && control.category !== selectedCategory) return false
    if (statusFilter && control.status !== statusFilter) return false
    return true
  }) || []

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-gray-900 flex items-center gap-2">
            <BarChart3 className="h-7 w-7 text-primary-600" />
            Compliance Analysis Dashboard
          </h2>
          <p className="text-gray-500 mt-1">
            {results?.scan_type === 'full' ? 'Full scan' : 'Quick scan'} • {results?.total_controls} controls evaluated
          </p>
        </div>
        <div className="flex gap-3">
          <Button variant="outline" size="sm">
            <Download className="h-4 w-4 mr-2" />
            Export Report
          </Button>
          <Button onClick={onRunAnalysis} disabled={isLoading}>
            <RefreshCw className={`h-4 w-4 mr-2 ${isLoading ? 'animate-spin' : ''}`} />
            Re-run Analysis
          </Button>
        </div>
      </div>

      {/* Score Overview */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {/* Compliance Score */}
        <Card className={`border-2 ${getScoreBgColor(complianceScore)}`}>
          <CardContent className="pt-6">
            <div className="text-center">
              <div className={`text-5xl font-bold ${getScoreColor(complianceScore)}`}>
                {complianceScore}%
              </div>
              <p className="text-sm text-gray-600 mt-2">Compliance Score</p>
              <div className="mt-4">
                <Progress value={complianceScore} className="h-2" />
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Passing */}
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-green-100 rounded-lg">
                <CheckCircle className="h-6 w-6 text-green-600" />
              </div>
              <div>
                <p className="text-sm text-gray-500">Passing</p>
                <p className="text-2xl font-bold text-gray-900">{results?.passing || 0}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Failing */}
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-red-100 rounded-lg">
                <XCircle className="h-6 w-6 text-red-600" />
              </div>
              <div>
                <p className="text-sm text-gray-500">Failing</p>
                <p className="text-2xl font-bold text-gray-900">{results?.failing || 0}</p>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Needs Review */}
        <Card>
          <CardContent className="pt-6">
            <div className="flex items-center gap-4">
              <div className="p-3 bg-yellow-100 rounded-lg">
                <AlertTriangle className="h-6 w-6 text-yellow-600" />
              </div>
              <div>
                <p className="text-sm text-gray-500">Needs Review</p>
                <p className="text-2xl font-bold text-gray-900">{results?.needs_review || 0}</p>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Category Breakdown */}
      <Card>
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <PieChart className="h-5 w-5 text-primary-600" />
            Compliance by Category
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {results?.categories.map((category, index) => {
              const percentage = Math.round((category.passing / category.total) * 100)
              return (
                <div 
                  key={index}
                  className={`p-4 rounded-lg cursor-pointer transition-colors ${
                    selectedCategory === category.name 
                      ? 'bg-primary-50 border-2 border-primary-200' 
                      : 'bg-gray-50 hover:bg-gray-100'
                  }`}
                  onClick={() => setSelectedCategory(
                    selectedCategory === category.name ? null : category.name
                  )}
                >
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-medium text-gray-900">{category.name}</span>
                    <span className={`font-bold ${getScoreColor(percentage)}`}>
                      {category.passing}/{category.total} ({percentage}%)
                    </span>
                  </div>
                  <Progress value={percentage} className="h-2" />
                </div>
              )
            })}
          </div>
        </CardContent>
      </Card>

      {/* Controls Detail */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="flex items-center gap-2">
              <Target className="h-5 w-5 text-primary-600" />
              Control Details
            </CardTitle>
            <div className="flex gap-2">
              <select
                className="text-sm border rounded-md px-3 py-1.5 bg-white"
                value={statusFilter || ''}
                onChange={(e) => setStatusFilter(e.target.value || null)}
              >
                <option value="">All Status</option>
                <option value="pass">Passing</option>
                <option value="fail">Failing</option>
                <option value="needs_review">Needs Review</option>
              </select>
              {selectedCategory && (
                <Button 
                  variant="outline" 
                  size="sm"
                  onClick={() => setSelectedCategory(null)}
                >
                  Clear Filter
                </Button>
              )}
            </div>
          </div>
        </CardHeader>
        <CardContent>
          <div className="space-y-4">
            {filteredControls.map((control, index) => (
              <div
                key={index}
                className="border rounded-lg p-4 hover:shadow-md transition-shadow"
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-start gap-3">
                    {getStatusIcon(control.status)}
                    <div>
                      <div className="flex items-center gap-2">
                        <span className="font-mono text-sm text-primary-600 font-medium">
                          {control.control_id}
                        </span>
                        <span className="font-semibold text-gray-900">
                          {control.title}
                        </span>
                        {getStatusBadge(control.status)}
                      </div>
                      <p className="text-sm text-gray-500 mt-1">{control.category}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-sm text-gray-500">Confidence</div>
                    <div className={`font-bold ${control.confidence >= 0.8 ? 'text-green-600' : control.confidence >= 0.6 ? 'text-yellow-600' : 'text-red-600'}`}>
                      {Math.round(control.confidence * 100)}%
                    </div>
                  </div>
                </div>

                <p className="text-sm text-gray-700 mt-3">{control.summary}</p>

                {control.evidence_quote && (
                  <div className="mt-3 p-3 bg-green-50 border-l-4 border-green-400 rounded">
                    <p className="text-sm text-green-800">
                      <strong>Evidence:</strong> "{control.evidence_quote}"
                    </p>
                  </div>
                )}

                {control.gaps.length > 0 && (
                  <div className="mt-3 p-3 bg-red-50 border-l-4 border-red-400 rounded">
                    <p className="text-sm font-medium text-red-800 mb-2">Gaps Identified:</p>
                    <ul className="text-sm text-red-700 space-y-1">
                      {control.gaps.map((gap, gapIndex) => (
                        <li key={gapIndex} className="flex items-start gap-2">
                          <AlertTriangle className="h-4 w-4 flex-shrink-0 mt-0.5" />
                          {gap}
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            ))}

            {filteredControls.length === 0 && (
              <div className="text-center py-8 text-gray-500">
                No controls match the current filters
              </div>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Gaps Summary */}
      {results && results.controls.some(c => c.gaps.length > 0) && (
        <Card className="border-red-200 bg-red-50">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-red-700">
              <AlertTriangle className="h-5 w-5" />
              Remediation Required
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {results.controls
                .filter(c => c.gaps.length > 0)
                .map((control, index) => (
                  <div key={index} className="bg-white rounded-lg p-4">
                    <div className="flex items-center gap-2 mb-2">
                      <span className="font-mono text-sm text-primary-600 font-medium">
                        {control.control_id}
                      </span>
                      <span className="font-semibold text-gray-900">
                        {control.title}
                      </span>
                    </div>
                    <ul className="space-y-2">
                      {control.gaps.map((gap, gapIndex) => (
                        <li key={gapIndex} className="flex items-start gap-2 text-sm text-gray-700">
                          <ChevronRight className="h-4 w-4 text-red-500 flex-shrink-0 mt-0.5" />
                          {gap}
                        </li>
                      ))}
                    </ul>
                  </div>
                ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
