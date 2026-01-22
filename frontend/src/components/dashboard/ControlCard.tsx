import { useState } from 'react'
import {
  CheckCircle,
  XCircle,
  AlertCircle,
  ChevronDown,
  ChevronUp,
  Sparkles,
  Settings,
} from 'lucide-react'
import { Card, CardContent, Badge } from '../ui'
import type { EvidenceItem, Control } from '../../types'

interface ControlCardProps {
  evidence: EvidenceItem
  control?: Control
}

export default function ControlCard({ evidence, control }: ControlCardProps) {
  const [isExpanded, setIsExpanded] = useState(false)

  const getStatusIcon = () => {
    switch (evidence.status) {
      case 'pass':
        return <CheckCircle className="h-5 w-5 text-green-500" />
      case 'fail':
        return <XCircle className="h-5 w-5 text-red-500" />
      case 'needs_review':
        return <AlertCircle className="h-5 w-5 text-yellow-500" />
      default:
        return <AlertCircle className="h-5 w-5 text-gray-400" />
    }
  }

  const getStatusBadge = () => {
    switch (evidence.status) {
      case 'pass':
        return <Badge variant="status" status="pass">Pass</Badge>
      case 'fail':
        return <Badge variant="status" status="fail">Fail</Badge>
      case 'needs_review':
        return <Badge variant="status" status="needs_review">Needs Review</Badge>
      default:
        return <Badge>Unknown</Badge>
    }
  }

  return (
    <Card className="transition-shadow hover:shadow-md">
      <CardContent className="p-4">
        {/* Header */}
        <div className="flex items-start justify-between">
          <div className="flex items-start gap-3">
            {getStatusIcon()}
            <div>
              <div className="flex items-center gap-2">
                <span className="font-mono text-sm font-semibold text-primary-600">
                  {evidence.control_id}
                </span>
                {control?.check_type === 'ai_prompt' ? (
                  <Sparkles className="h-4 w-4 text-purple-500" />
                ) : (
                  <Settings className="h-4 w-4 text-gray-400" />
                )}
              </div>
              <h4 className="text-sm font-medium text-gray-900 mt-0.5">
                {control?.title || evidence.control_id}
              </h4>
            </div>
          </div>
          <div className="flex items-center gap-2">
            {getStatusBadge()}
            {evidence.confidence > 0 && (
              <span className="text-xs text-gray-500">
                {Math.round(evidence.confidence * 100)}% confidence
              </span>
            )}
          </div>
        </div>

        {/* Summary */}
        {evidence.summary && (
          <p className="mt-3 text-sm text-gray-600 line-clamp-2">
            {evidence.summary}
          </p>
        )}

        {/* Expand/Collapse */}
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="flex items-center gap-1 mt-3 text-sm text-primary-600 hover:text-primary-700"
        >
          {isExpanded ? (
            <>
              <ChevronUp className="h-4 w-4" />
              Hide details
            </>
          ) : (
            <>
              <ChevronDown className="h-4 w-4" />
              Show details
            </>
          )}
        </button>

        {/* Expanded Content */}
        {isExpanded && (
          <div className="mt-4 pt-4 border-t border-gray-200 space-y-4 animate-fade-in">
            {/* Evidence Quote */}
            {evidence.evidence_quote && (
              <div>
                <h5 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
                  Evidence Quote
                </h5>
                <blockquote className="text-sm text-gray-700 bg-gray-50 p-3 rounded-lg border-l-4 border-primary-500">
                  "{evidence.evidence_quote}"
                </blockquote>
              </div>
            )}

            {/* Source Location */}
            {evidence.source_location && (
              <div>
                <h5 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
                  Source
                </h5>
                <p className="text-sm text-gray-600">{evidence.source_location}</p>
              </div>
            )}

            {/* Control Description */}
            {control?.description && (
              <div>
                <h5 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
                  Control Description
                </h5>
                <p className="text-sm text-gray-600">{control.description}</p>
              </div>
            )}

            {/* Raw Response (for debugging) */}
            {evidence.evidence_metadata && Object.keys(evidence.evidence_metadata).length > 0 && (
              <div>
                <h5 className="text-xs font-semibold text-gray-500 uppercase tracking-wider mb-2">
                  Metadata
                </h5>
                <pre className="text-xs text-gray-600 bg-gray-50 p-3 rounded-lg overflow-auto max-h-40">
                  {JSON.stringify(evidence.evidence_metadata, null, 2)}
                </pre>
              </div>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  )
}
