import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Card, CardHeader, CardTitle, CardContent } from '../ui/Card';
import Button from '../ui/Button';
import Badge from '../ui/Badge';

// Demo data that showcases all features
const DEMO_ANALYSIS = {
  organization: 'Acme Corporation',
  score: 72.5,
  riskLevel: 'medium',
  auditReadiness: 'Almost Ready',
  totalControls: 8,
  passing: 5,
  failing: 1,
  needsReview: 2,
  categories: [
    { name: 'Security', score: 75, controls: 6, passing: 4 },
    { name: 'Availability', score: 95, controls: 1, passing: 1 },
    { name: 'Processing Integrity', score: 60, controls: 1, passing: 0 },
  ],
  controls: [
    {
      id: 'CC6.1',
      title: 'Logical Access Security',
      category: 'Security',
      status: 'pass',
      confidence: 92,
      summary: 'Strong access controls with MFA and RBAC implemented.',
    },
    {
      id: 'CC6.2',
      title: 'User Registration',
      category: 'Security',
      status: 'pass',
      confidence: 88,
      summary: 'Documented onboarding with manager approval workflow.',
    },
    {
      id: 'CC6.3',
      title: 'Access Removal',
      category: 'Security',
      status: 'needs_review',
      confidence: 65,
      summary: 'Termination procedures exist but need documentation.',
      gaps: ['Automated deprovisioning not documented', 'Transfer procedures missing'],
    },
    {
      id: 'CC7.3',
      title: 'Incident Response',
      category: 'Security',
      status: 'pass',
      confidence: 85,
      summary: 'IR plan with severity levels and escalation paths.',
    },
    {
      id: 'CC8.1',
      title: 'Change Management',
      category: 'Security',
      status: 'pass',
      confidence: 90,
      summary: 'Formal CAB approval with testing requirements.',
    },
    {
      id: 'CC9.1',
      title: 'Risk Assessment',
      category: 'Security',
      status: 'fail',
      confidence: 78,
      summary: 'No documented risk assessment methodology found.',
      gaps: ['No risk register', 'No risk treatment plans', 'Annual review not evidenced'],
    },
    {
      id: 'A1.2',
      title: 'Backup and Recovery',
      category: 'Availability',
      status: 'pass',
      confidence: 95,
      summary: 'Comprehensive backup with 4-hour RTO, 1-hour RPO.',
    },
    {
      id: 'PI1.1',
      title: 'Processing Integrity',
      category: 'Processing Integrity',
      status: 'needs_review',
      confidence: 55,
      summary: 'Data validation exists but needs better documentation.',
      gaps: ['Validation rules not documented', 'Error handling procedures unclear'],
    },
  ],
  recommendations: [
    '🎯 Priority: Implement formal risk assessment methodology',
    '🚨 Address 1 critical gap before audit',
    '📝 Document existing access removal procedures',
    '🔍 Implement continuous monitoring for processing integrity',
    '✅ Maintain current security posture',
  ],
  estimatedHours: 96,
};

const DEMO_REMEDIATION = {
  totalTasks: 3,
  completedTasks: 0,
  progress: 0,
  tasks: [
    {
      id: '1',
      controlId: 'CC9.1',
      title: 'Implement Risk Assessment Program',
      priority: 'critical',
      status: 'not_started',
      hours: 40,
      dueDate: '2 weeks',
    },
    {
      id: '2',
      controlId: 'CC6.3',
      title: 'Document Access Removal Procedures',
      priority: 'high',
      status: 'not_started',
      hours: 24,
      dueDate: '4 weeks',
    },
    {
      id: '3',
      controlId: 'PI1.1',
      title: 'Document Processing Validation',
      priority: 'medium',
      status: 'not_started',
      hours: 32,
      dueDate: '8 weeks',
    },
  ],
};

interface DemoModeProps {
  isOpen: boolean;
  onClose: () => void;
}

