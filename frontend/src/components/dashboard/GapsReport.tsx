import { AlertTriangle } from 'lucide-react'
import { Card, CardHeader, CardTitle, CardContent, Badge } from '../ui'
import { cn, getSeverityColor } from '../../lib/utils'
import type { Gap } from '../../types'

interface GapsReportProps {
  gaps: Gap[]
}

export default function GapsReport({ gaps }: GapsReportProps) {
  if (gaps.length === 0) {
    return (
      <Card>
        <CardContent className="py-8 text-center">
          <div className="inline-flex items-center justify-center w-12 h-12 rounded-full bg-green-100 mb-4">
            <AlertTriangle className="h-6 w-6 text-green-600" />
          </div>
          <h3 className="text-lg font-medium text-gray-900">No Gaps Found</h3>
          <p className="text-sm text-gray-500 mt-1">
            All controls are passing or need review.
          </p>
        </CardContent>
      </Card>
    )
  }

  const severityOrder = ['critical', 'high', 'medium', 'low']
  const sortedGaps = [...gaps].sort((a, b) => {
    return severityOrder.indexOf(a.severity) - severityOrder.indexOf(b.severity)
  })

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>Compliance Gaps ({gaps.length})</CardTitle>
          <div className="flex items-center gap-2">
            {gaps.filter(g => g.severity === 'critical').length > 0 && (
              <Badge className={getSeverityColor('critical')}>
                {gaps.filter(g => g.severity === 'critical').length} Critical
              </Badge>
            )}
            {gaps.filter(g => g.severity === 'high').length > 0 && (
              <Badge className={getSeverityColor('high')}>
                {gaps.filter(g => g.severity === 'high').length} High
              </Badge>
            )}
          </div>
        </div>
      </CardHeader>
      <CardContent className="p-0">
        <div className="divide-y divide-gray-200">
          {sortedGaps.map((gap) => (
            <div key={gap.id} className="p-4 hover:bg-gray-50 transition-colors">
              <div className="flex items-start justify-between">
                <div className="flex items-start gap-3">
                  <span
                    className={cn(
                      'inline-flex items-center px-2 py-1 rounded text-xs font-medium border',
                      getSeverityColor(gap.severity)
                    )}
                  >
                    {gap.severity.toUpperCase()}
                  </span>
                  <div>
                    <div className="flex items-center gap-2">
                      <span className="font-mono text-sm font-semibold text-primary-600">
                        {gap.control_id}
                      </span>
                    </div>
                    <p className="text-sm text-gray-700 mt-1">
                      {gap.description}
                    </p>
                    {gap.remediation_suggestion && (
                      <div className="mt-2 p-2 bg-blue-50 rounded text-sm text-blue-800">
                        <strong>Remediation:</strong> {gap.remediation_suggestion}
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
