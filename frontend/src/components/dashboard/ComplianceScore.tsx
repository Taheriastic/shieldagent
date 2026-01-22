import { PieChart, Pie, Cell, ResponsiveContainer } from 'recharts'
import { CheckCircle, XCircle, AlertCircle } from 'lucide-react'
import { Card, CardContent } from '../ui'

interface ComplianceScoreProps {
  passing: number
  failing: number
  needsReview: number
  total: number
}

export default function ComplianceScore({
  passing,
  failing,
  needsReview,
  total,
}: ComplianceScoreProps) {
  const score = total > 0 ? Math.round((passing / total) * 100) : 0
  
  const data = [
    { name: 'Passing', value: passing, color: '#22c55e' },
    { name: 'Failing', value: failing, color: '#ef4444' },
    { name: 'Needs Review', value: needsReview, color: '#f59e0b' },
  ]

  const getScoreColor = () => {
    if (score >= 80) return 'text-green-600'
    if (score >= 50) return 'text-yellow-600'
    return 'text-red-600'
  }

  return (
    <Card className="h-full">
      <CardContent className="pt-6">
        <div className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold text-gray-900">
              Compliance Score
            </h3>
            <p className="text-sm text-gray-500 mt-1">
              Based on {total} controls
            </p>
          </div>
          <div className={`text-4xl font-bold ${getScoreColor()}`}>
            {score}%
          </div>
        </div>

        <div className="mt-6 flex items-center gap-8">
          {/* Pie Chart */}
          <div className="w-32 h-32">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={data}
                  cx="50%"
                  cy="50%"
                  innerRadius={35}
                  outerRadius={50}
                  paddingAngle={2}
                  dataKey="value"
                >
                  {data.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={entry.color} />
                  ))}
                </Pie>
              </PieChart>
            </ResponsiveContainer>
          </div>

          {/* Legend */}
          <div className="flex-1 space-y-3">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <CheckCircle className="h-4 w-4 text-green-500" />
                <span className="text-sm text-gray-600">Passing</span>
              </div>
              <span className="text-sm font-semibold text-gray-900">
                {passing}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <XCircle className="h-4 w-4 text-red-500" />
                <span className="text-sm text-gray-600">Failing</span>
              </div>
              <span className="text-sm font-semibold text-gray-900">
                {failing}
              </span>
            </div>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <AlertCircle className="h-4 w-4 text-yellow-500" />
                <span className="text-sm text-gray-600">Needs Review</span>
              </div>
              <span className="text-sm font-semibold text-gray-900">
                {needsReview}
              </span>
            </div>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}