export function DemoMode({ isOpen, onClose }: DemoModeProps) {
  const [activeTab, setActiveTab] = useState<'dashboard' | 'controls' | 'remediation' | 'report'>('dashboard');
  const [isGeneratingReport, setIsGeneratingReport] = useState(false);

  const handleDownloadReport = async () => {
    setIsGeneratingReport(true);
    try {
      const response = await fetch(
        `${import.meta.env.VITE_API_URL || 'http://localhost:8000/api'}/reports/demo?organization_name=${encodeURIComponent(DEMO_ANALYSIS.organization)}`
      );
      
      if (response.ok) {
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `ShieldAgent_Demo_Report.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        a.remove();
      }
    } catch (error) {
      console.error('Failed to download report:', error);
    }
    setIsGeneratingReport(false);
  };

  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        className="fixed inset-0 z-50 overflow-y-auto"
      >
        {/* Backdrop */}
        <div className="fixed inset-0 bg-black/70" onClick={onClose} />

        {/* Modal */}
        <div className="relative min-h-screen flex items-center justify-center p-4">
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            exit={{ scale: 0.9, opacity: 0 }}
            className="relative bg-gray-900 rounded-xl w-full max-w-6xl max-h-[90vh] overflow-hidden shadow-2xl border border-gray-700"
          >
            {/* Header */}
            <div className="bg-gradient-to-r from-indigo-600 to-purple-600 p-4 flex items-center justify-between">
              <div>
                <h2 className="text-xl font-bold text-white flex items-center gap-2">
                  <span className="text-2xl">🎮</span> Demo Mode
                </h2>
                <p className="text-indigo-200 text-sm">
                  Explore ShieldAgent with sample compliance data
                </p>
              </div>
              <button
                onClick={onClose}
                className="text-white/80 hover:text-white p-2 rounded-lg hover:bg-white/10 transition-colors"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            {/* Tabs */}
            <div className="border-b border-gray-700 bg-gray-800/50">
              <div className="flex space-x-1 p-2">
                {[
                  { id: 'dashboard', label: '📊 Dashboard', icon: '📊' },
                  { id: 'controls', label: '🔐 Controls', icon: '🔐' },
                  { id: 'remediation', label: '🔧 Remediation', icon: '🔧' },
                  { id: 'report', label: '📄 Report', icon: '📄' },
                ].map((tab) => (
                  <button
                    key={tab.id}
                    onClick={() => setActiveTab(tab.id as typeof activeTab)}
                    className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                      activeTab === tab.id
                        ? 'bg-indigo-600 text-white'
                        : 'text-gray-400 hover:text-white hover:bg-gray-700'
                    }`}
                  >
                    {tab.label}
                  </button>
                ))}
              </div>
            </div>

            {/* Content */}
            <div className="p-6 overflow-y-auto max-h-[calc(90vh-180px)]">
              {activeTab === 'dashboard' && <DemoDashboard data={DEMO_ANALYSIS} />}
              {activeTab === 'controls' && <DemoControls controls={DEMO_ANALYSIS.controls} />}
              {activeTab === 'remediation' && <DemoRemediation data={DEMO_REMEDIATION} />}
              {activeTab === 'report' && (
                <DemoReport
                  onDownload={handleDownloadReport}
                  isGenerating={isGeneratingReport}
                />
              )}
            </div>
          </motion.div>
        </div>
      </motion.div>
    </AnimatePresence>
  );
}

