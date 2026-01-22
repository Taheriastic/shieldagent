import { Link } from 'react-router-dom'
import {
  Clock,
  CheckCircle,
  XCircle,
  Loader2,
  ChevronRight,
} from 'lucide-react'
import { Card, CardHeader, CardTitle, CardContent, Badge, Progress } from '../ui'
import { formatDate } from '../../lib/utils'
import type { Job } from '../../types'

interface RecentJobsProps {
  jobs: Job[]
}

export default function RecentJobs({ jobs }: RecentJobsProps) {
  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'SUCCEEDED':
        return <CheckCircle className="h-5 w-5 text-green-500" />
      case 'FAILED':
        return <XCircle className="h-5 w-5 text-red-500" />
      case 'RUNNING':
        return <Loader2 className="h-5 w-5 text-blue-500 animate-spin" />
      default:
        return <Clock className="h-5 w-5 text-gray-400" />
    }
  }

  if (jobs.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Recent Jobs</CardTitle>
        </CardHeader>
        <CardContent className="py-8 text-center">
          <Clock className="h-12 w-12 text-gray-300 mx-auto mb-4" />
          <p className="text-gray-500">No jobs yet</p>
          <p className="text-sm text-gray-400 mt-1">
            Upload documents and run your first compliance check
          </p>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Recent Jobs</CardTitle>
      </CardHeader>
      <CardContent className="p-0">
        <div className="divide-y divide-gray-200">
          {jobs.slice(0, 5).map((job) => (
            <Link
              key={job.id}
              to={`/jobs/${job.id}`}
              className="flex items-center justify-between p-4 hover:bg-gray-50 transition-colors"
            >
              <div className="flex items-center gap-3">
                {getStatusIcon(job.status)}
                <div>
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-medium text-gray-900">
                      {job.job_type.toUpperCase()} Analysis
                    </span>
                    <Badge variant="status" status={job.status.toLowerCase()}>
                      {job.status}
                    </Badge>
                  </div>
                  <p className="text-xs text-gray-500 mt-0.5">
                    {formatDate(job.created_at)}
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-4">
                {job.status === 'RUNNING' && (
                  <div className="w-24">
                    <Progress
                      value={job.progress}
                      max={job.total_controls}
                      showLabel
                    />
                  </div>
                )}
                <ChevronRight className="h-5 w-5 text-gray-400" />
              </div>
            </Link>
          ))}
        </div>
      </CardContent>
    </Card>
  )
}