// Dashboard Tab
function DemoDashboard({ data }: { data: typeof DEMO_ANALYSIS }) {
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-400';
    if (score >= 60) return 'text-yellow-400';
    return 'text-red-400';
  };

  const getRiskBadge = (level: string) => {
    const variants: Record<string, 'success' | 'warning' | 'error' | 'default'> = {
      low: 'success',
      medium: 'warning',
      high: 'error',
      critical: 'error',
    };
    return variants[level] || 'default';
  };

  return (
    <div className="space-y-6">
      {/* Score Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="bg-gradient-to-br from-indigo-500/20 to-purple-500/20 border-indigo-500/30">
          <CardContent className="p-4 text-center">
            <p className="text-sm text-gray-400 mb-1">Compliance Score</p>
            <p className={`text-4xl font-bold ${getScoreColor(data.score)}`}>
              {data.score}%
            </p>
          </CardContent>
        </Card>
        
        <Card className="border-gray-700">
          <CardContent className="p-4 text-center">
            <p className="text-sm text-gray-400 mb-1">Risk Level</p>
            <Badge variant={getRiskBadge(data.riskLevel)} className="text-lg px-3 py-1">
              {data.riskLevel.toUpperCase()}
            </Badge>
          </CardContent>
        </Card>
        
        <Card className="border-gray-700">
          <CardContent className="p-4 text-center">
            <p className="text-sm text-gray-400 mb-1">Audit Readiness</p>
            <p className="text-xl font-semibold text-indigo-400">{data.auditReadiness}</p>
          </CardContent>
        </Card>
        
        <Card className="border-gray-700">
          <CardContent className="p-4 text-center">
            <p className="text-sm text-gray-400 mb-1">Remediation Time</p>
            <p className="text-xl font-semibold text-amber-400">{data.estimatedHours}h</p>
          </CardContent>
        </Card>
      </div>

      {/* Control Status */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Card className="border-gray-700">
          <CardHeader>
            <CardTitle className="text-lg">Control Status</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex items-center justify-around">
              <div className="text-center">
                <div className="w-16 h-16 rounded-full bg-green-500/20 flex items-center justify-center mb-2">
                  <span className="text-2xl font-bold text-green-400">{data.passing}</span>
                </div>
                <p className="text-sm text-gray-400">Passing</p>
              </div>
              <div className="text-center">
                <div className="w-16 h-16 rounded-full bg-yellow-500/20 flex items-center justify-center mb-2">
                  <span className="text-2xl font-bold text-yellow-400">{data.needsReview}</span>
                </div>
                <p className="text-sm text-gray-400">Review</p>
              </div>
              <div className="text-center">
                <div className="w-16 h-16 rounded-full bg-red-500/20 flex items-center justify-center mb-2">
                  <span className="text-2xl font-bold text-red-400">{data.failing}</span>
                </div>
                <p className="text-sm text-gray-400">Failing</p>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="border-gray-700">
          <CardHeader>
            <CardTitle className="text-lg">Category Scores</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-3">
              {data.categories.map((cat) => (
                <div key={cat.name}>
                  <div className="flex justify-between text-sm mb-1">
                    <span className="text-gray-300">{cat.name}</span>
                    <span className={getScoreColor(cat.score)}>{cat.score}%</span>
                  </div>
                  <div className="w-full bg-gray-700 rounded-full h-2">
                    <div
                      className={`h-2 rounded-full ${
                        cat.score >= 80 ? 'bg-green-500' : cat.score >= 60 ? 'bg-yellow-500' : 'bg-red-500'
                      }`}
                      style={{ width: `${cat.score}%` }}
                    />
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Recommendations */}
      <Card className="border-gray-700">
        <CardHeader>
          <CardTitle className="text-lg">AI Recommendations</CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="space-y-2">
            {data.recommendations.map((rec, i) => (
              <li key={i} className="text-gray-300 text-sm bg-gray-800/50 p-3 rounded-lg">
                {rec}
              </li>
            ))}
          </ul>
        </CardContent>
      </Card>
    </div>
  );
}

// Controls Tab
function DemoControls({ controls }: { controls: typeof DEMO_ANALYSIS.controls }) {
  const getStatusBadge = (status: string) => {
    const map: Record<string, 'success' | 'warning' | 'error'> = {
      pass: 'success',
      needs_review: 'warning',
      fail: 'error',
    };
    return map[status] || 'default';
  };

  return (
    <div className="space-y-4">
      {controls.map((control) => (
        <Card key={control.id} className="border-gray-700 hover:border-gray-600 transition-colors">
          <CardContent className="p-4">
            <div className="flex items-start justify-between">
              <div className="flex-1">
                <div className="flex items-center gap-3 mb-2">
                  <span className="text-indigo-400 font-mono text-sm bg-indigo-500/20 px-2 py-1 rounded">
                    {control.id}
                  </span>
                  <h3 className="font-semibold text-white">{control.title}</h3>
                  <Badge variant={getStatusBadge(control.status)}>
                    {control.status === 'needs_review' ? 'Needs Review' : control.status.toUpperCase()}
                  </Badge>
                </div>
                <p className="text-sm text-gray-400 mb-2">{control.summary}</p>
                <div className="flex items-center gap-4 text-xs text-gray-500">
                  <span>Category: {control.category}</span>
                  <span>Confidence: {control.confidence}%</span>
                </div>
                {control.gaps && control.gaps.length > 0 && (
                  <div className="mt-3 p-3 bg-red-500/10 border border-red-500/30 rounded-lg">
                    <p className="text-xs font-semibold text-red-400 mb-1">Identified Gaps:</p>
                    <ul className="list-disc list-inside text-xs text-red-300 space-y-1">
                      {control.gaps.map((gap, i) => (
                        <li key={i}>{gap}</li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}

// Remediation Tab
function DemoRemediation({ data }: { data: typeof DEMO_REMEDIATION }) {
  const getPriorityColor = (priority: string) => {
    const map: Record<string, string> = {
      critical: 'text-red-400 bg-red-500/20',
      high: 'text-orange-400 bg-orange-500/20',
      medium: 'text-yellow-400 bg-yellow-500/20',
      low: 'text-green-400 bg-green-500/20',
    };
    return map[priority] || 'text-gray-400 bg-gray-500/20';
  };

  return (
    <div className="space-y-6">
      {/* Progress Overview */}
      <Card className="border-gray-700 bg-gradient-to-r from-gray-800 to-gray-800/50">
        <CardContent className="p-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h3 className="text-lg font-semibold text-white">Remediation Progress</h3>
              <p className="text-sm text-gray-400">
                {data.completedTasks} of {data.totalTasks} tasks completed
              </p>
            </div>
            <div className="text-right">
              <p className="text-3xl font-bold text-indigo-400">{data.progress}%</p>
              <p className="text-xs text-gray-500">Complete</p>
            </div>
          </div>
          <div className="w-full bg-gray-700 rounded-full h-3">
            <div
              className="h-3 rounded-full bg-gradient-to-r from-indigo-500 to-purple-500 transition-all"
              style={{ width: `${data.progress}%` }}
            />
          </div>
        </CardContent>
      </Card>

      {/* Tasks */}
      <div className="space-y-3">
        <h3 className="text-lg font-semibold text-white">Remediation Tasks</h3>
        {data.tasks.map((task) => (
          <Card key={task.id} className="border-gray-700">
            <CardContent className="p-4">
              <div className="flex items-center gap-4">
                <div className="flex-shrink-0">
                  <div className="w-10 h-10 rounded-full bg-gray-700 flex items-center justify-center">
                    <span className="text-lg">
                      {task.status === 'completed' ? '✅' : task.status === 'in_progress' ? '🔄' : '⏳'}
                    </span>
                  </div>
                </div>
                <div className="flex-1">
                  <div className="flex items-center gap-2 mb-1">
                    <span className="text-xs font-mono text-indigo-400">{task.controlId}</span>
                    <span className={`text-xs px-2 py-0.5 rounded-full ${getPriorityColor(task.priority)}`}>
                      {task.priority.toUpperCase()}
                    </span>
                  </div>
                  <h4 className="font-medium text-white">{task.title}</h4>
                  <div className="flex items-center gap-4 mt-1 text-xs text-gray-500">
                    <span>⏱ {task.hours}h estimated</span>
                    <span>📅 Due: {task.dueDate}</span>
                  </div>
                </div>
                <Button variant="outline" size="sm" disabled>
                  Start Task
                </Button>
              </div>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}

// Report Tab
function DemoReport({ onDownload, isGenerating }: { onDownload: () => void; isGenerating: boolean }) {
  return (
    <div className="space-y-6">
      <Card className="border-gray-700">
        <CardContent className="p-8 text-center">
          <div className="w-20 h-20 mx-auto mb-6 bg-gradient-to-br from-indigo-500 to-purple-500 rounded-2xl flex items-center justify-center">
            <span className="text-4xl">📄</span>
          </div>
          <h3 className="text-2xl font-bold text-white mb-2">
            Generate Compliance Report
          </h3>
          <p className="text-gray-400 mb-6 max-w-md mx-auto">
            Download a professional PDF report with executive summary, compliance scores, 
            control analysis, and remediation recommendations.
          </p>
          
          <div className="bg-gray-800 rounded-lg p-4 mb-6 max-w-md mx-auto">
            <h4 className="text-sm font-semibold text-white mb-3">Report Includes:</h4>
            <ul className="text-sm text-gray-400 space-y-2 text-left">
              <li className="flex items-center gap-2">
                <span className="text-green-400">✓</span> Executive Summary
              </li>
              <li className="flex items-center gap-2">
                <span className="text-green-400">✓</span> Compliance Score Breakdown
              </li>
              <li className="flex items-center gap-2">
                <span className="text-green-400">✓</span> Control-by-Control Analysis
              </li>
              <li className="flex items-center gap-2">
                <span className="text-green-400">✓</span> Gap Identification & Remediation
              </li>
              <li className="flex items-center gap-2">
                <span className="text-green-400">✓</span> AI-Powered Recommendations
              </li>
            </ul>
          </div>

          <Button
            onClick={onDownload}
            disabled={isGenerating}
            className="bg-gradient-to-r from-indigo-500 to-purple-500 hover:from-indigo-600 hover:to-purple-600 text-white px-8 py-3 text-lg"
          >
            {isGenerating ? (
              <>
                <svg className="animate-spin -ml-1 mr-3 h-5 w-5" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                </svg>
                Generating...
              </>
            ) : (
              <>
                <span className="mr-2">📥</span> Download PDF Report
              </>
            )}
          </Button>
        </CardContent>
      </Card>

      {/* Sample Report Preview */}
      <Card className="border-gray-700">
        <CardHeader>
          <CardTitle className="text-lg">Report Preview</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="bg-white rounded-lg p-6 text-gray-900">
            <div className="border-b border-gray-200 pb-4 mb-4">
              <h1 className="text-xl font-bold text-indigo-600">🛡️ ShieldAgent</h1>
              <h2 className="text-2xl font-bold mt-2">SOC 2 Compliance Report</h2>
              <p className="text-gray-500 text-sm">Acme Corporation • Generated Today</p>
            </div>
            
            <div className="grid grid-cols-3 gap-4 mb-4">
              <div className="text-center p-3 bg-indigo-50 rounded-lg">
                <p className="text-2xl font-bold text-indigo-600">72.5%</p>
                <p className="text-xs text-gray-500">Compliance Score</p>
              </div>
              <div className="text-center p-3 bg-yellow-50 rounded-lg">
                <p className="text-2xl font-bold text-yellow-600">Medium</p>
                <p className="text-xs text-gray-500">Risk Level</p>
              </div>
              <div className="text-center p-3 bg-green-50 rounded-lg">
                <p className="text-2xl font-bold text-green-600">96h</p>
                <p className="text-xs text-gray-500">Est. Remediation</p>
              </div>
            </div>
            
            <p className="text-xs text-gray-400 text-center">
              [Full report continues with detailed analysis...]
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

export default DemoMode;
